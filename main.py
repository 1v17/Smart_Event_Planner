import dotenv
from langchain_core.messages import HumanMessage
from agent import get_agent_graph

dotenv.load_dotenv()

def main():
    graph = get_agent_graph()
    
    print("Welcome to Smart Event Planner! Type 'quit' to exit.")
    
    # Simple thread ID configuration for state endurance
    config = {"configurable": {"thread_id": "1"}}
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
                
            # Stream events from the graph
            # stream_mode="values" returns the full state at each step
            events = graph.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config,
                stream_mode="values"
            )
            
            for event in events:
                if "messages" in event:
                    messages = event["messages"]
                    if messages:
                        last_message = messages[-1]
                        # Only print AI messages to avoid double printing user input
                        if last_message.type == "ai" and last_message.content:
                            print(f"Agent: {last_message.content}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
