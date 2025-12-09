import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

def verify_api():
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("Error: OPENROUTER_API_KEY not found in environment variables.")
        return

    print(f"Found API Key: {api_key[:5]}...{api_key[-4:]}")
    
    try:
        llm = ChatOpenAI(
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            model_name=os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash")
        )
        response = llm.invoke("Hello, are you working?")
        print("\nAPI Check Successful!")
        print(f"Response: {response.content}")
    except Exception as e:
        print(f"\nAPI Check Failed: {e}")

if __name__ == "__main__":
    verify_api()
