import streamlit as st
from answer_generator import generate_answer
from database import load_all_chats, save_chat, delete_chat, rename_chat
import re
import edge_tts
import asyncio
import io
import base64
import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

load_dotenv()

groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# ── Session State initialize ──────────────────────
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "next_chat_counter" not in st.session_state:
    st.session_state.next_chat_counter = 1
if "rename_mode" not in st.session_state:
    st.session_state.rename_mode = None
if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = None
if "db_loaded" not in st.session_state:
    st.session_state.db_loaded = False

# ── Load from PostgreSQL ──────────────────────────
def load_chat_history():
    try:
        st.session_state.all_chats = load_all_chats()
        if st.session_state.all_chats:
            counter_ids = [
                int(k.split("_")[1])
                for k in st.session_state.all_chats.keys()
                if k.startswith("chat_") and k.split("_")[1].isdigit()
            ]
            st.session_state.next_chat_counter = max(counter_ids) + 1 if counter_ids else 1
        st.session_state.db_loaded = True
    except Exception as e:
        st.error(f"Database connection error: {e}")
        st.session_state.all_chats = {}
        st.session_state.db_loaded = False

# ── Save current chat to PostgreSQL ──────────────
def save_chat_history():
    try:
        chat = st.session_state.all_chats[st.session_state.current_chat_id]
        save_chat(
            chat_id=st.session_state.current_chat_id,
            title=chat.get("title", "New Chat"),
            messages=chat.get("messages", []),
            last_updated=chat.get("last_updated")
        )
    except Exception as e:
        st.error(f"Save error: {e}")

if not st.session_state.db_loaded:
    load_chat_history()

# Auto-load most recent chat or create fresh one
if st.session_state.current_chat_id not in st.session_state.all_chats:
    if st.session_state.all_chats:
        latest_id = max(
            st.session_state.all_chats.keys(),
            key=lambda k: st.session_state.all_chats[k].get("last_updated", "1970-01-01T00:00:00")
        )
        st.session_state.current_chat_id = latest_id
    else:
        new_id = f"chat_{st.session_state.next_chat_counter}"
        st.session_state.all_chats[new_id] = {
            "title": "New Chat",
            "messages": [],
            "last_updated": datetime.now().isoformat()
        }
        st.session_state.current_chat_id = new_id
        st.session_state.next_chat_counter += 1

current_messages = st.session_state.all_chats[st.session_state.current_chat_id]["messages"]
current_chat = st.session_state.all_chats[st.session_state.current_chat_id]

# ── TTS ──────────────────────────────────────────

