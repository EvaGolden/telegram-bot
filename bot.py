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

    try:
        while True:
            user_message = input("You: ")

            if user_message.lower() in ["quit", "exit", "bye"]:
                print("🤖 Alexi: 👋 Alright, take care! Talk soon 😌")
                break

            # Add user message to history
            conversation_history.append({"role": "user", "content": user_message})

            # Get AI response
            reply = normal_ai_response(user_message)
            print(f"🤖 Alexi: {reply}\n")

            # Add AI reply to history
            conversation_history.append({"role": "ai", "content": reply})

    finally:
        # Make sure scheduler shuts down cleanly
        scheduler.shutdown()

if __name__ == "__main__":
    run_chat()
