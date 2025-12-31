# question_generator.py

from openai import OpenAI

client = OpenAI(
    api_key="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",  # तुम्हारी key
    base_url="https://api.groq.com/openai/v1"  # Perfect!
)

def generate_question(role, difficulty="Medium"):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Latest & best Groq model (very smart, gpt-4o-mini से better/better in many tasks)
        # Alternatives (fast & good):
        # "llama3-70b-8192" (classic fast)
        # "mixtral-8x7b-32768" (good reasoning)
        # "gemma2-9b-it" (small & quick)
        # "openai/gpt-oss-120b" (if available – super intelligent)
        messages=[
            {"role": "system", "content": "You are an expert technical interviewer. Ask only ONE clear, relevant interview question."},
            {"role": "user", "content": f"Ask one {difficulty.lower()} level behavioral/technical interview question for a {role} position."}
        ],
        temperature=0.7,   # Optional: some creativity लेकिन consistent
        max_tokens=200     # Optional: short & crisp questions
    )
    return response.choices[0].message.content.strip()  # Clean output (no extra spaces)