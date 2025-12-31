

from openai import OpenAI

client = OpenAI(
    api_key="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", 
    base_url="https://api.groq.com/openai/v1" 
)

def evaluate_answer(question, answer):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  
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
        temperature=0.7,  
        max_tokens=500   
    )
    return response.choices[0].message.content