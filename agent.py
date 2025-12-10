from langgraph.graph import END, StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage

from llm import get_llm
from tools import search_venues

# 1. State Definition
# We use the built-in MessagesState which already has:
# messages: Annotated[Sequence[BaseMessage], operator.add]


# 2. Graph Construction

def get_agent_graph():
    
    # Initialize LLM and bind tools
    llm = get_llm()
    tools = [search_venues]
    llm_with_tools = llm.bind_tools(tools)

    # Define the 'agent' node function
    def agent(state: MessagesState):
        messages = state["messages"]
        # Add a system message if it's not already there (though usually we prepend it to the list passed to invoke)
        # But 'messages' is the full history. 
        # A simple way: prepend a SystemMessage if one isn't the first message?
        # Or better: construct a list for the LLM that starts with the system prompt, followed by the conversation history.
            
        system_prompt = SystemMessage(
            content="You are a venue search assistant for event planning. You ONLY help with venue-related queries: searching venues, \
                comparing options, providing venue details (location, capacity, amenities, price), and helping users choose venues. \
                Use the search_venues tool to find information. \
                \
                REJECT all non-venue requests (general questions, creative writing, coding, weather, etc.) with: \
                'I'm sorry, I can only help with venue-related queries for event planning.'")
        
        # We invoke the LLM with the system prompt + history
        response = llm_with_tools.invoke([system_prompt] + messages)
        return {"messages": [response]}

    # Define the 'tools' node
    # ToolNode is a prebuilt node that executes tool calls found in the last message
    tool_node = ToolNode(tools)

    # Define the conditional edge logic
    def should_continue(state: MessagesState) -> str:
        messages = state["messages"]
        last_message = messages[-1]
        
        # If the LLM wants to call tools, route to "tools"
        if last_message.tool_calls:
            return "tools"
        # Otherwise, stop
        return END

    # Build the graph
    workflow = StateGraph(MessagesState)

    workflow.add_node("agent", agent)
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "agent")
    
    # Conditional edge from agent
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            END: END
        }
    )

    # Edge from tools back to agent
    workflow.add_edge("tools", "agent")

    # Compile the graph with memory checkpointer
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    
    return app
