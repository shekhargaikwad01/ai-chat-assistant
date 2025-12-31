import streamlit as st
from streamlit_mic_recorder import speech_to_text
from answer_generator import generate_answer
import re
from gtts import gTTS
import io
import base64

def play_audio(text):
    try:
        clean_text = re.sub(r'(\*\*|__|\*|_|`|~|#|>|\|)', '', text)
        clean_text = re.sub(r'\n+', '. ', clean_text)
        clean_text = clean_text.strip()

        if not clean_text:
            return

        tts = gTTS(text=clean_text, lang='en', slow=False)  # 'hi' करो हिंदी के लिए
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)

        audio_base64 = base64.b64encode(audio_bytes.read()).decode('utf-8')
        audio_html = f"""
        <audio autoplay="true" style="display:none;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        <script>
            var audio = document.querySelector('audio');
            if (audio) {{
                audio.play().catch(e => console.log("Play issue:", e));
            }}
        </script>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
        st.markdown("🔊 **बोल रहा हूँ... सुनो पूरी बात!**")

    except Exception as e:
        st.error(f"आवाज़ में समस्या: {e}")
        st.caption("इंटरनेट चेक करें।")


# --------------------- Keyword-based Suggestions ---------------------
def get_suggestions(last_question):
    question = last_question.lower()
    if any(word in question for word in ["code", "python", "program", "error", "debug"]):
        return ["इसका code example चाहिए?", "और optimize कैसे करें?", "Common mistakes क्या हैं?"]
    elif any(word in question for word in ["interview", "job", "resume", "question"]):
        return ["अगला question practice करें?", "Answer improve कैसे करें?", "Common tips बताओ"]
    elif any(word in question for word in ["machine learning", "data science", "ai"]):
        return ["Real-world example?", "Best resources कौन से?", "Latest trends क्या हैं?"]
    else:
        return ["और detail में बताओ?", "Example के साथ समझाओ?", "क्या related कुछ और पूछू?"]


# --------------------- Page Setup ---------------------
st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="centered")

# Splash Screen
if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.markdown("""
        <style>
        .big-robot {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        .title {font-size: 3.5rem; margin: 30px 0 10px 0; font-weight: bold;}
        .subtitle {font-size: 1.6rem; margin-bottom: 50px; opacity: 0.9;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="big-robot">', unsafe_allow_html=True)

    try:
        st.image("C:/Users/shekhar/OneDrive/Desktop/chatbot", width=320)
    except:
        st.markdown("<h1 style='font-size:6rem;margin:0;'>🤖</h1>", unsafe_allow_html=True)

    st.markdown("<div class='title'>AI Chat Assistant</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Voice या Text से बात करो • हर जवाब automatic बोलेगा!</div>", unsafe_allow_html=True)

    if st.button("🚀 Tap to Start Chat", use_container_width=True):
        st.session_state.started = True
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------- Main Chat Interface ---------------------
else:
    st.markdown("""
        <h1 style='text-align: center; color: #4CAF50;'>🤖 AI Chat Assistant</h1>
        <p style='text-align: center; color: #666;'>Ask Anything – Voice या Text से! 🔊 हर जवाब बोलेगा</p>
        <hr>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg["content"])
        else:
            # कस्टम रोबोट अवतार + मैसेज
            with st.chat_message("assistant"):
                cols = st.columns([1, 10])
                with cols[0]:
                    try:
                        st.image("robot.png", width=50)  # आपकी robot.png यहाँ दिखेगी
                    except:
                        st.markdown("🤖")
                with cols[1]:
                    st.markdown(msg["content"])

    # Suggestions
    if len(st.session_state.messages) >= 2 and st.session_state.messages[-1]["role"] == "assistant":
        last_question = st.session_state.messages[-2]["content"]
        suggestions = get_suggestions(last_question)
        st.markdown("**💡 Suggested Questions:**")
        cols = st.columns(3)
        for idx, sugg in enumerate(suggestions):
            if cols[idx].button(sugg, use_container_width=True):
                st.session_state.pending_question = sugg
                st.rerun()

    # Voice Input
    st.markdown("**🎤 Voice Input**")
    voice_key = f"voice_{len(st.session_state.messages)}"
    text_from_voice = speech_to_text(
        language="en",
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹️ Stop Recording",
        just_once=False,
        use_container_width=True,
        key=voice_key
    )

    text_input = st.chat_input("Type your message here...")

    if "pending_question" in st.session_state:
        question = st.session_state.pending_question
        del st.session_state.pending_question
    else:
        question = text_from_voice or text_input

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user", avatar="👤"):
            st.markdown(question)

        # असिस्टेंट का जवाब + कस्टम अवतार
        with st.chat_message("assistant"):
            cols = st.columns([1, 10])
            with cols[0]:
                try:
                    st.image("robot.png", width=50)
                except:
                    st.markdown("🤖")
            with cols[1]:
                with st.spinner("🤔 सोच रहा हूँ..."):
                    history = [m for m in st.session_state.messages[:-1]]
                    response = generate_answer(question, history)
                st.markdown(response)
                play_audio(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Options")
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")
        st.caption("🔊 आवाज़ पूरी सुनी जाएगी – बीच में सवाल पूछो तो भी नहीं रुकेगी!")
        st.caption("🤖 आपका कस्टम रोबोट अवतार हर मैसेज में दिख रहा है!")
        st.caption("🇮🇳 हिंदी आवाज़: play_audio में lang='hi' कर दो")
        st.caption("🚀 Powered by Groq + Llama-3.3-70B")