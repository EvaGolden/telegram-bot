# ai_wrapper.py
from google import genai

# Initialize client with your API key
client = genai.Client(api_key="YOUR_API_KEY_HERE")

def normal_ai_response(user_message: str) -> str:
    """
    Sends user input to Gemini and returns the AI's response text.
    """
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",   # You can change to "gemini-1.5-pro" if you have access
            contents=user_message
        )
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Oops, something went wrong: {e}"