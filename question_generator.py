
from openai import OpenAI

client = OpenAI(
    api_key="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",  
    base_url="https://api.groq.com/openai/v1"  # Perfect!
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