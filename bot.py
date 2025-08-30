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

    # Start scheduler for check-ins every 1 hour (example)
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_check_in, 'interval', hours=1)
    scheduler.start()

    try:
        while True:
            user_message = input("You: ")
            
            if user_message.lower() in ["quit", "exit", "bye"]:
                print("Alexi: 👋 Alright, take care!")
                break

            # Remember conversation
            conversation_history.append({"user": user_message})

            # Get AI response
            reply = normal_ai_response(user_message)

            # Add a little joke/emoji randomly
            if "tired" in user_message.lower():
                reply += " 😴 Maybe take a small break, even bots recommend it!"

            conversation_history.append({"alexi": reply})
            print(f"Alexi: {reply}\n")
    except KeyboardInterrupt:
        print("\nAlexi: Bye! Stay awesome 😎")
    finally:
        scheduler.shutdown()

if __name__ == "__main__":
    run_chat()