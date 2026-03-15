import streamlit as st
from answer_generator import generate_answer
import re
import edge_tts
import asyncio
import io
import base64
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import streamlit.components.v1 as components

load_dotenv()

groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "next_chat_counter" not in st.session_state:
    st.session_state.next_chat_counter = 1
if "rename_mode" not in st.session_state:
    st.session_state.rename_mode = None
if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = None
if "started" not in st.session_state:
    st.session_state.started = False

# ── LocalStorage se history load karo on first load ──
LOAD_JS = """
<script>
(function() {
    try {
        const raw = localStorage.getItem('intellichat_data');
        if (raw) {
            const data = JSON.parse(raw);
            // Send to Streamlit via query param trick
            const url = new URL(window.location.href);
            url.searchParams.set('_lsdata', encodeURIComponent(raw));
            // Store in sessionStorage for Streamlit to read
            sessionStorage.setItem('intellichat_loaded', raw);
        }
    } catch(e) {}
})();
</script>
"""

def init_chat():
    if not st.session_state.all_chats:
        new_id = f"chat_{st.session_state.next_chat_counter}"
        st.session_state.all_chats[new_id] = {
            "title": "New Chat",
            "messages": [],
            "last_updated": datetime.now().isoformat()
        }
        st.session_state.current_chat_id = new_id
        st.session_state.next_chat_counter += 1
    elif st.session_state.current_chat_id not in st.session_state.all_chats:
        latest_id = max(
            st.session_state.all_chats.keys(),
            key=lambda k: st.session_state.all_chats[k].get("last_updated", "")
        )
        st.session_state.current_chat_id = latest_id

init_chat()

current_messages = st.session_state.all_chats[st.session_state.current_chat_id]["messages"]
current_chat = st.session_state.all_chats[st.session_state.current_chat_id]

def save_to_local_storage():
    data = {
        "all_chats": st.session_state.all_chats,
        "next_counter": st.session_state.next_chat_counter
    }
    data_json = json.dumps(data, ensure_ascii=False)
    js_code = f"""
    <script>
    try {{
        localStorage.setItem('intellichat_data', {json.dumps(data_json)});
    }} catch(e) {{
        console.log('Save error:', e);
    }}
    </script>
    """
    components.html(js_code, height=0)

def hide_streamlit_branding():
    components.html("""
    <script>
    function hideElements() {
        document.querySelectorAll('a[href*="streamlit.io"]').forEach(el => el.style.display = 'none');
        document.querySelectorAll('a[href*="github.com"]').forEach(el => el.style.display = 'none');
        const toolbar = document.querySelector('[data-testid="stToolbar"]');
        if (toolbar) toolbar.style.display = 'none';
        const header = document.querySelector('[data-testid="stHeader"]');
        if (header) header.style.display = 'none';
        const footer = document.querySelector('footer');
        if (footer) footer.style.display = 'none';
        document.querySelectorAll('button[kind="header"]').forEach(el => el.style.display = 'none');
        document.querySelectorAll('[data-testid="stActionButtonIcon"]').forEach(el => {
            if (el.closest('button')) el.closest('button').style.display = 'none';
        });
        document.querySelectorAll('[class*="ToolbarActions"]').forEach(el => el.style.display = 'none');
        document.querySelectorAll('[class*="StatusWidget"]').forEach(el => el.style.display = 'none');
        document.querySelectorAll('[class*="viewerBadge"]').forEach(el => el.style.display = 'none');
        document.querySelectorAll('[class*="decoration"]').forEach(el => el.style.display = 'none');
        document.querySelectorAll('[class*="Toolbar"]').forEach(el => el.style.display = 'none');
        document.querySelectorAll('[data-testid="manage-app-button"]').forEach(el => el.style.display = 'none');
        document.querySelectorAll('button[aria-label="Manage app"]').forEach(el => el.style.display = 'none');
        const bottomRight = document.querySelector('.st-emotion-cache-h4xjwg');
        if (bottomRight) bottomRight.style.display = 'none';
        const allFixed = document.querySelectorAll('section[data-testid="stBottom"] button');
        allFixed.forEach(el => el.style.display = 'none');
    }
    hideElements();
    setTimeout(hideElements, 500);
    setTimeout(hideElements, 1000);
    setTimeout(hideElements, 2000);
    setTimeout(hideElements, 3000);
    const observer = new MutationObserver(hideElements);
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """, height=0)

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
        st.markdown("🔊 **Speaking now...**")
    except Exception as e:
        st.error(f"Audio issue: {e}")

