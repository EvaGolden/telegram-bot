# ai_wrapper.py
import os
from google import genai

# Get API key from environment variables
API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

def normal_ai_response(user_message: str) -> str:
    """
    Sends user input to Gemini and returns the AI's response text.
    """
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",   # Change to "gemini-1.5-pro" if needed
            contents=user_message
        )
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Oops, something went wrong: {e}"