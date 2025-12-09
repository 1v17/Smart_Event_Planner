import dotenv
import sys
from langchain_core.messages import HumanMessage
from agent import get_agent_graph

dotenv.load_dotenv()

def run_test_queries():
    print("Initializing Agent...")
    graph = get_agent_graph()
    config = {"configurable": {"thread_id": "test_thread_1"}}
    
    queries = [
        "I need a venue in Boston for 50 people.",
        "What amenities does it have?"
    ]
    
    print(f"Running {len(queries)} test queries...")
    
    for query in queries:
        print(f"\nUser: {query}")
        print("-" * 20)
        
        events = graph.stream(
            {"messages": [HumanMessage(content=query)]},
            config,
            stream_mode="values"
        )
        
        interaction_output = []
        for event in events:
            if "messages" in event:
                msg = event["messages"][-1]
                if msg.type == "ai" and msg.content:
                    print(f"Agent: {msg.content}")
                    interaction_output.append(msg.content)
        
        if not interaction_output:
            print("[WARNING] No AI response captured for this query.")
            
    print("\nTest Run Complete.")

if __name__ == "__main__":
    try:
        run_test_queries()
    except Exception as e:
        print(f"Verification failed with error: {e}")
        sys.exit(1)
