import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import google.generativeai as genai

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def chat_with_gemini(user_message):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        You are a supportive, friendly chatbot 🤝.
        Rules:
        - Reply in MAX 2 short sentences.
        - Use emojis if it’s emotional/casual (like chatting with a friend).
        - Skip emojis if it’s serious/formal.
        - Be warm & relatable, not robotic.
        - If user seems sad/tired, show empathy first then ask a gentle follow-up.
        - If user says bye/thanks, reply warmly but don’t ask a follow-up.

        User: {user_message}
        Bot:
        """
        response = model.generate_content(prompt)
        reply = response.text.strip()

        # Safety cut: force short reply
        sentences = reply.split(". ")
        if len(sentences) > 2:
            reply = ". ".join(sentences[:2]) + "."

        return reply

    except Exception as e:
        logger.error(f"Gemini error: {e}")
        return "Oops 😅 something went wrong."

# Telegram bot handlers
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hey 👋 I’m your friendly bot. How are you feeling today?")

def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    reply = chat_with_gemini(user_message)
    update.message.reply_text(reply)

def error(update: Update, context: CallbackContext):
    logger.warning(f"Update {update} caused error {context.error}")

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_TOKEN is missing. Set it in your environment variables.")

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()