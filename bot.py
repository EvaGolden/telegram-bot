import os
import logging
import google.generativeai as genai
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

# Logging for debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Rewrite Gemini response into human-like, short, emoji-friendly reply
def humanize_reply(original, user_message):
    # Make response shorter
    if len(original.split()) > 25:  # If too long, cut it down
        original = " ".join(original.split()[:25]) + "..."

    # Add emojis if emotional
    emojis = {
        "tired": "😞",
        "happy": "😊",
        "sad": "😔",
        "angry": "😡",
        "love": "❤️",
        "stress": "😥",
        "work": "💼",
        "friend": "🤝",
    }

    emoji = ""
    for word, emo in emojis.items():
        if word in user_message.lower():
            emoji = emo
            break

    # Add a reflective question
    followups = [
        "What do you think caused that?",
        "How does that make you feel?",
        "Do you want to talk more about it?",
        "What’s on your mind right now?",
        "How are you coping with it?",
    ]

    import random
    followup = random.choice(followups)

    # Combine into final human-like reply
    return f"{original} {emoji}\n\n{followup}"

# Handle start command
def start(update, context):
    update.message.reply_text("Hey 👋 I’m your companion bot. How are you feeling today?")

# Handle normal messages
def chat(update, context):
    user_message = update.message.text

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_message)

        # Humanize Gemini’s response
        bot_reply = humanize_reply(response.text, user_message)

        update.message.reply_text(bot_reply)

    except Exception as e:
        logging.error(f"Error: {e}")
        update.message.reply_text("Oops 😅 I couldn’t process that. Want to try again?")

def main():
    updater = Updater(os.getenv("TELEGRAM_TOKEN"), use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()