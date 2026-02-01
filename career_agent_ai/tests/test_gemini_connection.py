import os
import sys

# Add parent dir to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dotenv import load_dotenv
from career_agent_ai.utils.llm_provider import get_llm

def test_connection():
    load_dotenv()
    print("Testing Gemini Connection...")
    try:
        llm = get_llm()
        llm_type = type(llm).__name__
        print(f"LLM Initialized: {llm_type}")
        
        if "Google" in llm_type or "Gemini" in str(llm):
             print("✅ SUCCESS: Configured to use Google Gemini.")
        else:
             print(f"⚠️ WARNING: Initialized {llm_type}. Check if GOOGLE_API_KEY is properly set.")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_connection()
