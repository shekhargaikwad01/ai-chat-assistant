




# # answer_generator.py

# from openai import OpenAI

# Groq client setup (same as your existing code)
# client = OpenAI(
#     api_key="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",  # Replace if needed, but keep secure!
#     base_url="https://api.groq.com/openai/v1"
# )

# def generate_answer(question, history=None):
#     """
#     Generate an answer to the user's question using the AI model.
#     - question: The user's query (str).
#     - history: Optional list of previous messages for context (list of dicts).
#     """
#     # Build messages with history for contextual responses
#     messages = [
#         {"role": "system", "content": "You are a helpful AI assistant. Provide accurate, concise answers to general knowledge or technical questions. Be educational and clear."}
#     ]
    
#     if history:
#         messages.extend(history)
    
#     messages.append({"role": "user", "content": question})
    
#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",  # Smart model for diverse questions
#         messages=messages,
#         temperature=0.7,  # Balanced: factual but engaging
#         max_tokens=500    # Limit to ~300-400 words for brevity
#     )
#     return response.choices[0].message.content.strip()












# import base64
# from openai import OpenAI
# import streamlit as st

# # Groq Client (आपकी key सही है)
# client = OpenAI(
#     api_key="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",
#     base_url="https://api.groq.com/openai/v1"
# )

# # Latest best text model (replacement of old llama3-70b)
# TEXT_MODEL = "llama-3.3-70b-versatile"  # सबसे अच्छा और fast

# # Alternative fast models (अगर ऊपर वाला busy हो)
# # "llama-3.1-8b-instant"  # छोटा और super fast
# # "gemma2-9b-it"         # अगर available हो

# def generate_answer(question, history=None, uploaded_files=None):
#     if history is None:
#         history = []

#     messages = [{"role": m["role"], "content": m["content"]} for m in history]

#     # User content
#     content = question or "Hello!"

#     # अगर image uploaded है तो warn करें (vision support नहीं अभी)
#     if uploaded_files:
#         st.warning("📎 Image uploaded है, लेकिन अभी Groq पर vision support नहीं है। AI सिर्फ text पर जवाब देगा।")
#         content = f"{content}\n(User ने image upload की है, लेकिन मैं उसे देख नहीं सकता।)"

#     messages.append({"role": "user", "content": content})

#     try:
#         response = client.chat.completions.create(
#             model=TEXT_MODEL,
#             messages=messages,
#             max_tokens=1000,
#             temperature=0.7
#         )
#         return response.choices[0].message.content

#     except Exception as e:
#         return f"Error: {str(e)} (Internet या API limit check करें)"












# import base64
# from openai import OpenAI
# import streamlit as st
# import time  # Retry के लिए

# # Groq Client (आपकी key)
# client = OpenAI(
#     api_key="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",
#     base_url="https://api.groq.com/openai/v1"
# )

# # Latest best text model (2025 end)
# TEXT_MODEL = "llama-3.3-70b-versatile"  # Super fast & intelligent

# def generate_answer(question, history=None, uploaded_files=None):
#     if history is None:
#         history = []

#     messages = [{"role": m["role"], "content": m["content"]} for m in history]

#     user_content = question or "Hello!"

#     if uploaded_files:
#         st.warning("📎 आपने image/video upload की है! दिख तो रही है chat में, लेकिन Groq अभी images को समझ नहीं सकता (vision support नहीं है)। मैं सिर्फ text पर जवाब दूंगा। Vision के लिए GPT-4o best है।")
#         user_content = f"{user_content}\n\n(Note: User ने image upload की है, लेकिन मैं उसे analyze नहीं कर सकता।)"

#     messages.append({"role": "user", "content": user_content})

#     # Retry logic connection error के लिए (3 tries)
#     for attempt in range(3):
#         try:
#             response = client.chat.completions.create(
#                 model=TEXT_MODEL,
#                 messages=messages,
#                 max_tokens=1000,
#                 temperature=0.7
#             )
#             return response.choices[0].message.content

#         except Exception as e:
#             error_str = str(e).lower()
#             if "connection" in error_str or "timeout" in error_str:
#                 st.warning(f"🌐 Connection issue (attempt {attempt+1}/3). Retrying in 2 seconds...")
#                 time.sleep(2)
#                 continue
#             elif "rate limit" in error_str:
#                 return "🚫 Rate limit hit हो गई (Groq free tier limit)। 1-2 minute wait करें और फिर try करें।"
#             else:
#                 return f"Error: {str(e)}. Internet या API status check करें: https://status.groq.com"

#     return "❌ Multiple connection errors. Internet check करें या बाद में try करें।"













