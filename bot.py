import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Logging
logging.basicConfig(level=logging.INFO)

# Gemini setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# --- Middle Layer: Rewriter ---
def humanize_reply(gemini_text: str, user_text: str) -> str:
    """
    Take Gemini's reply and rewrite it into:
    - short
    - casual/human
    - emojis if emotional
    - end with a question
    """
    user_text = user_text.lower()
    reply = gemini_text.strip()

    # If user expresses tiredness or sadness
    if any(word in user_text for word in ["tired", "exhausted", "sad", "stressed", "down"]):
        return "Aww sorry to hear that 😞. What do you think is making you feel this way?"

    # If user expresses happiness
    if any(word in user_text for word in ["happy", "excited", "good", "great"]):
        return "That’s awesome 😃! What’s making you feel so good today?"

    # If user uses slang / local expressions
    if "fall my hand" in user_text or "wahala" in user_text:
        return "Haha I understand you well 🤣. But tell me, what really happened?"

    # Default fallback: make Gemini’s response shorter
    if len(reply) > 120:  # cut long replies
        reply = reply[:120].rsplit(" ", 1)[0] + "..."

    return f"{reply} 🤔 What do you think?"

# --- Bot Handlers ---
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hey 👋 I’m your buddy bot. How are you feeling today?")

def chat(update: Update, context: CallbackContext):
    user_message = update.message.text

    try:
        # Step 1: Ask Gemini
        response = model.generate_content(user_message)
        gemini_reply = response.text if response and response.text else "Hmm 🤔 I didn’t get that."

        # Step 2: Humanize the reply
        final_reply = humanize_reply(gemini_reply, user_message)

        # Step 3: Send back to user
        update.message.reply_text(final_reply)

    except Exception as e:
        logging.error(f"Error: {e}")
        update.message.reply_text("Oops 😅 something went wrong, try again.")

def main():
    updater = Updater(os.getenv("TELEGRAM_TOKEN"), use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()