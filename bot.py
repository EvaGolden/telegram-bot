# bot.py
from ai_wrapper import normal_ai_response
from apscheduler.schedulers.background import BackgroundScheduler
import time

# Store conversation history
conversation_history = []

# Function for scheduled check-in
def scheduled_check_in():
    print("\n🤖 Alexi: Hey! Just checking in 😄 How's your day going?\n")

def run_chat():
    print("🤖 Alexi is online! (type 'quit' to exit)\n")

    # Start scheduler for check-ins every 30 minutes
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_check_in, 'interval', minutes=30)
    scheduler.start()

    while True:
        user_message = input("You: ")

        if user_message.lower() in ["quit", "exit", "bye"]:
            print("🤖 Alexi: 👋 Alright, take care! Talk soon 😌")
            scheduler.shutdown()
            break

        # Add user message to history
        conversation_history.append({"role": "user", "content": user_message})

        # Get AI response (using conversation history)
        try:
            reply = normal_ai_response(user_message)
        except Exception as e:
            reply = f"⚠️ Oops, something went wrong: {e}"

        # Add AI reply to history
        conversation_history.append({"role": "assistant", "content": reply})

        # Print reply with emojis
        print(f"🤖 Alexi: {reply} 😄\n")

if __name__ == "__main__":
    run_chat()
