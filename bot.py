# bot.py
from ai_wrapper import normal_ai_response

def run_chat():
    print("🤖 Alexi is online! (type 'quit' to exit)\n")

    while True:
        user_message = input("You: ")

        if user_message.lower() in ["quit", "exit", "bye"]:
            print("Alexi: 👋 Alright, take care!")
            break

        # Get AI response
        reply = normal_ai_response(user_message)
        print(f"Alexi: {reply}\n")

if __name__ == "__main__":
    run_chat()