async def get_edge_audio(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    audio_bytes = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes.write(chunk["data"])
    audio_bytes.seek(0)
    return audio_bytes.getvalue()

def play_audio(text):
    try:
        clean_text = re.sub(r'(\*\*|__|\*|_|`|~|#|>|\|)', '', text)
        clean_text = re.sub(r'\n+', '. ', clean_text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        if not clean_text:
            return
        devanagari_count = sum(1 for c in clean_text if '\u0900' <= c <= '\u097F')
        devanagari_ratio = devanagari_count / len(clean_text) if clean_text else 0
        if devanagari_ratio > 0.3:
            primary_voice = "hi-IN-SwatiNeural"
            fallback_voice = "hi-IN-MadhurNeural"
            voice_display = "Hindi (Swati)"
        else:
            primary_voice = "en-IN-NeerjaNeural"
            fallback_voice = None
            voice_display = "English (Neerja)"
        st.caption(f"🔊 Voice: **{voice_display}**")
        try:
            audio_data = asyncio.run(get_edge_audio(clean_text, primary_voice))
        except Exception:
            if fallback_voice:
                audio_data = asyncio.run(get_edge_audio(clean_text, fallback_voice))
            else:
                st.error("Text-to-speech failed")
                return
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        audio_html = f"""
        <audio autoplay style="display:none;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        <script>document.querySelector('audio')?.play().catch(e=>console.log(e))</script>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
        st.markdown("🔊 **Speaking now... Listen till the end!**")
    except Exception as e:
        st.error(f"Audio issue: {e}")

# ── PAGE CONFIG ───────────────────────────────────

st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.block-container { padding-top: 1rem !important; }
header[data-testid="stHeader"] { background: transparent; }
</style>
""", unsafe_allow_html=True)

# ── SPLASH SCREEN ─────────────────────────────────

if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.markdown("""
        <style>
        .welcome {
            display: flex; flex-direction: column; align-items: center;
            justify-content: center; height: 90vh;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: white; text-align: center; padding: 2rem; border-radius: 1rem;
        }
        .wtitle { font-size: 4rem; font-weight: bold;
                  text-shadow: 0 0 20px rgba(0,255,255,0.6); margin: 1rem 0; }
        .wsub   { font-size: 1.6rem; margin: 1rem 0; }
        </style>
        <div class="welcome">
            <h1 class="wtitle">🤖 AI Chat Assistant</h1>
            <p class="wsub">बोलो या लिखो — English या हिंदी में</p>
            <p>शुरू करने के लिए नीचे बटन दबाएँ</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Start Chatting 🚀", type="primary", use_container_width=True, key="start_btn"):
        st.session_state.started = True
        st.rerun()
    st.stop()

# ── SIDEBAR ───────────────────────────────────────

with st.sidebar:
    st.markdown("## 🤖 AI Chat")

    if st.session_state.db_loaded:
        st.success("🟢 PostgreSQL Connected", icon="✅")
    else:
        st.error("🔴 DB Not Connected")

    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        new_id = f"chat_{st.session_state.next_chat_counter}"
        st.session_state.all_chats[new_id] = {
            "title": "New Chat",
            "messages": [],
            "last_updated": datetime.now().isoformat()
        }
        st.session_state.current_chat_id = new_id
        st.session_state.next_chat_counter += 1
        st.rerun()

    st.markdown("---")
    st.markdown("**Your chats**")

    sorted_chats = sorted(
        [
            (cid, c) for cid, c in st.session_state.all_chats.items()
            if c.get("messages") or cid == st.session_state.current_chat_id
        ],
        key=lambda x: x[1].get("last_updated", "1970-01-01T00:00:00"),
        reverse=True
    )

    if not sorted_chats:
        st.caption("No chats yet. Start typing below!")
    else:
        for chat_id, chat in sorted_chats:
            title = chat.get("title", "New Chat")
            is_active = chat_id == st.session_state.current_chat_id

            col_t, col_r, col_d = st.columns([6, 1, 1])

            with col_t:
                btn_type = "secondary" if is_active else "tertiary"
                if st.button(f"💬 {title}", key=f"chat_select_{chat_id}",
                             use_container_width=True, type=btn_type):
                    st.session_state.current_chat_id = chat_id
                    st.session_state.rename_mode = None
                    st.session_state.confirm_delete = None
                    st.rerun()

            with col_r:
                if st.button("✏️", key=f"rename_btn_{chat_id}", help="Rename"):
                    st.session_state.rename_mode = chat_id
                    st.session_state.confirm_delete = None
                    st.rerun()

            with col_d:
                if st.button("🗑️", key=f"delete_btn_{chat_id}", help="Delete"):
                    st.session_state.confirm_delete = chat_id
                    st.session_state.rename_mode = None
                    st.rerun()

            if st.session_state.rename_mode == chat_id:
                new_title_val = st.text_input(
                    "New title", value=title,
                    key=f"rename_input_{chat_id}", max_chars=50
                )
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Save", key=f"rename_save_{chat_id}", type="primary"):
                        if new_title_val.strip():
                            st.session_state.all_chats[chat_id]["title"] = new_title_val.strip()
                            rename_chat(chat_id, new_title_val.strip())
                        st.session_state.rename_mode = None
                        st.rerun()
                with c2:
                    if st.button("Cancel", key=f"rename_cancel_{chat_id}"):
                        st.session_state.rename_mode = None
                        st.rerun()

            if st.session_state.confirm_delete == chat_id:
                st.warning(f"Delete **{title}**?")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Yes", key=f"del_yes_{chat_id}", type="primary"):
                        del st.session_state.all_chats[chat_id]
                        delete_chat(chat_id)
                        if st.session_state.current_chat_id == chat_id:
                            remaining = [
                                c for c in st.session_state.all_chats
                                if st.session_state.all_chats[c].get("messages")
                            ]
                            if remaining:
                                st.session_state.current_chat_id = max(
                                    remaining,
                                    key=lambda k: st.session_state.all_chats[k].get("last_updated", "")
                                )
                            else:
                                new_id = f"chat_{st.session_state.next_chat_counter}"
                                st.session_state.all_chats[new_id] = {
                                    "title": "New Chat", "messages": [],
                                    "last_updated": datetime.now().isoformat()
                                }
                                st.session_state.current_chat_id = new_id
                                st.session_state.next_chat_counter += 1
                        st.session_state.confirm_delete = None
                        st.rerun()
                with c2:
                    if st.button("No", key=f"del_no_{chat_id}"):
                        st.session_state.confirm_delete = None
                        st.rerun()

    st.markdown("---")
    st.caption("Made with Groq + PostgreSQL + Streamlit")

# ── MAIN AREA ─────────────────────────────────────

st.markdown(
    f"<h2 style='margin:0 0 8px 0; padding:0;'>{current_chat.get('title', 'New Chat')}</h2>"
    f"<hr style='margin:0 0 16px 0'>",
    unsafe_allow_html=True
)

# ── CHAT MESSAGES ─────────────────────────────────

for msg in current_messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            if msg.get("content"):
                st.markdown(msg["content"])
            if msg.get("has_files"):
                st.caption("📎 Attachments included")
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# ── INPUT ─────────────────────────────────────────

prompt = st.chat_input(
    "Ask anything... (text or 🎤 voice)",
    accept_file=True,
    file_type=["jpg", "jpeg", "png", "gif", "webp", "mp4", "mov", "avi", "webm"],
    accept_audio=True,
    key=f"input_{st.session_state.current_chat_id}"
)

if prompt:
    user_text = (prompt.text or "").strip()
    uploaded_files = getattr(prompt, "files", [])
    audio_uploaded = getattr(prompt, "audio", None)

    is_voice = audio_uploaded is not None
    display_text = user_text

    if is_voice:
        with st.spinner("🎤 Transcribing voice..."):
            try:
                audio_bytes = audio_uploaded.getvalue()
                audio_io = io.BytesIO(audio_bytes)
                audio_io.name = "voice_input.webm"
                transcription = groq_client.audio.transcriptions.create(
                    model="whisper-large-v3",
                    file=audio_io,
                    response_format="text"
                )
                display_text = transcription.strip()
                st.caption(f"🎤 Recognized: **{display_text}**")
            except Exception as e:
                st.error(f"Voice → Text failed: {str(e)}")
                display_text = "[Voice transcription failed — please type instead]"

    if not display_text and uploaded_files:
        display_text = "कृपया इस मीडिया का वर्णन करें या विश्लेषण करें"

    if display_text or uploaded_files:
        with st.chat_message("user"):
            if display_text:
                st.markdown(display_text)
            for file in uploaded_files:
                if file.type.startswith("image/"):
                    st.image(file, use_column_width=True)
                elif file.type.startswith("video/"):
                    st.video(file)

        current_messages.append({
            "role": "user",
            "content": display_text,
            "has_files": bool(uploaded_files)
        })

        # Auto-title from first message
        if len(current_messages) == 1:
            first_text = display_text or "New Chat"
            short_title = (first_text[:35] + "...") if len(first_text) > 35 else first_text
            current_chat["title"] = short_title

        current_chat["last_updated"] = datetime.now().isoformat()
        save_chat_history()

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                history = [{"role": m["role"], "content": m["content"]} for m in current_messages[:-1]]
                response = generate_answer(display_text, history, uploaded_files)
                if not response.strip():
                    response = "क्षमा करें, जवाब जनरेट नहीं हो सका। कृपया दोबारा कोशिश करें।"
                st.markdown(response)
                if is_voice:
                    words = response.split()
                    spoken = " ".join(words[:45])
                    if len(words) > 45:
                        spoken += " … (ऊपर पूरा जवाब देखें)"
                    play_audio(spoken)

        current_messages.append({"role": "assistant", "content": response})
        current_chat["last_updated"] = datetime.now().isoformat()
        save_chat_history()
        st.rerun()