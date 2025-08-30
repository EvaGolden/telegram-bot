import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import google.generativeai as genai

# Logging
logging.basicConfig(level=logging.INFO)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hey 👋 I’m your friendly bot. How’s your day going? 😊")

def chat_with_gemini(user_message):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        You are a friendly human-like chatbot 🤖. 
        Rules:
        - Replies must be SHORT (1–3 sentences).
        - Use emojis naturally but not too much.
        - Make it feel like gist, not lecture.
        - End with a small friendly question (unless user says bye/thanks).
        - Reply in casual English (mix small Naija slang if it fits).
        
        User: {user_message}
        Bot:
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logging.error(f"Gemini error: {e}")
        return "Oops 😅 something went wrong."

def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    bot_reply = chat_with_gemini(user_message)
    update.message.reply_text(bot_reply)

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_TOKEN not set in environment variables")

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()