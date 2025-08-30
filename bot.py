import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Get API keys from Railway Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Your Telegram bot token from Railway
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # OpenAI API key

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello 👋 I'm your AI friend bot! Send me anything and I'll reply 😊")

# Handle normal text messages
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        bot_reply = response["choices"][0]["message"]["content"]
        await update.message.reply_text(bot_reply)

    except Exception as e:
        await update.message.reply_text("Oops 😅 something went wrong.")
        logging.error(e)

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    application.run_polling()

if __name__ == "__main__":
    main()