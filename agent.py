import warnings
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from llm import get_llm
from tools import search_venues

warnings.filterwarnings("ignore", category=DeprecationWarning)

ITERATION_LIMIT = 10

def get_agent_graph():
    """
    Returns a ReAct agent executor for venue search assistance with conversation memory.
    """
    # Initialize LLM
    llm = get_llm()
    
    # Wrap tools
    tools = [search_venues]
    
    # Define the ReAct prompt template with system instructions
    react_prompt = PromptTemplate.from_template(
        """You are a venue search assistant for event planning. You ONLY help with venue-related queries: searching venues, comparing options, providing venue details (location, capacity, amenities, price), and helping users choose venues.

REJECT all non-venue requests (general questions, creative writing, coding, weather, etc.).

You have access to the following tools:

{tools}

Use the following format EXACTLY:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

IMPORTANT: After seeing an Observation, you MUST either:
1. Start a new Thought/Action/Action Input sequence, OR
2. Write "Thought: I now know the final answer" followed by "Final Answer: [your answer]"

Do NOT write lengthy explanations in the middle of the chain. Save all user-facing explanations for the Final Answer.

Previous conversation history:
{chat_history}

Question: {input}
Thought: {agent_scratchpad}"""
    )
    
    # Create conversation memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=False
    )
    
    # Create the ReAct agent
    agent = create_react_agent(llm, tools, react_prompt)
    
    # Create an AgentExecutor with memory
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=ITERATION_LIMIT
    )
    
    return agent_executor
