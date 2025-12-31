
# evaluator.py

from openai import OpenAI

# Groq client with correct base_url
client = OpenAI(
    api_key="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",  # तुम्हारी key (safe रखो!)
    base_url="https://api.groq.com/openai/v1"  # ये line add करो – most important!
)

def evaluate_answer(question, answer):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Best free Groq model (smart & fast, gpt-4o-mini से comparable/better in many tasks)
        # Alternatives: "llama3-70b-8192", "mixtral-8x7b-32768", "gemma2-9b-it" (small & fast)
        messages=[
            {"role": "system", "content": "You are a professional interviewer evaluating candidate answers."},
            {"role": "user", "content": f"""
Question: {question}
Candidate Answer: {answer}

Evaluate objectively and provide:
1. Score: X/10 (with justification)
2. Strengths of the answer
3. Areas for improvement
4. Suggested better response (brief)

Be strict but fair.
"""}
        ],
        temperature=0.7,  # Optional: balanced creativity
        max_tokens=500    # Optional: enough for detailed eval
    )
    return response.choices[0].message.content