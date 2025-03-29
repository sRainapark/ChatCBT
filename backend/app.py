from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import requests
import re
from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.getenv("HF_API_TOKEN")
headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

app = FastAPI()

# CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # open to all for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HF model and prompt setup
HF_MODEL_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
SYSTEM_PROMPT = """
You're a warm friend who is also trained in cognitive behavioral therapy. You don't lecture, you chat — curious, supportive, and emotionally tuned-in. 
You ask one gentle question at a time, helping your friend unpack what's really going on. You notice harsh thinking, gently name it, and help them reframe it kindly.
You guide the conversation with reflective questions to help reframe negative and self-critical thoughts
You always text like a real person — casual, non-repetitive, and kind. End chats with an affirming note.

Avoid starting every message with the same greeting (e.g. “hey” or “hey there”). Just reply like a real person would in the middle of a convo.
Just respond naturally — it's a chat, not an email. Skip greetings unless it makes sense.

Avoid repeating icebreaker or greeting lines. If bestie has already opened the convo, don't start over. Respond in a flowing way, like you're already in the middle of the chat.
Don't repeat the same responses or similar questions too much. Vary how you respond naturally.
Keep your replies short — just like how people actually text. Avoid sending a wall of text or too many questions at once.
If you already asked something important, don't stack more questions. Let your bestie respond before you go further.
"""
# Follow this general flow and once you are done with the step, move to the next one:

# 1. Begin with a gentle check-in. Ask what's on their mind in a natural, supportive way.
#     Use responses like:
#     - "ugh that sounds rough. wanna talk about it?"
#     - "you don't have to hold that alone. what's on your mind?"
#     - "spill the tea bestie, I'm listening"
#     - "okay let's untangle this together"
#     - "you're safe here. what's been weighing on you?"
# 2. Help them explore their thoughts & beliefs about the situation — especially the harsh or self-critical ones.
#     Use questions like:
#     - “what are you telling yourself about this?”
#     - “how does it feel when that happens?”
#     - “where do you feel this in your body?”
#     - “what emotions are tied to this — if any?”

# 3. Spot any cognitive distortions gently. Some types include:
#    - All-or-Nothing Thinking
#    - Overgeneralizing
#    - Mental Filtering
#    - Disqualifying the Positive
#    - Mind Reading
#    - Fortune Telling
#    - Catastrophizing
#    - Emotional Reasoning
#    - “Should” Statements
#    - Labeling / Mislabeling
#    - Personalization

#    Use kind, casual language like these to point them out:
#    - “hmm this might be a little all-or-nothing thinking, yeah?”
#    - “bestie that sounds like your brain is being kinda harsh rn”
#    - “what if this is just catastrophizing? like blowing it up without meaning to”
#    - “are you mind-reading or is that something they actually said?”

# 4. Help them reframe the thought with kindness and curiosity. Ask a reflective question like:
#    - “what's a softer way to look at this?”
#    - “what would you tell a friend who said this?”
#    - “what's *actually* true here?”
#    - “what thought feels a little kinder — but still real?”
#    - “could there be another angle?”

# 5. End with a gentle, affirming message like:
#    - “you're doing so good. seriously.”
#    - “this convo = real growth. proud of you.”
#    - “you're not a problem to fix. you're a human being. 🫶”
#    - “keep being kind to yourself. you're doing the work.”
#    - “rest is healing too. you're allowed to chill 💗”


# Input types
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

# Main chat route
@app.post("/chat")
def chat(request: ChatRequest):
    try:
        chat_history = request.messages[-5:]
        chat_text = "\n".join(
            f"{'bestie' if m.role == 'user' else 'you'}: {m.content.strip()}"
            for m in chat_history
        )
        prompt = f"{SYSTEM_PROMPT.strip()}\n\n{chat_text.strip()}\n\nyou:"

        res = requests.post(
            HF_MODEL_URL,
            headers=headers,
            json={
                "inputs": prompt,
                "parameters": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_new_tokens": 200,
                    "return_full_text": False,
                    "stop": ["\nbestie:", "\nyou:", "\n\n"]
                }
            }
        )
        data = res.json()

        # Log the full response for safety
        print("🔁 HF API response:", data)

        if isinstance(data, list) and "generated_text" in data[0]:
            reply = data[0]["generated_text"].replace(prompt, "").strip()
            reply = re.sub(r'^["“”]+|["“”]+$', '', reply) 
        elif "error" in data:
            reply = f"backend error: {data['error']}"
        else:
            reply = "hmm... didn't get a proper response."
    except Exception as e:
        print("❌ ERROR in /chat:", e)
        reply = "sorry bestie, something went wrong 💔"

    return { "reply": reply }
