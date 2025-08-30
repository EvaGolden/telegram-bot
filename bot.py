import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import google.generativeai as genai

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Set up Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def start(update, context):
    update.message.reply_text("Hey 👋 I’m your Gemini-powered friend bot. Talk to me!")

def chat(update, context):
    user_message = update.message.text
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_message)
        reply = response.text if response.text else "😅 I couldn’t generate a reply."
        update.message.reply_text(reply)
    except Exception as e:
        update.message.reply_text("⚠️ Error: " + str(e))

def main():
    updater = Updater(os.getenv("TELEGRAM_TOKEN"), use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()