# import base64
# from openai import OpenAI
# import streamlit as st

# # OpenAI Client (अपनी real key डालो)
# client = OpenAI(
#     api_key="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",
#     base_url="https://api.groq.com/openai/v1"
# )


# def generate_answer(question, history=None, uploaded_files=None):
#     if history is None:
#         history = []

#     messages = [{"role": m["role"], "content": m["content"]} for m in history]

#     # User content list (multimodal के लिए)
#     content = []

#     # Text add करो
#     default_prompt = "इस image/video को Hindi या English में detail से describe करो। अगर सवाल है तो उसका जवाब दो।"
#     if question:
#         content.append({"type": "text", "text": question})
#     else:
#         content.append({"type": "text", "text": default_prompt})

#     # Images add करो
#     if uploaded_files:
#         for file in uploaded_files:
#             if file.type.startswith("image/"):
#                 file.seek(0)  # Reset pointer
#                 file_bytes = file.read()
#                 base64_image = base64.b64encode(file_bytes).decode('utf-8')
#                 content.append({
#                     "type": "image_url",
#                     "image_url": {
#                         "url": f"data:{file.type};base64,{base64_image}"
#                     }
#                 })

#     messages.append({"role": "user", "content": content})

#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o",  # Best vision model (fast + accurate)
#             messages=messages,
#             max_tokens=1000,
#             temperature=0.7
#         )
#         return response.choices[0].message.content

#     except Exception as e:
#         return f"Error: {str(e)} (API key या internet check करें)"







###################################################
# answer_generator.py (Updated with Vision Support using latest OpenAI model)

# answer_generator.py
# Groq के साथ fast text chat (आपकी API key के साथ)

# from openai import OpenAI
# import streamlit as st
# import time

# # आपकी Groq API key (सही है और काम कर रही है)
# client = OpenAI(
#     api_key="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",
#     base_url="https://api.groq.com/openai/v1"
# )

# # Latest best Groq model (December 2025)
# TEXT_MODEL = "llama-3.3-70b-versatile"  # सबसे तेज़ और intelligent

# def generate_answer(question, history=None, uploaded_files=None):
#     """
#     AI से जवाब generate करता है।
#     - question: user का text
#     - history: previous messages
#     - uploaded_files: uploaded images/videos (अभी सिर्फ display के लिए)
#     """
#     if history is None:
#         history = []

#     # History को messages format में convert करो
#     messages = [{"role": m["role"], "content": m["content"]} for m in history]

#     # User का current message
#     user_content = question or "नमस्ते! आप कैसे मदद कर सकते हैं?"

#     # अगर image upload हुई है तो user को inform करो (vision नहीं है अभी)
#     if uploaded_files:
#         image_count = sum(1 for f in uploaded_files if f.type.startswith("image/"))
#         video_count = len(uploaded_files) - image_count
        
#         media_info = []
#         if image_count:
#             media_info.append(f"{image_count} image")
#         if video_count:
#             media_info.append(f"{video_count} video")
        
#         media_str = " और ".join(media_info) if media_info else "media"
        
#         st.warning(f"📎 आपने {media_str} upload की है! दिख तो रही है chat में, लेकिन अभी Groq images को समझ नहीं सकता। मैं सिर्फ text पर जवाब दूंगा।")
        
#         user_content = f"{user_content}\n\n(नोट: User ने {media_str} upload की है, लेकिन मैं उसे analyze नहीं कर सकता।)"

#     messages.append({"role": "user", "content": user_content})

#     # API call with retry (connection error के लिए)
#     for attempt in range(3):
#         try:
#             response = client.chat.completions.create(
#                 model=TEXT_MODEL,
#                 messages=messages,
#                 max_tokens=1000,
#                 temperature=0.7
#             )
#             return response.choices[0].message.content.strip()

#         except Exception as e:
#             error_str = str(e).lower()
#             if "connection" in error_str or "timeout" in error_str:
#                 if attempt < 2:
#                     st.warning(f"🌐 Connection issue... Retrying ({attempt + 2}/3)...")
#                     time.sleep(2)
#                     continue
#                 else:
#                     return "❌ Connection problem बार-बार आ रही है। Internet check करें या थोड़ी देर बाद try करें।"
#             elif "rate limit" in error_str:
#                 return "🚫 Rate limit hit हो गई (बहुत requests भेजीं)। 1-2 minute wait करें।"
#             else:
#                 return f"Error: {str(e)}"

#     return "कुछ गलत हो गया। बाद में try करें।"



###################*************************************$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$###########



# answer_generator.py - Groq with Vision Support (Llama 4 Multimodal)

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