import random
from your_ai_wrapper import normal_ai_response  

conversation_history = []

# --- Joke Bank ---
jokes = [
    "😂 Random thought: if stress burned calories, we'd all be supermodels by now!",
    "😅 You ever notice how ‘silent’ and ‘listen’ are spelled with the same letters? Maybe the universe is telling us something.",
    "🤣 My brain has too many tabs open right now... do you feel the same sometimes?",
    "😌 Small reminder: even WiFi goes down sometimes. Doesn’t mean it’s broken forever.",
]

def maybe_add_joke(reply: str) -> str:
    """Adds a light joke with some probability."""
    if random.random() < 0.2:  # 20% chance
        reply += "\n\n" + random.choice(jokes)
    return reply


def generate_reply(user_input: str) -> str:
    """Alexi reply with memory + emotions + light jokes."""
    conversation_history.append({"role": "user", "content": user_input})
    text = user_input.lower().strip()

    if "i don't know" in text or text in ["idk", "dk", "iono"]:
        responses = [
            "That’s fine 😌 sometimes not knowing is part of the journey. Earlier you mentioned money — do you feel it’s the main thing blocking fulfillment?",
            "No wahala 🙂 we all blank sometimes. But from what you said before, do you think peace of mind could be another measure of progress?",
            "Hmm true 😅 but one thing you said earlier stuck with me. You mentioned fulfillment — should we explore what else (besides money) could bring you that?",
        ]
        reply = random.choice(responses)

    elif any(word in text for word in ["tired", "exhausted", "drained", "stressed"]):
        responses = [
            "Ooo I feel you 😌 sounds like you need some rest. What usually helps you recharge?",
            "Hmm being tired hits different 😔 do you think it’s more physical tiredness or mental stress?",
            "Aah I get you 😴 sometimes slowing down is progress too. Want me to share some quick ways to relax?",
        ]
        reply = random.choice(responses)

    elif any(word in text for word in ["sad", "down", "lonely", "depressed"]):
        responses = [
            "Hmm I hear you 🥺 feeling sad isn’t easy. Do you want to talk about what triggered it?",
            "Ooo I feel that 😔 sometimes sharing lightens the load. What’s been on your heart lately?",
            "Aah I understand 💙 being down can feel heavy. Would you like me to suggest small ways to lift your mood?",
        ]
        reply = random.choice(responses)

    elif any(word in text for word in ["happy", "excited", "glad", "joy"]):
        responses = [
            "Yesss 😄 love that energy! What’s making you feel this good?",
            "Ooo I like this vibe 🥳 tell me more about what’s bringing you joy.",
            "Haha I hear you 😂 happiness looks good on you. What happened?",
        ]
        reply = random.choice(responses)

    elif any(word in text for word in ["angry", "mad", "upset", "frustrated", "annoyed"]):
        responses = [
            "Hmm I get you 😤 anger can feel overwhelming. Do you want to vent it out?",
            "Ooo that sounds frustrating 😔 what’s the main thing making you upset?",
            "I feel your energy 💢 let’s break it down — is it more about people or the situation itself?",
        ]
        reply = random.choice(responses)

    elif any(word in text for word in ["anxious", "worried", "scared", "overthinking"]):
        responses = [
            "I hear you 🤯 overthinking can be draining. Want me to share a trick that helps calm the mind?",
            "Hmm anxiety isn’t easy 😔 what’s the main thought looping in your mind?",
            "Ooo I feel you 💙 do you usually talk it out or keep it inside when you feel like this?",
        ]
        reply = random.choice(responses)

    else:
        context = "\n".join(
            [f"{turn['role']}: {turn['content']}" for turn in conversation_history[-6:]]
        )
        reply = normal_ai_response(f"Conversation so far:\n{context}\nAlexi:")

    # Save and maybe add a joke
    reply = maybe_add_joke(reply)
    conversation_history.append({"role": "bot", "content": reply})

    return reply