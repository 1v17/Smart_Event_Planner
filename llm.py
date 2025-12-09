import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    """
    Returns a configured Chatbot (ChatOpenAI) instance pointing to OpenRouter.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv('OPENROUTER_MODEL')
    # Base URL for OpenRouter
    base_url = "https://openrouter.ai/api/v1"
    
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

    llm = ChatOpenAI(
        model=model,
        openai_api_key=api_key,
        openai_api_base=base_url,
        temperature=0.7
    )
    
    return llm
