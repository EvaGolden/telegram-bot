# bot.py
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from ai_wrapper import normal_ai_response

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update, context):
    await update.message.reply_text("🤖 Alexi is online! Type something to chat.")

async def chat(update, context):
    user_message = update.message.text
    reply = normal_ai_response(user_message)
    await update.message.reply_text(reply)

def run_bot():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    run_bot()
