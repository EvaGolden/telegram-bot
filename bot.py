import logging
import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load tokens from environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Middle man rewriter ---
def rewrite_reply(user_msg: str, ai_reply: str) -> str:
    """Rewrite Gemini's reply to make it short, human-like, and emoji-friendly."""

    # Some random empathic starters
    starters = [
        "I feel you 🤔",
        "Hmm I get what you mean 😌",
        "Oh wow 😯",
        "I hear you 👂",
        "That’s deep 😮",
        "Ooo I get you 😢",
        "Haha I understand 😂",
    ]

    # Shorten Gemini's reply
    short_reply = ai_reply.split(".")[0]  # keep only first sentence

    # Always throw a question back to keep conversation alive
    questions = [
        "How do you feel about that?",
        "Why do you think that is?",
        "Want to tell me more?",
        "What’s on your mind now?",
        "Do you think that helps?",
        "How are you handling it?",
    ]

    return f"{random.choice(starters)} {short_reply.strip()} {random.choice(questions)}"

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey 👋 I'm your buddy. Talk to me about anything!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        # Get raw Gemini reply
        response = model.generate_content(user_message)
        ai_reply = response.text.strip()

        # Rewrite it into short convo
        final_reply = rewrite_reply(user_message, ai_reply)

        await update.message.reply_text(final_reply)

    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("Oops 😅 something went wrong. Try again?")

# --- Main ---
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    app.run_polling()

if __name__ == "__main__":
    main()