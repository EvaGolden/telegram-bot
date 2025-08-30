import os
import re
import random
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# -------- Logging --------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
log = logging.getLogger("companion-bot")

# -------- API Keys --------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")    # set this in Railway
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")    # set this in Railway

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN is missing (Railway Variables).")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing (Railway Variables).")

# -------- Gemini --------
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-pro")  # solid + widely available

# -------- Intent / Mood Dictionaries --------
EMO_WORDS = {
    "tired": "😞", "exhausted": "😞", "stressed": "😥", "burnt": "😥", "sad": "😔",
    "down": "😔", "lonely": "😔", "anxious": "😟", "angry": "😤", "frustrated": "😤",
    "heartbroken": "💔", "breakup": "💔", "love": "❤️", "crush": "😊", "happy": "😄"
}
SERIOUS_WORDS = [
    "job","work","cv","resume","assignment","exam","deadline","proposal","report",
    "application","interview","school","university","project","finance","budget"
]
CLOSERS = ["bye","goodbye","good night","goodnight","gtg","talk later","thanks","thank you","tnx","appreciate"]

# -------- Small helpers --------
def is_serious(text: str) -> bool:
    t = text.lower()
    return any(w in t for w in SERIOUS_WORDS)

def pick_emoji(text: str) -> str:
    t = text.lower()
    for w, emo in EMO_WORDS.items():
        if w in t:
            return emo
    return ""  # no emoji if none detected

def is_closing(text: str) -> bool:
    t = text.lower()
    return any(c in t for c in CLOSERS)

def short_clean(s: str, max_chars: int = 200) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) > max_chars:
        s = s[:max_chars].rstrip() + "…"
    # enforce max 2 sentences
    parts = re.split(r"(?<=[.!?])\s+", s)
    return " ".join(parts[:2]).strip()

# Build a short, human reply that always invites the user to continue
def craft_reply(user_text: str, gemini_hint: str) -> str:
    serious = is_serious(user_text)
    closing = is_closing(user_text)

    # Base acknowledgement lines (vary by mood)
    emo = pick_emoji(user_text) if not serious else ""
    ack_pool_emotional = [
        f"I feel you {emo}",
        f"Ahh, that’s a lot {emo}",
        f"I get how that can weigh on you {emo}",
        f"Omo, I hear you {emo}",
        f"That sounds tough {emo}",
    ]
    ack_pool_serious = [
        "Got it.",
        "Okay, noted.",
        "Understood.",
        "Makes sense.",
        "I see."
    ]

    # Follow-up questions (guided, short, open)
    followups_emotional = [
        "What do you think started it?",
        "Where do you feel it most—mind or body?",
        "Wanna tell me what happened today?",
        "What’s the part that hurts most?",
        "What would help a little right now?"
    ]
    followups_serious = [
        "What’s the exact goal or deadline?",
        "Where are you stuck exactly?",
        "What have you tried so far?",
        "What’s the toughest part here?",
        "What would a ‘win’ look like for you?"
    ]

    # Choose pools
    ack = random.choice(ack_pool_serious if serious else ack_pool_emotional)

    # Use Gemini only as a hint (never dump it raw)
    hint = short_clean(gemini_hint, max_chars=120)
    # If hint is empty or too generic, ignore it
    if not hint or len(hint.split()) < 3:
        hint = ""

    # Build final text
    if closing:
        # Warm close, no question
        closers = [
            "Anytime. Take care.",
            "Appreciate you. Talk soon.",
            "Alright then. Rest well.",
            "Got you. I’m here when you need me.",
        ]
        return random.choice(closers)

    # Compose: acknowledgement (+ optional tiny hint) + one short follow-up question
    follow = random.choice(followups_serious if serious else followups_emotional)

    if serious:
        base = ack if not hint else f"{ack} {hint}"
        reply = f"{short_clean(base)} {follow}"
    else:
        # add a tiny bit of warmth when casual/emotional
        base = ack if not hint else f"{ack} {hint}"
        reply = f"{short_clean(base)} {follow}"

    # Make sure it's at most 2 sentences. If more, trim.
    parts = re.split(r"(?<=[.!?])\s+", reply)
    if len(parts) > 2:
        reply = " ".join(parts[:2])

    return reply.strip()

# -------- Telegram Handlers --------
def start(update: Update, context: CallbackContext):
    greetings = [
        "Hey 👋 how are you feeling today?",
        "Yo! 👋 what’s on your mind?",
        "Heyy 👋 I’m here. Talk to me.",
    ]
    update.message.reply_text(random.choice(greetings))

def chat(update: Update, context: CallbackContext):
    user_text = update.message.text or ""

    try:
        # We ask Gemini for a VERY short hint (we won’t send it directly)
        prompt = (
            "Give a super short, plain-language gist (1 sentence, <=15 words) of the user's message. "
            "No advice, no lists, no questions—just the gist."
        )
        g = gemini_model.generate_content(f"{prompt}\n\nUser: {user_text}")
        gemini_hint = (g.text or "").strip() if g else ""

    except Exception as e:
        log.warning(f"Gemini hint error: {e}")
        gemini_hint = ""

    # Build the final human-style reply
    final = craft_reply(user_text, gemini_hint)
    update.message.reply_text(final)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

    log.info("Companion bot running ✅")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()