from openai import OpenAI
import streamlit as st
import base64
import time

# आपकी Groq API key
client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

# Vision models (text + image दोनों support करते हैं)
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"  # Fast & good
# ALTERNATIVE: "meta-llama/llama-4-maverick-17b-128e-instruct"  # Better quality

def generate_answer(question, history=None, uploaded_files=None):
    if history is None:
        history = []

    messages = [{"role": m["role"], "content": m["content"]} for m in history]

    # User content (multimodal format)
    content = []

    # Default prompt अगर सिर्फ image हो
    default_prompt = "इस image को Hindi या English में detail से describe करो। क्या दिख रहा है, objects, colors, background, text सब बताओ।"
    if question:
        content.append({"type": "text", "text": question})
    else:
        content.append({"type": "text", "text": default_prompt})

    # Add images
    if uploaded_files:
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

    # Fallback text model अगर vision fail हो (rare)
    try:
        response = client.chat.completions.create(
            model=VISION_MODEL,
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        error_msg = str(e)
        if "rate limit" in error_msg.lower():
            return "🚫 Rate limit hit! 1-2 minute wait करें।"
        elif "connection" in error_msg.lower():
            return "🌐 Connection issue। Internet check करें या retry करें।"
        else:
            st.warning("Vision model में issue। Text-only fallback use कर रहा हूँ...")
            # Fallback to fast text model
            try:
                fallback_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": question or "Describe the uploaded image"}],
                    max_tokens=500
                )
                return fallback_response.choices[0].message.content
            except:
                return f"Error: {error_msg}"
