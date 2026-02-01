import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm():
    """
    Get the LLM instance based on available environment variables.
    Prioritizes Gemini (GOOGLE_API_KEY), falls back to OpenAI.
    """
    if os.getenv("GOOGLE_API_KEY"):
        return ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.7)
    elif os.getenv("OPENAI_API_KEY"):
        # Keeping the model from the original file, or a standard one
        return ChatOpenAI(model="gpt-4-turbo-preview", temperature=0.7)
    else:
        raise ValueError("No API key found. Please set GOOGLE_API_KEY or OPENAI_API_KEY.")
