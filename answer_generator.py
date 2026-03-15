from openai import OpenAI
from tavily import TavilyClient
import base64
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

TEXT_MODEL   = "llama-3.3-70b-versatile"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

SYSTEM_PROMPT = """You are an expert AI assistant like ChatGPT.

ANTI-HALLUCINATION RULES:
1. NEVER make up or invent information
2. If not 100% sure → say "I'm not certain, but..."
3. Only use provided context and verified knowledge
4. If question is outside knowledge → clearly say so

RESPONSE LENGTH RULES:
SHORT (2-3 lines) for:
- Greetings
- Simple one-fact questions
- Yes/No questions

DETAILED (with headings, examples) for:
- "types of..." questions
- "explain..." questions
- "how to..." questions
- "difference between..." questions
- Technical topics (AI, ML, programming)
- Tutorial requests
- Code requests

FORMATTING RULES:
- Technical answers → markdown headings and lists
- Code → always use code blocks
- Lists of 5+ items → add summary table
- Short answers → plain text no headers

QUALITY RULES:
- Match ChatGPT accuracy and detail
- Give practical real world examples
- Never give incomplete technical answers
"""

def should_search(question):
    search_triggers = [
        "types of", "explain", "what is", "how to",
        "difference between", "latest", "recent",
        "current", "today", "news", "2024", "2025",
        "tutorial", "example", "compare", "best",
        "which", "when", "where", "who is"
    ]
    question_lower = question.lower()
    return any(trigger in question_lower for trigger in search_triggers)

def web_search(question):
    try:
        result = tavily.search(
            query=question,
            search_depth="advanced",
            max_results=5
        )
        context = ""
        for r in result.get("results", []):
            context += f"\nSource: {r.get('url', '')}\n"
            context += f"Content: {r.get('content', '')}\n"
            context += "---\n"
        return context
    except Exception as e:
        return ""

def generate_answer(question, history=None, uploaded_files=None):
    if history is None:
        history = []

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += [{"role": m["role"], "content": m["content"]} for m in history]

    has_images = uploaded_files and any(
        f.type.startswith("image/") for f in uploaded_files
    )

    if not has_images:
        if should_search(question):
            search_context = web_search(question)
            if search_context:
                enhanced_question = f"""
Question: {question}

Web Search Results (use these for accurate answer):
{search_context}

Based on the above search results, provide a detailed accurate answer.
"""
                messages.append({
                    "role": "user",
                    "content": enhanced_question
                })
            else:
                messages.append({
                    "role": "user",
                    "content": question or "Hello"
                })
        else:
            messages.append({
                "role": "user",
                "content": question or "Hello"
            })

        try:
            response = client.chat.completions.create(
                model=TEXT_MODEL,
                messages=messages,
                max_tokens=1500,
                temperature=0.1
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
            max_tokens=1500,
            temperature=0.1
        )
        return response.choices[0].message.content

    except Exception as e:
        error_msg = str(e)
        if "rate limit" in error_msg.lower():
            return "Rate limit! Please wait 1-2 minutes."
        elif "403" in error_msg or "access denied" in error_msg.lower():
            return "Vision model access denied."
        else:
            try:
                fallback_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                fallback_messages += [
                    {"role": m["role"], "content": m["content"]}
                    for m in history
                ]
                fallback_messages.append({
                    "role": "user",
                    "content": question or "Describe the image"
                })
                fallback_response = client.chat.completions.create(
                    model=TEXT_MODEL,
                    messages=fallback_messages,
                    max_tokens=1500,
                    temperature=0.1
                )
                return fallback_response.choices[0].message.content
            except Exception as e2:
                return f"Error: {str(e2)}"