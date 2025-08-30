# bot.py
from ai_wrapper import normal_ai_response
from apscheduler.schedulers.background import BackgroundScheduler
import time

# ----------------------
# Scheduled tasks
# ----------------------
def scheduled_check_in():
    print("\n🤖 Alexi: Hey! Just checking in 🌟 How's your day going?\n")

# ----------------------
# Main chat loop
# ----------------------
def run_chat():
    print("🤖 Alexi is online! (type 'quit' to exit)\n")

    # Start background scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_check_in, 'interval', minutes=1)  # every 1 min (adjust later)
    scheduler.start()

    try:
        while True:
            user_message = input("You: ")

            if user_message.lower() in ["quit", "exit", "bye"]:
                print("Alexi: 👋 Alright, take care! Stay awesome ✨")
                break

            # AI Response
            reply = normal_ai_response(user_message)

            # Add emoji flair
            enhanced_reply = f"{reply} 😄" if not reply.startswith("⚠️") else reply

            print(f"Alexi: {enhanced_reply}\n")
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nAlexi: 📴 Chat ended.")
    finally:
        scheduler.shutdown()

if __name__ == "__main__":
    run_chat()
