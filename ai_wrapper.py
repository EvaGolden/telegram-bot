from google import genai
import os

# Initialize client with your Google API key from environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Safer than hardcoding
client = genai.Client(api_key=GOOGLE_API_KEY)

def normal_ai_response(user_message: str) -> str:
    """
    Sends user input to Gemini and returns the AI's response text.
    """
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=user_message
        )
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Oops, something went wrong: {e}"