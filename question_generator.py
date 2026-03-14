import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def generate_question(role, difficulty="Medium"):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert technical interviewer. Ask only ONE clear, relevant interview question."},
            {"role": "user", "content": f"Ask one {difficulty.lower()} level behavioral/technical interview question for a {role} position."}
        ],
        temperature=0.7,
        max_tokens=200
    )
    return response.choices[0].message.content.strip()