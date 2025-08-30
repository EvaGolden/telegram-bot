import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import random

# Logging
logging.basicConfig(level=logging.INFO)

# API keys
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Setup Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Store conversations (per user)
chat_history = {}

# Some casual emojis
emojis = ["😅", "😂", "🔥", "✨", "🤔", "🙌", "😎", "🫶", "💯", "🤗"]

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    chat_history[user_id] = []  # reset history when starting
    text = random.choice([
        "Yo! 👋 Wassup?",
        "Heeey 🤗 glad you texted!",
        "Heyyy 😎 what’s good?"
    ])
    await update.message.reply_text(text)

# Chat handler with memory
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_text = update.message.text.strip()

    # Init memory if not set
    if user_id not in chat_history:
        chat_history[user_id] = []

    # Save user msg
    chat_history[user_id].append(f"You: {user_text}")

    # If "hi/bye" do friendly manual response
    if user_text.lower() in ["hi", "hello", "hey"]:
        reply = random.choice([
            "Heyyy 😁 how you doing?",
            "Yo! 🙌 what’s up?",
            "Heeeey 🤗 glad you texted!"
        ])
    elif "bye" in user_text.lower():
        reply = random.choice([
            "Later fam ✌️",
            "Catch you soon 🫶",
            "Take care 🔥"
        ])
    else:
        try:
            # Give Gemini the conversation history
            conversation = "\n".join(chat_history[user_id][-10:])  # last 10 exchanges
            response = model.generate_content(
                f"You're chatting as a friendly human friend. Use emojis casually. "
                f"Here’s the convo so far:\n{conversation}\n\nNow reply to: {user_text}"
            )
            reply = response.text.strip()
        except Exception as e:
            logging.error(e)
            reply = "Bruh my brain glitched 😅 try again."

    # Save bot reply in history
    chat_history[user_id].append(f"Bot: {reply}")

    await update.message.reply_text(reply)

# Main
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    app.run_polling()

if __name__ == "__main__":
    main()