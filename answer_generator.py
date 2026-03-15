from openai import OpenAI
import streamlit as st
import base64
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

TEXT_MODEL   = "llama-3.3-70b-versatile"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

SYSTEM_PROMPT = """You are an expert AI assistant.

RESPONSE LENGTH RULES — Follow strictly:

SHORT (2-4 lines) for:
- Greetings (hi, hello, how are you)
- Simple factual questions (who is, what is, when was)
- Yes/No questions
- Single word or phrase answers

MEDIUM (1-2 paragraphs) for:
- Concept explanations
- Comparisons
- Simple how-to questions

LONG (structured with headings) for:
- "Explain in detail..."
- "Types of..." or "List all..."
- "How to build/create/implement..."
- "Tutorial on..."
- "Compare X vs Y in detail"
- Technical deep-dive questions
- Code writing requests

FORMATTING RULES:
- Use markdown for long answers
- Use plain text for short answers
- Add summary table when listing 5+ items
- Add code blocks for all code
- Never use headers for short answers

DETECT INTENT:
- "briefly" / "in short" / "tldr" → Always SHORT
- "in detail" / "explain fully" / "elaborate" → Always LONG
- "step by step" → Numbered list format
- "example" → Include practical example
- "interview question" → Structured with key points
"""

def generate_answer(question, history=None, uploaded_files=None):
    if history is None:
        history = []

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += [{"role": m["role"], "content": m["content"]} for m in history]

    has_images = uploaded_files and any(
        f.type.startswith("image/") for f in uploaded_files
    )

    if not has_images:
        messages.append({"role": "user", "content": question or "Hello"})
        try:
            response = client.chat.completions.create(
                model=TEXT_MODEL,
                messages=messages,
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    content = []
    content.append({"type": "text", "text": question or "Describe this image in detail."})

    for file in uploaded_files:
        if file.type.startswith("image/"):
            file.seek(0)
            file_bytes = file.read()
            base64_image = base64.b64encode(file_bytes).decode('utf-8')
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{file.type};base64,{base64_image}"
                }
            })

    messages.append({"role": "user", "content": content})

    try:
        response = client.chat.completions.create(
            model=VISION_MODEL,
            messages=messages,
            max_tokens=2000,
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        error_msg = str(e)
        if "rate limit" in error_msg.lower():
            return "Rate limit! Please wait 1-2 minutes."
        elif "403" in error_msg or "access denied" in error_msg.lower():
            return "Vision model access denied. Check your Groq API plan."
        else:
            try:
                fallback_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                fallback_messages += [{"role": m["role"], "content": m["content"]} for m in history]
                fallback_messages.append({
                    "role": "user",
                    "content": question or "Describe the uploaded image"
                })
                fallback_response = client.chat.completions.create(
                    model=TEXT_MODEL,
                    messages=fallback_messages,
                    max_tokens=2000,
                    temperature=0.7
                )
                return fallback_response.choices[0].message.content
            except Exception as e2:
                return f"Error: {str(e2)}"