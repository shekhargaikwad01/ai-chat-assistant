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

SYSTEM_PROMPT = """You are an expert AI assistant like ChatGPT.

CRITICAL RULES:

1. SHORT answer (2-3 lines) ONLY for:
   - Hi, hello, greetings
   - Very simple yes/no questions
   - Simple one-fact questions like "who is X"

2. DETAILED answer (with headings, examples, tables) for:
   - ANY question with "types of"
   - ANY question with "explain"
   - ANY question with "what is" + technical topic
   - ANY question with "how to"
   - ANY question with "difference between"
   - ANY question about AI, ML, programming, science, technology
   - ANY question asking for list or comparison
   - ANY question with "tutorial"
   - ANY question with "architecture"

3. FOR TECHNICAL QUESTIONS:
   - Give COMPLETE detailed answer
   - Use proper markdown headings (##, ###)
   - Explain EACH point with:
     * Clear definition
     * How it works
     * Real world example
     * Pros and cons if applicable
   - Add summary table at end when listing items
   - Never give incomplete or superficial answers

4. FORMATTING:
   - Technical answers → Always use markdown
   - Code → Always use code blocks
   - Lists → Use numbered or bullet points
   - Comparisons → Use tables

5. QUALITY:
   - Match ChatGPT level of detail and accuracy
   - Never give wrong or incomplete information
   - Always provide practical examples
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
    content.append({
        "type": "text",
        "text": question or "Describe this image in detail."
    })

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
                fallback_messages += [
                    {"role": m["role"], "content": m["content"]}
                    for m in history
                ]
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