st.set_page_config(
    page_title="IntelliChat AI",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important;}
header {visibility: hidden !important;}
[data-testid="stToolbar"] {display: none !important;}
[data-testid="stDecoration"] {display: none !important;}
[data-testid="stStatusWidget"] {display: none !important;}
.viewerBadge_container__1QSob {display: none !important;}
.viewerBadge_link__1S137 {display: none !important;}
#stDecoration {display: none !important;}
button[kind="header"] {display: none !important;}
[data-testid="manage-app-button"] {display: none !important;}
[data-testid="stActionButtonIcon"] {display: none !important;}
.stActionButton {display: none !important;}
div[class*="StatusWidget"] {display: none !important;}
div[class*="ToolbarActions"] {display: none !important;}
div[class*="Toolbar"] {display: none !important;}
.st-emotion-cache-czk5ss {display: none !important;}
.st-emotion-cache-1dp5vir {display: none !important;}
a[href*="streamlit.io"] {display: none !important;}
a[href*="github.com/streamlit"] {display: none !important;}
button[data-testid="baseButton-header"] {display: none !important;}
section[data-testid="stBottom"] button {display: none !important;}
.st-emotion-cache-h4xjwg {display: none !important;}
.block-container {padding: 0 !important; max-width: 100% !important;}
[data-testid="stSidebar"] {background: #F8F7FF !important; border-right: 0.5px solid #E0DEFC !important;}
[data-testid="stSidebar"] > div {padding: 0 !important;}
.sidebar-logo {display: flex; align-items: center; gap: 10px; padding: 20px 16px 16px; border-bottom: 0.5px solid #E0DEFC; margin-bottom: 12px;}
.logo-icons {display: flex; gap: 6px;}
.logo-icon-1 {width: 32px; height: 32px; border-radius: 8px; background: #534AB7; display: flex; align-items: center; justify-content: center;}
.logo-icon-2 {width: 32px; height: 32px; border-radius: 8px; background: #7F77DD; display: flex; align-items: center; justify-content: center;}
.logo-text {font-size: 15px; font-weight: 600; color: #3C3489;}
.chat-item-active {background: #EEEDFE; border: 0.5px solid #AFA9EC; border-radius: 8px; padding: 9px 12px; margin-bottom: 4px;}
.chat-title-active {font-size: 13px; font-weight: 500; color: #3C3489; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;}
.chat-time-active {font-size: 11px; color: #7F77DD; margin-top: 2px;}
.main-header {display: flex; align-items: center; padding: 14px 24px; border-bottom: 0.5px solid #E0DEFC; background: white;}
.header-left {display: flex; align-items: center; gap: 10px;}
.header-icon {width: 34px; height: 34px; border-radius: 8px; background: #534AB7; display: flex; align-items: center; justify-content: center;}
.header-title {font-size: 15px; font-weight: 600; color: #1a1a2e; margin: 0;}
.header-subtitle {font-size: 11px; color: #7F77DD; margin: 0;}
.section-label {font-size: 11px; color: #999; text-transform: uppercase; letter-spacing: 0.5px; padding: 4px 16px 8px;}
.sidebar-divider {border: none; border-top: 0.5px solid #E0DEFC; margin: 8px 16px;}
[data-testid="stChatMessage"] {padding: 4px 24px !important;}
</style>
""", unsafe_allow_html=True)

if not st.session_state.started:
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e) !important; }
    </style>
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:90vh; text-align:center; padding:2rem;">
        <div style="display:flex; gap:12px; margin-bottom:24px;">
            <div style="width:56px; height:56px; border-radius:14px; background:#534AB7; display:flex; align-items:center; justify-content:center;">
                <svg width="30" height="30" viewBox="0 0 24 24" fill="none">
                    <path d="M12 2C9 2 7 4 7 6.5c0 .8.2 1.5.6 2.1C6.1 9.2 5 10.7 5 12.5c0 1.4.6 2.6 1.5 3.5C6.2 16.6 6 17.3 6 18c0 2.2 1.8 4 4 4h4c2.2 0 4-1.8 4-4 0-.7-.2-1.4-.5-2 .9-.9 1.5-2.1 1.5-3.5 0-1.8-1.1-3.3-2.6-4-.4-.6-.6-1.3-.6-2.1C15.8 4 13.8 2 12 2z" stroke="white" stroke-width="1.4" stroke-linecap="round"/>
                    <circle cx="10" cy="13" r="1" fill="white"/>
                    <circle cx="14" cy="13" r="1" fill="white"/>
                    <path d="M10 17c.6.6 1.4 1 2 1s1.4-.4 2-1" stroke="white" stroke-width="1.2" stroke-linecap="round"/>
                </svg>
            </div>
            <div style="width:56px; height:56px; border-radius:14px; background:#7F77DD; display:flex; align-items:center; justify-content:center;">
                <svg width="30" height="30" viewBox="0 0 24 24" fill="none">
                    <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M8 10h8M8 14h5" stroke="white" stroke-width="1.3" stroke-linecap="round"/>
                </svg>
            </div>
        </div>
        <h1 style="font-size:3.5rem; font-weight:700; color:white; margin:0 0 12px; text-shadow:0 0 30px rgba(127,119,221,0.8);">IntelliChat AI</h1>
        <p style="font-size:1.3rem; color:#AFA9EC; margin:0 0 8px;">Ask anything — Voice, Text or Image</p>
        <p style="font-size:1rem; color:#7F77DD; margin:0 0 40px;">Powered by Groq + Tavily Web Search</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Chatting 🚀", type="primary", use_container_width=True, key="start_btn"):
        st.session_state.started = True
        st.rerun()
    hide_streamlit_branding()
    st.stop()

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-icons">
            <div class="logo-icon-1">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                    <path d="M12 2C9 2 7 4 7 6.5c0 .8.2 1.5.6 2.1C6.1 9.2 5 10.7 5 12.5c0 1.4.6 2.6 1.5 3.5C6.2 16.6 6 17.3 6 18c0 2.2 1.8 4 4 4h4c2.2 0 4-1.8 4-4 0-.7-.2-1.4-.5-2 .9-.9 1.5-2.1 1.5-3.5 0-1.8-1.1-3.3-2.6-4-.4-.6-.6-1.3-.6-2.1C15.8 4 13.8 2 12 2z" stroke="white" stroke-width="1.4" stroke-linecap="round"/>
                    <circle cx="10" cy="13" r="1" fill="white"/>
                    <circle cx="14" cy="13" r="1" fill="white"/>
                    <path d="M10 17c.6.6 1.4 1 2 1s1.4-.4 2-1" stroke="white" stroke-width="1.2" stroke-linecap="round"/>
                </svg>
            </div>
            <div class="logo-icon-2">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                    <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M8 10h8M8 14h5" stroke="white" stroke-width="1.3" stroke-linecap="round"/>
                </svg>
            </div>
        </div>
        <span class="logo-text">IntelliChat AI</span>
    </div>
    """, unsafe_allow_html=True)

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

    st.markdown('<div class="section-label">Recent</div>', unsafe_allow_html=True)

    sorted_chats = sorted(
        [
            (cid, c) for cid, c in st.session_state.all_chats.items()
            if c.get("messages") or cid == st.session_state.current_chat_id
        ],
        key=lambda x: x[1].get("last_updated", "1970-01-01T00:00:00"),
        reverse=True
    )

    if not sorted_chats:
        st.caption("No chats yet. Start typing!")
    else:
        for chat_id, chat in sorted_chats:
            title = chat.get("title", "New Chat")
            is_active = chat_id == st.session_state.current_chat_id

            last_updated = chat.get("last_updated", "")
            try:
                dt = datetime.fromisoformat(last_updated)
                now = datetime.now()
                diff = now - dt
                if diff.days == 0:
                    time_str = "Today"
                elif diff.days == 1:
                    time_str = "Yesterday"
                else:
                    time_str = f"{diff.days} days ago"
            except:
                time_str = ""

            col_t, col_r, col_d = st.columns([6, 1, 1])

            with col_t:
                if is_active:
                    st.markdown(f"""
                    <div class="chat-item-active">
                        <div class="chat-title-active">{title}</div>
                        <div class="chat-time-active">{time_str}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    if st.button(f"💬 {title}", key=f"chat_select_{chat_id}",
                                 use_container_width=True):
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
                            save_to_local_storage()
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
                        save_to_local_storage()
                        st.rerun()
                with c2:
                    if st.button("No", key=f"del_no_{chat_id}"):
                        st.session_state.confirm_delete = None
                        st.rerun()

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px; color:#999; text-align:center; padding:8px;">Powered by Groq + Tavily</div>', unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <div class="header-left">
        <div class="header-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                <path d="M12 2C9 2 7 4 7 6.5c0 .8.2 1.5.6 2.1C6.1 9.2 5 10.7 5 12.5c0 1.4.6 2.6 1.5 3.5C6.2 16.6 6 17.3 6 18c0 2.2 1.8 4 4 4h4c2.2 0 4-1.8 4-4 0-.7-.2-1.4-.5-2 .9-.9 1.5-2.1 1.5-3.5 0-1.8-1.1-3.3-2.6-4-.4-.6-.6-1.3-.6-2.1C15.8 4 13.8 2 12 2z" stroke="white" stroke-width="1.4" stroke-linecap="round"/>
                <circle cx="10" cy="13" r="1" fill="white"/>
                <circle cx="14" cy="13" r="1" fill="white"/>
                <path d="M10 17c.6.6 1.4 1 2 1s1.4-.4 2-1" stroke="white" stroke-width="1.2" stroke-linecap="round"/>
            </svg>
        </div>
        <div>
            <p class="header-title">IntelliChat AI</p>
            <p class="header-subtitle">Powered by Groq + Tavily</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

hide_streamlit_branding()

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

prompt = st.chat_input(
    "Ask anything... (text or 🎤 voice)",
    accept_file=True,
    file_type=["jpg", "jpeg", "png", "gif", "webp", "mp4", "mov", "avi", "webm"],
    accept_audio=True,
    key="chat_input"
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
                display_text = "[Voice transcription failed]"

    if not display_text and uploaded_files:
        display_text = "Please describe this media"

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

        if len(current_messages) == 1:
            first_text = display_text or "New Chat"
            short_title = (first_text[:35] + "...") if len(first_text) > 35 else first_text
            current_chat["title"] = short_title

        current_chat["last_updated"] = datetime.now().isoformat()

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                history = [
                    {"role": m["role"], "content": m["content"]}
                    for m in current_messages[:-1]
                ]
                response = generate_answer(display_text, history, uploaded_files)
                if not response.strip():
                    response = "Sorry, could not generate a reply. Please try again."
                st.markdown(response)
                if is_voice:
                    words = response.split()
                    spoken = " ".join(words[:45])
                    if len(words) > 45:
                        spoken += " (see full answer above)"
                    play_audio(spoken)

        current_messages.append({
            "role": "assistant",
            "content": response
        })

        current_chat["last_updated"] = datetime.now().isoformat()
        save_to_local_storage()
        st.rerun()
        