# ai_wrapper.py
import google.generativeai as genai
import os

# Load API key (set this as an environment variable in your system or hosting platform)
API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini client
genai.configure(api_key=API_KEY)

def normal_ai_response(user_message: str) -> str:
    """
    Sends user input to Gemini and returns the AI's response text.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # Or "gemini-1.5-pro"
        response = model.generate_content(user_message)

        # Gemini responses are structured, so extract text safely
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        elif hasattr(response, "candidates") and response.candidates:
            return response.candidates[0].content.parts[0].text.strip()
        else:
            return "🤔 Sorry, I didn’t quite get that."

    except Exception as e:
        return f"⚠️ Oops, something went wrong: {e}"
