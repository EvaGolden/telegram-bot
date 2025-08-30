# ai_wrapper.py
import os
import google.generativeai as genai

# Load API key from Railway env variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def normal_ai_response(user_message: str) -> str:
    """
    Sends user input to Gemini and returns the AI's response text.
    """
    try:
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(user_message)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Oops, something went wrong: {e}"
