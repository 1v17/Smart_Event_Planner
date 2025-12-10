import dotenv
from agent import get_agent_graph

dotenv.load_dotenv()

def main():
    agent_executor = get_agent_graph()
    
    print("Welcome to Smart Event Planner! Type 'quit' to exit.")
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
                
            # Invoke the agent with the user input
            response = agent_executor.invoke({"input": user_input})
            
            # Print the agent's response
            if "output" in response:
                print(f"Agent: {response['output']}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
