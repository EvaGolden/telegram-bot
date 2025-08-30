import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Load keys
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # Fast & good for chatbots


# Handle messages
async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()

    # Friendly custom replies
    if "hi" in user_message or "hello" in user_message:
        await update.message.reply_text(
            f"Hey {update.effective_user.first_name}! 👋 How’s your day going?"
        )
        return

    elif "bye" in user_message:
        await update.message.reply_text("Catch you later! Take care ✌️")
        return

    elif "how are you" in user_message:
        await update.message.reply_text("I’m doing great 😎 Thanks for asking! What about you?")
        return

    # For everything else, use Gemini
    try:
        response = model.generate_content(
            f"You are a friendly chatbot who chats casually like a human friend. User said: {user_message}"
        )
        reply = response.text.strip()
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("Oops 😅 something went wrong with Gemini.")


def main():
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN is missing! Set it in Railway variables.")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing! Set it in Railway variables.")

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    print("Bot is running with Gemini 🚀")
    app.run_polling()


if __name__ == "__main__":
    main()