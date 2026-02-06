import os
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.api_core.exceptions import ResourceExhausted

load_dotenv()

class RateLimitedGemini(ChatGoogleGenerativeAI):
    """
    Wrapper around ChatGoogleGenerativeAI to enforce strict rate limit handlng.
    """
    @retry(
        retry=retry_if_exception_type(ResourceExhausted),
        wait=wait_exponential(multiplier=4, min=4, max=60),
        stop=stop_after_attempt(10),
        reraise=True
    )
    def invoke(self, input, config=None, **kwargs):
        """
        Overrides invoke to add retry logic.
        """
        print(f"✨ Invoking Gemini (Attempting request)...")
        return super().invoke(input, config=config, **kwargs)

def get_llm():
    """
    Returns the configured Gemini LLM instance with strict rate limiting.
    """
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")
    
    return RateLimitedGemini(
        model="gemini-flash-lite-latest",
        verbose=True,
        temperature=0,
        google_api_key=api_key,
        max_retries=0 # We handle retries manually
    )
