# # import streamlit as st
# # from streamlit_mic_recorder import speech_to_text
# # from answer_generator import generate_answer
# # import re
# # from gtts import gTTS
# # import io

# # # --------------------- TTS using gTTS (Works Locally + Online) ---------------------
# # def play_audio(text):
# #     """
# #     Convert text to speech using gTTS and play it automatically in Streamlit.
# #     Works on local machine and deployed apps.
# #     """
# #     try:
# #         # Clean markdown symbols so they aren't spoken (e.g., *bold*, **headers**)
# #         clean_text = re.sub(r'(\*\*|__|\*|_|`|~|#|>|\|)', '', text)
# #         clean_text = re.sub(r'\n+', '. ', clean_text)  # Replace newlines with pauses
# #         clean_text = clean_text.strip()

# #         if not clean_text:
# #             return

# #         # Generate speech
# #         tts = gTTS(text=clean_text, lang='en', slow=False)  # Change 'en' to 'hi' for Hindi
# #         audio_bytes = io.BytesIO()
# #         tts.write_to_fp(audio_bytes)
# #         audio_bytes.seek(0)

# #         # Play audio automatically
# #         st.audio(audio_bytes, format='audio/mp3', autoplay=True)

# #     except Exception as e:
# #         st.error(f"Speech error: {e}")
# #         st.caption("Tip: Internet required for voice playback.")


# # # --------------------- Keyword-based Suggestions ---------------------
# # def get_suggestions(last_question):
# #     question = last_question.lower()
# #     if any(word in question for word in ["code", "python", "program", "error", "debug"]):
# #         return ["इसका code example चाहिए?", "और optimize कैसे करें?", "Common mistakes क्या हैं?"]
# #     elif any(word in question for word in ["interview", "job", "resume", "question"]):
# #         return ["अगला question practice करें?", "Answer improve कैसे करें?", "Common tips बताओ"]
# #     elif any(word in question for word in ["machine learning", "data science", "ai"]):
# #         return ["Real-world example?", "Best resources कौन से?", "Latest trends क्या हैं?"]
# #     else:
# #         return ["और detail में बताओ?", "Example के साथ समझाओ?", "क्या related कुछ और पूछू?"]


# # # --------------------- Page Setup ---------------------
# # st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="centered")

# # # Splash Screen
# # if "started" not in st.session_state:
# #     st.session_state.started = False

# # if not st.session_state.started:
# #     st.markdown("""
# #         <style>
# #         .big-robot {
# #             display: flex;
# #             flex-direction: column;
# #             align-items: center;
# #             justify-content: center;
# #             height: 100vh;
# #             background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# #             color: white;
# #             text-align: center;
# #             margin: 0;
# #             padding: 0;
# #         }
# #         .title {font-size: 3.5rem; margin: 30px 0 10px 0; font-weight: bold;}
# #         .subtitle {font-size: 1.6rem; margin-bottom: 50px; opacity: 0.9;}
# #         </style>
# #     """, unsafe_allow_html=True)

# #     st.markdown('<div class="big-robot">', unsafe_allow_html=True)

# #     try:
# #         st.image("robot.png", width=320)
# #     except:
# #         st.markdown("<h1 style='font-size:6rem;margin:0;'>🤖</h1>", unsafe_allow_html=True)

# #     st.markdown("<div class='title'>AI Chat Assistant</div>", unsafe_allow_html=True)
# #     st.markdown("<div class='subtitle'>Voice या Text से बात करो • हर जवाब automatic बोलेगा!</div>", unsafe_allow_html=True)

# #     if st.button("🚀 Tap to Start Chat", use_container_width=True):
# #         st.session_state.started = True
# #         st.rerun()

# #     st.markdown("</div>", unsafe_allow_html=True)

# # # --------------------- Main Chat Interface ---------------------
# # else:
# #     st.markdown("""
# #         <h1 style='text-align: center; color: #4CAF50;'>🤖 AI Chat Assistant</h1>
# #         <p style='text-align: center; color: #666;'>Ask Anything – Voice या Text से! 🔊 हर जवाब बोलेगा</p>
# #         <hr>
# #     """, unsafe_allow_html=True)

# #     # Initialize chat history
# #     if "messages" not in st.session_state:
# #         st.session_state.messages = []

# #     # Display previous messages
# #     for msg in st.session_state.messages:
# #         if msg["role"] == "user":
# #             with st.chat_message("user", avatar="👤"):
# #                 st.markdown(msg["content"])
# #         else:
# #             with st.chat_message("assistant", avatar="🤖"):
# #                 st.markdown(msg["content"])

# #     # Show suggestions after AI response
# #     if len(st.session_state.messages) >= 2 and st.session_state.messages[-1]["role"] == "assistant":
# #         last_question = st.session_state.messages[-2]["content"]
# #         suggestions = get_suggestions(last_question)
# #         st.markdown("**💡 Suggested Questions:**")
# #         cols = st.columns(3)
# #         for idx, sugg in enumerate(suggestions):
# #             if cols[idx].button(sugg, use_container_width=True):
# #                 st.session_state.pending_question = sugg
# #                 st.rerun()

# #     # Voice Input
# #     st.markdown("**🎤 Voice Input**")
# #     voice_key = f"voice_{len(st.session_state.messages)}"
# #     text_from_voice = speech_to_text(
# #         language="en",  # Change to "hi" for Hindi if needed
# #         start_prompt="🎤 Start Recording",
# #         stop_prompt="⏹️ Stop Recording",
# #         just_once=False,
# #         use_container_width=True,
# #         key=voice_key
# #     )

# #     # Text Input
# #     text_input = st.chat_input("Type your message here...")

# #     # Determine the question (from suggestion, voice, or text)
# #     if "pending_question" in st.session_state:
# #         question = st.session_state.pending_question
# #         del st.session_state.pending_question
# #     else:
# #         question = text_from_voice or text_input

# #     # Process the question
# #     if question:
# #         # Add user message
# #         st.session_state.messages.append({"role": "user", "content": question})
# #         with st.chat_message("user", avatar="👤"):
# #             st.markdown(question)

# #         # Generate and display AI response
# #         with st.chat_message("assistant", avatar="🤖"):
# #             with st.spinner("🤔 सोच रहा हूँ..."):
# #                 history = [m for m in st.session_state.messages[:-1]]
# #                 response = generate_answer(question, history)
# #             st.markdown(response)
# #             play_audio(response)  # This will now SPEAK the answer!

# #         # Save AI response
# #         st.session_state.messages.append({"role": "assistant", "content": response})

# #     # Sidebar Options
# #     with st.sidebar:
# #         st.header("⚙️ Options")
# #         if st.button("🗑️ Clear Chat"):
# #             st.session_state.messages = []
# #             st.rerun()

# #         st.markdown("---")
# #         # st.caption("🔊 हर जवाब अब voice में बोलेगा (Internet चाहिए)")
# #         st.caption("🌐 Works on mobile & deployed apps too!")
# #         st.caption("🇮🇳 For Hindi voice: change `lang='en'` → `lang='hi'` in code")





# import streamlit as st
# from streamlit_mic_recorder import speech_to_text
# from answer_generator import generate_answer
# import re
# from gtts import gTTS
# import io
# import base64

# # --------------------- TTS with Uninterruptible Audio (Base64 Embed) ---------------------
# def play_audio(text):
#     """
#     टेक्स्ट को आवाज़ में बदलता है और पूरी तरह प्ले करता है,
#     भले ही यूजर तुरंत अगला सवाल पूछ दे। कोई रुकावट नहीं!
#     """
#     try:
#         # Markdown symbols हटाओ ताकि * या # न बोले
#         clean_text = re.sub(r'(\*\*|__|\*|_|`|~|#|>|\|)', '', text)
#         clean_text = re.sub(r'\n+', '. ', clean_text)  # न्यूलाइन को पॉज में बदलो
#         clean_text = clean_text.strip()

#         if not clean_text:
#             return

#         # gTTS से ऑडियो बनाओ (हिंदी चाहो तो lang='hi' करो)
#         tts = gTTS(text=clean_text, lang='en', slow=False)  # 'hi' = हिंदी आवाज़
#         audio_bytes = io.BytesIO()
#         tts.write_to_fp(audio_bytes)
#         audio_bytes.seek(0)

#         # Bytes को Base64 में कन्वर्ट करो
#         audio_base64 = base64.b64encode(audio_bytes.read()).decode('utf-8')

#         # HTML ऑडियो एम्बेड – यह पेज रिफ्रेश होने पर भी चलता रहेगा
#         audio_html = f"""
#         <audio autoplay="true" style="display:none;">
#             <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
#         </audio>
#         <script>
#             var audio = document.querySelector('audio');
#             if (audio) {{
#                 audio.play().catch(e => console.log("Play interrupted:", e));
#             }}
#         </script>
#         """

#         # Streamlit में HTML डालो
#         st.markdown(audio_html, unsafe_allow_html=True)

#         # छोटा इंडिकेटर दिखाओ कि बोल रहा है
#         st.markdown("🔊 **बोल रहा हूँ... सुनो पूरी बात!**")

#     except Exception as e:
#         st.error(f"आवाज़ में समस्या: {e}")
#         st.caption("इंटरनेट कनेक्शन चेक करें। gTTS के लिए नेट चाहिए।")


# # --------------------- Keyword-based Suggestions ---------------------
# def get_suggestions(last_question):
#     question = last_question.lower()
#     if any(word in question for word in ["code", "python", "program", "error", "debug"]):
#         return ["इसका code example चाहिए?", "और optimize कैसे करें?", "Common mistakes क्या हैं?"]
#     elif any(word in question for word in ["interview", "job", "resume", "question"]):
#         return ["अगला question practice करें?", "Answer improve कैसे करें?", "Common tips बताओ"]
#     elif any(word in question for word in ["machine learning", "data science", "ai"]):
#         return ["Real-world example?", "Best resources कौन से?", "Latest trends क्या हैं?"]
#     else:
#         return ["और detail में बताओ?", "Example के साथ समझाओ?", "क्या related कुछ और पूछू?"]


# # --------------------- Page Setup ---------------------
# st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="centered")

# # Splash Screen
# if "started" not in st.session_state:
#     st.session_state.started = False

# if not st.session_state.started:
#     st.markdown("""
#         <style>
#         .big-robot {
#             display: flex;
#             flex-direction: column;
#             align-items: center;
#             justify-content: center;
#             height: 100vh;
#             background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#             color: white;
#             text-align: center;
#             margin: 0;
#             padding: 0;
#         }
#         .title {font-size: 3.5rem; margin: 30px 0 10px 0; font-weight: bold;}
#         .subtitle {font-size: 1.6rem; margin-bottom: 50px; opacity: 0.9;}
#         </style>
#     """, unsafe_allow_html=True)

#     st.markdown('<div class="big-robot">', unsafe_allow_html=True)

#     try:
#         st.image("robot.png", width=320)
#     except:
#         st.markdown("<h1 style='font-size:6rem;margin:0;'>🤖</h1>", unsafe_allow_html=True)

#     st.markdown("<div class='title'>AI Chat Assistant</div>", unsafe_allow_html=True)
#     st.markdown("<div class='subtitle'>Voice या Text से बात करो • हर जवाब automatic बोलेगा!</div>", unsafe_allow_html=True)

#     if st.button("🚀 Tap to Start Chat", use_container_width=True):
#         st.session_state.started = True
#         st.rerun()

#     st.markdown("</div>", unsafe_allow_html=True)

# # --------------------- Main Chat Interface ---------------------
# else:
#     st.markdown("""
#         <h1 style='text-align: center; color: #4CAF50;'>🤖 AI Chat Assistant</h1>
#         <p style='text-align: center; color: #666;'>Ask Anything – Voice या Text से! 🔊 हर जवाब पूरी तरह बोलेगा</p>
#         <hr>
#     """, unsafe_allow_html=True)

#     # Initialize chat history
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Display previous messages
#     for msg in st.session_state.messages:
#         if msg["role"] == "user":
#             with st.chat_message("user", avatar="👤"):
#                 st.markdown(msg["content"])
#         else:
#             with st.chat_message("assistant", avatar="🤖"):
#                 st.markdown(msg["content"])

#     # Show suggestions after AI response
#     if len(st.session_state.messages) >= 2 and st.session_state.messages[-1]["role"] == "assistant":
#         last_question = st.session_state.messages[-2]["content"]
#         suggestions = get_suggestions(last_question)
#         st.markdown("**💡 Suggested Questions:**")
#         cols = st.columns(3)
#         for idx, sugg in enumerate(suggestions):
#             if cols[idx].button(sugg, use_container_width=True):
#                 st.session_state.pending_question = sugg
#                 st.rerun()

#     # Voice Input
#     st.markdown("**🎤 Voice Input**")
#     voice_key = f"voice_{len(st.session_state.messages)}"
#     text_from_voice = speech_to_text(
#         language="en",  # हिंदी के लिए "hi" करो
#         start_prompt="🎤 Start Recording",
#         stop_prompt="⏹️ Stop Recording",
#         just_once=False,
#         use_container_width=True,
#         key=voice_key
#     )

#     # Text Input
#     text_input = st.chat_input("Type your message here...")

#     # Determine the question
#     if "pending_question" in st.session_state:
#         question = st.session_state.pending_question
#         del st.session_state.pending_question
#     else:
#         question = text_from_voice or text_input

#     # Process the question
#     if question:
#         # Add user message
#         st.session_state.messages.append({"role": "user", "content": question})
#         with st.chat_message("user", avatar="👤"):
#             st.markdown(question)

#         # Generate and display AI response
#         with st.chat_message("assistant", avatar="🤖"):
#             with st.spinner("🤔 सोच रहा हूँ..."):
#                 history = [m for m in st.session_state.messages[:-1]]
#                 response = generate_answer(question, history)
#             st.markdown(response)
#             play_audio(response)  # अब आवाज़ पूरी और बिना रुकावट के बोलेगी!

#         # Save AI response
#         st.session_state.messages.append({"role": "assistant", "content": response})

#     # Sidebar Options
#     with st.sidebar:
#         st.header("⚙️ Options")
#         if st.button("🗑️ Clear Chat"):
#             st.session_state.messages = []
#             st.rerun()

#         st.markdown("---")
#         st.caption("🔊 अब आवाज़ पूरी सुनी जाएगी – अगला सवाल बीच में पूछो तो भी नहीं रुकेगी!")
#         st.caption("🌐 लोकल + ऑनलाइन (Streamlit Cloud) दोनों पर काम करता है")
#         st.caption("🇮🇳 हिंदी आवाज़ के लिए: play_audio में lang='hi' कर दो")
#         st.caption("🚀 Model: Llama-3.3-70B (Groq) – बहुत तेज़ और स्मार्ट!")







# import streamlit as st
# from streamlit_mic_recorder import speech_to_text
# from answer_generator import generate_answer
# import re
# from gtts import gTTS
# import io
# import base64
# import os

# # --------------------- रोबोट इमेज का पूरा पाथ ---------------------
# # आपकी दी हुई लोकेशन के अनुसार फुल पाथ
# ROBOT_IMAGE_PATH = r"C:\Users\shekhar\OneDrive\Desktop\AI_Interview_Chatbot\chatbot\robot.png"

# # अगर फाइल नहीं मिली तो fallback इमोजी यूज़ करेंगे
# def get_robot_image(width):
#     try:
#         if os.path.exists(ROBOT_IMAGE_PATH):
#             return st.image(ROBOT_IMAGE_PATH, width=width)
#         else:
#             raise FileNotFoundError
#     except:
#         st.markdown(f"<h1 style='text-align:center;font-size:{width*1.2}px;'>🤖</h1>", unsafe_allow_html=True)


# # --------------------- Uninterruptible TTS ---------------------
# def play_audio(text):
#     try:
#         clean_text = re.sub(r'(\*\*|__|\*|_|`|~|#|>|\|)', '', text)
#         clean_text = re.sub(r'\n+', '. ', clean_text)
#         clean_text = clean_text.strip()

#         if not clean_text:
#             return

#         tts = gTTS(text=clean_text, lang='en', tld='com', slow=False) # हिंदी के लिए 'hi' करो
#         audio_bytes = io.BytesIO()
#         tts.write_to_fp(audio_bytes)
#         audio_bytes.seek(0)

#         audio_base64 = base64.b64encode(audio_bytes.read()).decode('utf-8')
#         audio_html = f"""
#         <audio autoplay="true" style="display:none;">
#             <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
#         </audio>
#         <script>
#             var audio = document.querySelector('audio');
#             if (audio) {{ audio.play().catch(e => console.log(e)); }}
#         </script>
#         """
#         st.markdown(audio_html, unsafe_allow_html=True)
#         st.markdown("🔊 **बोल रहा हूँ... पूरी सुनो!**")

#     except Exception as e:
#         st.error(f"आवाज़ में समस्या: {e}")


# # --------------------- Suggestions ---------------------
# def get_suggestions(last_question):
#     question = last_question.lower()
#     if any(word in question for word in ["code", "python", "program", "error", "debug"]):
#         return ["इसका code example चाहिए?", "और optimize कैसे करें?", "Common mistakes क्या हैं?"]
#     elif any(word in question for word in ["interview", "job", "resume", "question"]):
#         return ["अगला question practice करें?", "Answer improve कैसे करें?", "Common tips बताओ"]
#     elif any(word in question for word in ["machine learning", "data science", "ai"]):
#         return ["Real-world example?", "Best resources कौन से?", "Latest trends क्या हैं?"]
#     else:
#         return ["और detail में बताओ?", "Example के साथ समझाओ?", "क्या related कुछ और पूछू?"]


# # --------------------- Page Setup ---------------------
# st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="centered")

# # Splash Screen - आपकी लोकल इमेज दिखेगी
# if "started" not in st.session_state:
#     st.session_state.started = False

# if not st.session_state.started:
#     st.markdown("""
#         <style>
#         .welcome-container {
#             display: flex;
#             flex-direction: column;
#             align-items: center;
#             justify-content: center;
#             height: 100vh;
#             background: white;
#             text-align: center;
#             padding: 20px;
#         }
#         .title {font-size: 3.5rem; margin: 20px 0 10px 0; font-weight: bold; color: #333;}
#         .subtitle {font-size: 1.6rem; margin: 10px 0 50px 0; color: #555;}
#         </style>
#     """, unsafe_allow_html=True)

#     st.markdown('<div class="welcome-container">', unsafe_allow_html=True)

#     # आपकी फुल लोकल पाथ वाली इमेज यहाँ दिखेगी (बटन से ऊपर)
#     get_robot_image(width=400)

#     st.markdown("<div class='title'>AI Chat Assistant</div>", unsafe_allow_html=True)
#     st.markdown("<div class='subtitle'>Voice या Text से बात करो • हर जवाब automatic बोलेगा!</div>", unsafe_allow_html=True)

#     if st.button("🚀 Tap to Start Chat", use_container_width=True):
#         st.session_state.started = True
#         st.rerun()

#     st.markdown("</div>", unsafe_allow_html=True)

# # --------------------- Main Chat Interface ---------------------
# else:
#     st.markdown("""
#         <h1 style='text-align: center; color: #4CAF50;'>🤖 AI Chat Assistant</h1>
#         <p style='text-align: center; color: #666;'>Ask Anything – Voice या Text से! 🔊 हर जवाब बोलेगा</p>
#         <hr>
#     """, unsafe_allow_html=True)

#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # पुराने मैसेज
#     for msg in st.session_state.messages:
#         if msg["role"] == "user":
#             with st.chat_message("user", avatar="👤"):
#                 st.markdown(msg["content"])
#         else:
#             with st.chat_message("assistant"):
#                 cols = st.columns([1, 12])
#                 with cols[0]:
#                     get_robot_image(width=50)  # चैट में भी वही इमेज
#                 with cols[1]:
#                     st.markdown(msg["content"])

#     # सुझाव
#     if len(st.session_state.messages) >= 2 and st.session_state.messages[-1]["role"] == "assistant":
#         last_question = st.session_state.messages[-2]["content"]
#         suggestions = get_suggestions(last_question)
#         st.markdown("**💡 Suggested Questions:**")
#         cols = st.columns(3)
#         for idx, sugg in enumerate(suggestions):
#             if cols[idx].button(sugg, use_container_width=True):
#                 st.session_state.pending_question = sugg
#                 st.rerun()

#     # वॉइस इनपुट
#     st.markdown("**🎤 Voice Input**")
#     voice_key = f"voice_{len(st.session_state.messages)}"
#     text_from_voice = speech_to_text(
#         language="en",
#         start_prompt="🎤 Start Recording",
#         stop_prompt="⏹️ Stop Recording",
#         just_once=False,
#         use_container_width=True,
#         key=voice_key
#     )

#     text_input = st.chat_input("Type your message here...")

#     if "pending_question" in st.session_state:
#         question = st.session_state.pending_question
#         del st.session_state.pending_question
#     else:
#         question = text_from_voice or text_input

#     if question:
#         st.session_state.messages.append({"role": "user", "content": question})
#         with st.chat_message("user", avatar="👤"):
#             st.markdown(question)

#         with st.chat_message("assistant"):
#             cols = st.columns([1, 12])
#             with cols[0]:
#                 try:
#                     st.image(r"C:\Users\shekhar\OneDrive\Desktop\AI_Interview_Chatbot\chatbot\robot.png", width=50)
#                 except:
#                     st.markdown("🤖")
#             with cols[1]:
#                 with st.spinner("🤔 सोच रहा हूँ..."):
#                     history = [m for m in st.session_state.messages[:-1]]
#                     response = generate_answer(question, history)
#                 st.markdown(response)
#                 play_audio(response)

#         # यह लाइन सही है – कोई समस्या नहीं थी, लेकिन इंडेंटेशन चेक कर लो
#         st.session_state.messages.append({"role": "assistant", "content": response})

#     # साइडबार
#     with st.sidebar:
#         st.header("⚙️ Options")
#         if st.button("🗑️ Clear Chat"):
#             st.session_state.messages = []
#             st.rerun()

#         st.markdown("---")
#         st.caption("🔊 आवाज़ पूरी सुनी जाएगी – रुकावट नहीं!")
#         st.caption("🤖 आपकी इमेज अब सही से दिख रही है!")
#         st.caption("🇮🇳 हिंदी आवाज़ के लिए play_audio में lang='hi' करो")
#         st.caption("🚀 Powered by Groq + Llama-3.3-70B")





# import streamlit as st
# from streamlit_mic_recorder import speech_to_text
# from answer_generator import generate_answer
# import re
# import edge_tts
# import asyncio
# import io
# import base64

# # --------------------- Edge TTS - हाई क्वालिटी आवाज़ ---------------------
# async def get_edge_audio(text, voice="en-IN-NeerjaNeural"):
#     """Edge TTS से ऑडियो bytes जनरेट करता है"""
#     communicate = edge_tts.Communicate(text, voice)
#     audio_bytes = io.BytesIO()
#     async for chunk in communicate.stream():
#         if chunk["type"] == "audio":
#             audio_bytes.write(chunk["data"])
#     audio_bytes.seek(0)
#     return audio_bytes.getvalue()

# def play_audio(text, voice="en-IN-NeerjaNeural"):  # ← यहाँ voice बदल सकते हो
#     try:
#         clean_text = re.sub(r'(\*\*|__|\*|_|`|~|#|>|\|)', '', text)
#         clean_text = re.sub(r'\n+', '. ', clean_text)
#         clean_text = clean_text.strip()

#         if not clean_text:
#             return

#         # Edge TTS से ऑडियो bytes लेते हैं (async को sync में चलाते हैं)
#         audio_data = asyncio.run(get_edge_audio(clean_text, voice))

#         # Base64 embed – आवाज़ पूरी बोलेगी, रुकेगी नहीं!
#         audio_base64 = base64.b64encode(audio_data).decode('utf-8')
#         audio_html = f"""
#         <audio autoplay="true" style="display:none;">
#             <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
#         </audio>
#         <script>
#             var audio = document.querySelector('audio');
#             if (audio) {{ audio.play().catch(e => console.log(e)); }}
#         </script>
#         """
#         st.markdown(audio_html, unsafe_allow_html=True)
#         st.markdown("🔊 **बोल रहा हूँ... पूरी सुनो!**")

#     except Exception as e:
#         st.error(f"आवाज़ में समस्या: {e}")
#         st.caption("इंटरनेट चेक करें।")


# # --------------------- Suggestions ---------------------
# def get_suggestions(last_question):
#     question = last_question.lower()
#     if any(word in question for word in ["code", "python", "program", "error", "debug"]):
#         return ["इसका code example चाहिए?", "और optimize कैसे करें?", "Common mistakes क्या हैं?"]
#     elif any(word in question for word in ["interview", "job", "resume", "question"]):
#         return ["अगला question practice करें?", "Answer improve कैसे करें?", "Common tips बताओ"]
#     elif any(word in question for word in ["machine learning", "data science", "ai"]):
#         return ["Real-world example?", "Best resources कौन से?", "Latest trends क्या हैं?"]
#     else:
#         return ["और detail में बताओ?", "Example के साथ समझाओ?", "क्या related कुछ और पूछू?"]


# # --------------------- Page Setup ---------------------
# st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="centered")

# # Splash Screen
# if "started" not in st.session_state:
#     st.session_state.started = False

# if not st.session_state.started:
#     st.markdown("""
#         <style>
#         .welcome-container {
#             display: flex;
#             flex-direction: column;
#             align-items: center;
#             justify-content: center;
#             height: 100vh;
#             background: white;
#             text-align: center;
#             padding: 20px;
#         }
#         .title {font-size: 3.5rem; margin: 20px 0 10px 0; font-weight: bold; color: #333;}
#         .subtitle {font-size: 1.6rem; margin: 10px 0 50px 0; color: #555;}
#         </style>
#     """, unsafe_allow_html=True)

#     st.markdown('<div class="welcome-container">', unsafe_allow_html=True)

#     try:
#         st.image(r"C:\Users\shekhar\OneDrive\Desktop\AI_Interview_Chatbot\chatbot\robot.png", width=400)
#     except:
#         st.markdown("<h1 style='font-size:10rem;'>🤖</h1>", unsafe_allow_html=True)

#     st.markdown("<div class='title'>AI Chat Assistant</div>", unsafe_allow_html=True)
#     st.markdown("<div class='subtitle'>Voice या Text से बात करो • हर जवाब automatic बोलेगा!</div>", unsafe_allow_html=True)

#     if st.button("🚀 Tap to Start Chat", use_container_width=True):
#         st.session_state.started = True
#         st.rerun()

#     st.markdown("</div>", unsafe_allow_html=True)

# # --------------------- Main Chat Interface ---------------------
# else:
#     st.markdown("""
#         <h1 style='text-align: center; color: #4CAF50;'>🤖 AI Chat Assistant</h1>
#         <p style='text-align: center; color: #666;'>Ask Anything – Voice या Text से! 🔊 हर जवाब बोलेगा</p>
#         <hr>
#     """, unsafe_allow_html=True)

#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     for msg in st.session_state.messages:
#         if msg["role"] == "user":
#             with st.chat_message("user", avatar="👤"):
#                 st.markdown(msg["content"])
#         else:
#             with st.chat_message("assistant"):
#                 cols = st.columns([1, 12])
#                 with cols[0]:
#                     try:
#                         st.image(r"C:\Users\shekhar\OneDrive\Desktop\AI_Interview_Chatbot\chatbot\robot.png", width=50)
#                     except:
#                         st.markdown("🤖")
#                 with cols[1]:
#                     st.markdown(msg["content"])

#     if len(st.session_state.messages) >= 2 and st.session_state.messages[-1]["role"] == "assistant":
#         last_question = st.session_state.messages[-2]["content"]
#         suggestions = get_suggestions(last_question)
#         st.markdown("**💡 Suggested Questions:**")
#         cols = st.columns(3)
#         for idx, sugg in enumerate(suggestions):
#             if cols[idx].button(sugg, use_container_width=True):
#                 st.session_state.pending_question = sugg
#                 st.rerun()

#     st.markdown("**🎤 Voice Input**")
#     voice_key = f"voice_{len(st.session_state.messages)}"
#     text_from_voice = speech_to_text(
#         language="en",
#         start_prompt="🎤 Start Recording",
#         stop_prompt="⏹️ Stop Recording",
#         just_once=False,
#         use_container_width=True,
#         key=voice_key
#     )

#     text_input = st.chat_input("Type your message here...")

#     if "pending_question" in st.session_state:
#         question = st.session_state.pending_question
#         del st.session_state.pending_question
#     else:
#         question = text_from_voice or text_input

#     if question:
#         st.session_state.messages.append({"role": "user", "content": question})
#         with st.chat_message("user", avatar="👤"):
#             st.markdown(question)

#         with st.chat_message("assistant"):
#             cols = st.columns([1, 12])
#             with cols[0]:
#                 try:
#                     st.image(r"C:\Users\shekhar\OneDrive\Desktop\AI_Interview_Chatbot\chatbot\robot.png", width=50)
#                 except:
#                     st.markdown("🤖")
#             with cols[1]:
#                 with st.spinner("🤔 सोच रहा हूँ..."):
#                     history = [m for m in st.session_state.messages[:-1]]
#                     response = generate_answer(question, history)
#                 st.markdown(response)
#                 # ← यहाँ voice बदलो! नीचे दी लिस्ट से चुनो
#                 play_audio(response, voice="en-IN-NeerjaNeural")  # ← सबसे अच्छी इंडियन महिला voice

#         st.session_state.messages.append({"role": "assistant", "content": response})

#     with st.sidebar:
#         st.header("⚙️ Options")
#         st.caption("🔊 अब Microsoft की प्रीमियम voice में बोलेगा!")
#         st.caption("🎤 इंडियन महिला voice: en-IN-NeerjaNeural")
#         st.caption("🇮🇳 हिंदी voice: hi-IN-SwatiNeural")
#         st.caption("🔄 voice बदलने के लिए play_audio में voice=... करो")
#         if st.button("🗑️ Clear Chat"):
#             st.session_state.messages = []
#             st.rerun()












# import streamlit as st
# from streamlit_mic_recorder import speech_to_text
# from answer_generator import generate_answer
# import re
# import edge_tts
# import asyncio
# import io
# import base64

# # --------------------- Edge TTS with Fallback ---------------------
# async def get_edge_audio(text, voice):
#     """Generate audio bytes using Edge TTS"""
#     communicate = edge_tts.Communicate(text, voice)
#     audio_bytes = io.BytesIO()
#     async for chunk in communicate.stream():
#         if chunk["type"] == "audio":
#             audio_bytes.write(chunk["data"])
#     audio_bytes.seek(0)
#     return audio_bytes.getvalue()

# def play_audio(text):
#     try:
#         # Clean text for better TTS
#         clean_text = re.sub(r'(\*\*|__|\*|_|`|~|#|>|\|)', '', text)
#         clean_text = re.sub(r'\n+', '. ', clean_text)
#         clean_text = re.sub(r'\s+', ' ', clean_text)
#         clean_text = clean_text.strip()

#         if not clean_text:
#             return

#         # Detect Hindi content
#         hindi_char_count = sum(1 for c in clean_text if '\u0900' <= c <= '\u097F')
#         total_chars = len(clean_text)
#         hindi_ratio = hindi_char_count / total_chars if total_chars > 0 else 0

#         # Choose voices
#         if hindi_ratio > 0.3:
#             primary_voice = "hi-IN-SwatiNeural"
#             fallback_voice = "hi-IN-MadhurNeural"   # Very reliable fallback
#             voice_display = "Hindi (Swati → Madhur fallback)"
#         else:
#             primary_voice = "en-IN-NeerjaNeural"
#             fallback_voice = None
#             voice_display = "English (Neerja)"

#         st.caption(f"🔊 Trying voice: **{voice_display}**")

#         # Try primary voice first
#         try:
#             audio_data = asyncio.run(get_edge_audio(clean_text, primary_voice))
#             used_voice = primary_voice
#         except Exception as primary_error:
#             st.warning(f"Primary voice failed. Switching to fallback...")
#             if fallback_voice:
#                 try:
#                     audio_data = asyncio.run(get_edge_audio(clean_text, fallback_voice))
#                     used_voice = fallback_voice
#                 except Exception as fallback_error:
#                     st.error(f"All Hindi voices failed: {fallback_error}")
#                     return
#             else:
#                 st.error(f"Voice failed: {primary_error}")
#                 return

#         # Success feedback
#         voice_name = "Hindi (Madhur)" if used_voice == "hi-IN-MadhurNeural" else \
#                      "Hindi (Swati)" if used_voice == "hi-IN-SwatiNeural" else \
#                      "English (Neerja)"
#         st.caption(f"✅ Speaking in: **{voice_name}**")

#         # Embed and play audio
#         audio_base64 = base64.b64encode(audio_data).decode('utf-8')
#         audio_html = f"""
#         <audio autoplay="true" style="display:none;">
#             <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
#         </audio>
#         <script>
#             var audio = document.querySelector('audio');
#             if (audio) {{
#                 audio.play().catch(e => console.log("Play failed:", e));
#             }}
#         </script>
#         """
#         st.markdown(audio_html, unsafe_allow_html=True)
#         st.markdown("🔊 **बोल रहा हूँ... पूरी सुनो!**")

#     except Exception as e:
#         st.error(f"आवाज़ में समस्या: {e}")
#         st.caption("इंटरनेट चेक करें या थोड़ी देर बाद ट्राई करें।")


# # --------------------- Suggestions ---------------------
# def get_suggestions(last_question):
#     question = last_question.lower()
#     if any(word in question for word in ["code", "python", "program", "error", "debug"]):
#         return ["इसका code example चाहिए?", "और optimize कैसे करें?", "Common mistakes क्या हैं?"]
#     elif any(word in question for word in ["interview", "job", "resume", "question"]):
#         return ["अगला question practice करें?", "Answer improve कैसे करें?", "Common tips बताओ"]
#     elif any(word in question for word in ["machine learning", "data science", "ai"]):
#         return ["Real-world example?", "Best resources कौन से?", "Latest trends क्या हैं?"]
#     else:
#         return ["और detail में बताओ?", "Example के साथ समझाओ?", "क्या related कुछ और पूछू?"]


# # --------------------- Page Setup ---------------------
# st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="centered")

# # Splash Screen
# if "started" not in st.session_state:
#     st.session_state.started = False

# if not st.session_state.started:
#     st.markdown("""
#         <style>
#         .welcome-container {
#             display: flex;
#             flex-direction: column;
#             align-items: center;
#             justify-content: center;
#             height: 100vh;
#             background: linear-gradient(to bottom, #f0f8ff, #e0f0ff);
#             text-align: center;
#             padding: 20px;
#         }
#         .robot-img {
#             border-radius: 50%;
#             border: 8px solid #4CAF50;
#             box-shadow: 0 0 30px rgba(76, 175, 80, 0.5);
#             animation: float 3s ease-in-out infinite;
#             margin-bottom: 30px;
#         }
#         @keyframes float {
#             0% { transform: translateY(0px); }
#             50% { transform: translateY(-15px); }
#             100% { transform: translateY(0px); }
#         }
#         .title {font-size: 3.8rem; margin: 10px 0; font-weight: bold; color: #333;}
#         .subtitle {font-size: 1.8rem; margin: 20px 0 50px 0; color: #555;}
#         </style>
#     """, unsafe_allow_html=True)

#     st.markdown('<div class="welcome-container">', unsafe_allow_html=True)

#     try:
#         st.image(r"C:\Users\shekhar\OneDrive\Desktop\AI_Interview_Chatbot\chatbot\new_robot.png", 
#                  width=450, caption="आपका AI दोस्त 😄", use_column_width=False)
#         st.markdown('<img src="data:image/png;base64,...">', unsafe_allow_html=True)  # अगर animation चाहिए
#     except:
#         st.markdown("<h1 style='font-size:10rem;'>🤖</h1>", unsafe_allow_html=True)

#     st.markdown("<div class='title'>AI Chat Assistant</div>", unsafe_allow_html=True)
#     st.markdown("<div class='subtitle'>Voice या Text से बात करो • मैं हमेशा मदद के लिए तैयार हूँ!</div>", unsafe_allow_html=True)

#     if st.button("🚀 Start Chat करो!", use_container_width=True):
#         st.session_state.started = True
#         st.rerun()

#     st.markdown("</div>", unsafe_allow_html=True)

# # --------------------- Main Chat Interface ---------------------
# else:
#     st.markdown("""
#         <h1 style='text-align: center; color: #4CAF50;'>🤖 AI Chat Assistant</h1>
#         <p style='text-align: center; color: #666;'>Ask Anything – Voice या Text से! 🔊 हर जवाब बोलेगा</p>
#         <hr>
#     """, unsafe_allow_html=True)

#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Display chat history
#     for msg in st.session_state.messages:
#         if msg["role"] == "user":
#             with st.chat_message("user", avatar="👤"):
#                 st.markdown(msg["content"])
#         else:
#             with st.chat_message("assistant"):
#                 cols = st.columns([1, 12])
#                 with cols[0]:
#                     try:
#                         st.image(r"C:\Users\shekhar\OneDrive\Desktop\AI_Interview_Chatbot\chatbot\robot.png", width=50)
#                     except:
#                         st.markdown("🤖")
#                 with cols[1]:
#                     st.markdown(msg["content"])

#     # Suggested questions
#     if len(st.session_state.messages) >= 2 and st.session_state.messages[-1]["role"] == "assistant":
#         last_question = st.session_state.messages[-2]["content"]
#         suggestions = get_suggestions(last_question)
#         st.markdown("**💡 Suggested Questions:**")
#         cols = st.columns(3)
#         for idx, sugg in enumerate(suggestions):
#             if cols[idx].button(sugg, use_container_width=True):
#                 st.session_state.pending_question = sugg
#                 st.rerun()

#     # Voice Input
#     st.markdown("**🎤 Voice Input**")
#     voice_key = f"voice_{len(st.session_state.messages)}"
#     text_from_voice = speech_to_text(
#         language="en",
#         start_prompt="🎤 Start Recording",
#         stop_prompt="⏹️ Stop Recording",
#         just_once=False,
#         use_container_width=True,
#         key=voice_key
#     )

#     text_input = st.chat_input("Type your message here...")

#     # Get question
#     if "pending_question" in st.session_state:
#         question = st.session_state.pending_question
#         del st.session_state.pending_question
#     else:
#         question = text_from_voice or text_input

#     if question:
#         st.session_state.messages.append({"role": "user", "content": question})
#         with st.chat_message("user", avatar="👤"):
#             st.markdown(question)

#         with st.chat_message("assistant"):
#             cols = st.columns([1, 12])
#             with cols[0]:
#                 try:
#                     st.image(r"C:\Users\shekhar\OneDrive\Desktop\AI_Interview_Chatbot\chatbot\robot.png", width=50)
#                 except:
#                     st.markdown("🤖")
#             with cols[1]:
#                 with st.spinner("🤔 सोच रहा हूँ..."):
#                     history = [m for m in st.session_state.messages[:-1]]
#                     response = generate_answer(question, history)
#                 st.markdown(response)
#                 play_audio(response)  # Auto voice selection + fallback

#         st.session_state.messages.append({"role": "assistant", "content": response})

#     # Sidebar
#     with st.sidebar:
#         st.header("⚙️ Options")
#         st.caption("🔊 Smart Voice Selection with Fallback")
#         st.caption("🇮🇳 Hindi: Swati → Madhur (fallback)")
#         st.caption("🇬🇧 English: Neerja (best)")
#         st.caption("💡 Long Hindi answers now speak reliably!")
#         if st.button("🗑️ Clear Chat"):
#             st.session_state.messages = []
#             st.rerun()












# import streamlit as st
# from streamlit_mic_recorder import speech_to_text
# from answer_generator import generate_answer
# import re
# import edge_tts
# import asyncio
# import io
# import base64

# # --------------------- Edge TTS with Reliable Fallback ---------------------
# async def get_edge_audio(text, voice):
#     communicate = edge_tts.Communicate(text, voice)
#     audio_bytes = io.BytesIO()
#     async for chunk in communicate.stream():
#         if chunk["type"] == "audio":
#             audio_bytes.write(chunk["data"])
#     audio_bytes.seek(0)
#     return audio_bytes.getvalue()

# def play_audio(text):
#     try:
#         clean_text = re.sub(r'(\*\*|__|\*|_|`|~|#|>|\|)', '', text)
#         clean_text = re.sub(r'\n+', '. ', clean_text)
#         clean_text = re.sub(r'\s+', ' ', clean_text)
#         clean_text = clean_text.strip()

#         if not clean_text:
#             return

#         hindi_char_count = sum(1 for c in clean_text if '\u0900' <= c <= '\u097F')
#         total_chars = len(clean_text)
#         hindi_ratio = hindi_char_count / total_chars if total_chars > 0 else 0

#         if hindi_ratio > 0.3:
#             primary_voice = "hi-IN-SwatiNeural"
#             fallback_voice = "hi-IN-MadhurNeural"
#             voice_display = "Hindi (Swati → Madhur fallback)"
#         else:
#             primary_voice = "en-IN-NeerjaNeural"
#             fallback_voice = None
#             voice_display = "English (Neerja)"

#         st.caption(f"🔊 Trying voice: **{voice_display}**")

#         try:
#             audio_data = asyncio.run(get_edge_audio(clean_text, primary_voice))
#             used_voice = primary_voice
#         except Exception as primary_error:
#             st.warning(f"Primary voice failed. Switching to fallback...")
#             if fallback_voice:
#                 try:
#                     audio_data = asyncio.run(get_edge_audio(clean_text, fallback_voice))
#                     used_voice = fallback_voice
#                 except Exception as fallback_error:
#                     st.error(f"All Hindi voices failed: {fallback_error}")
#                     return
#             else:
#                 st.error(f"Voice failed: {primary_error}")
#                 return

#         voice_name = "Hindi (Madhur)" if used_voice == "hi-IN-MadhurNeural" else \
#                      "Hindi (Swati)" if used_voice == "hi-IN-SwatiNeural" else \
#                      "English (Neerja)"
#         st.caption(f"✅ Speaking in: **{voice_name}**")

#         audio_base64 = base64.b64encode(audio_data).decode('utf-8')
#         audio_html = f"""
#         <audio autoplay="true" style="display:none;">
#             <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
#         </audio>
#         <script>
#             var audio = document.querySelector('audio');
#             if (audio) {{ audio.play().catch(e => console.log("Play failed:", e)); }}
#         </script>
#         """
#         st.markdown(audio_html, unsafe_allow_html=True)
#         st.markdown("🔊 **बोल रहा हूँ... पूरी सुनो!**")

#     except Exception as e:
#         st.error(f"आवाज़ में समस्या: {e}")
#         st.caption("इंटरनेट चेक करें या थोड़ी देर बाद ट्राई करें।")


# # --------------------- Suggestions ---------------------
# def get_suggestions(last_question):
#     question = last_question.lower()
#     if any(word in question for word in ["code", "python", "program", "error", "debug"]):
#         return ["इसका code example चाहिए?", "और optimize कैसे करें?", "Common mistakes क्या हैं?"]
#     elif any(word in question for word in ["interview", "job", "resume", "question"]):
#         return ["अगला question practice करें?", "Answer improve कैसे करें?", "Common tips बताओ"]
#     elif any(word in question for word in ["machine learning", "data science", "ai"]):
#         return ["Real-world example?", "Best resources कौन से?", "Latest trends क्या हैं?"]
#     else:
#         return ["और detail में बताओ?", "Example के साथ समझाओ?", "क्या related कुछ और पूछू?"]


# # --------------------- Page Setup ---------------------
# st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="centered")

# # Splash Screen
# if "started" not in st.session_state:
#     st.session_state.started = False

# if not st.session_state.started:
#     st.markdown("""
#         <style>
#         .welcome-container {
#             display: flex;
#             flex-direction: column;
#             align-items: center;
#             justify-content: center;
#             height: 100vh;
#             background: linear-gradient(to bottom, #f0f8ff, #e0f0ff);
#             text-align: center;
#             padding: 20px;
#         }
#         .title {font-size: 3.8rem; margin: 10px 0; font-weight: bold; color: #333;}
#         .subtitle {font-size: 1.8rem; margin: 20px 0 50px 0; color: #555;}
#         </style>
#     """, unsafe_allow_html=True)

#     st.markdown('<div class="welcome-container">', unsafe_allow_html=True)

#     try:
#         # ← नया fixed width (warning-free)
#         st.image(r"C:\Users\shekhar\OneDrive\Desktop\AI_Interview_Chatbot\chatbot\robot.png", width=450)
#     except:
#         st.markdown("<h1 style='font-size:10rem;'>🤖</h1>", unsafe_allow_html=True)

#     st.markdown("<div class='title'>AI Chat Assistant</div>", unsafe_allow_html=True)
#     st.markdown("<div class='subtitle'>Voice या Text से बात करो • हर जवाब automatic बोलेगा!</div>", unsafe_allow_html=True)

#     # ← use_container_width → width="stretch"
#     if st.button("🚀 Tap to Start Chat", width="stretch"):
#         st.session_state.started = True
#         st.rerun()

#     st.markdown("</div>", unsafe_allow_html=True)

# # --------------------- Main Chat Interface ---------------------
# else:
#     st.markdown("""
#         <h1 style='text-align: center; color: #4CAF50;'>🤖 AI Chat Assistant</h1>
#         <p style='text-align: center; color: #666;'>Ask Anything – Voice या Text से! 🔊 हर जवाब बोलेगा</p>
#         <hr>
#     """, unsafe_allow_html=True)

#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     for msg in st.session_state.messages:
#         if msg["role"] == "user":
#             with st.chat_message("user", avatar="👤"):
#                 st.markdown(msg["content"])
#         else:
#             with st.chat_message("assistant"):
#                 cols = st.columns([1, 12])
#                 with cols[0]:
#                     try:
#                         # ← छोटा avatar – fixed width
#                         st.image(r"C:\Users\shekhar\OneDrive\Desktop\AI_Interview_Chatbot\chatbot\robot.png", width=50)
#                     except:
#                         st.markdown("🤖")
#                 with cols[1]:
#                     st.markdown(msg["content"])

#     # Suggested questions
#     if len(st.session_state.messages) >= 2 and st.session_state.messages[-1]["role"] == "assistant":
#         last_question = st.session_state.messages[-2]["content"]
#         suggestions = get_suggestions(last_question)
#         st.markdown("**💡 Suggested Questions:**")
#         cols = st.columns(3)
#         for idx, sugg in enumerate(suggestions):
#             # ← width="stretch" for full width buttons
#             if cols[idx].button(sugg, width="stretch"):
#                 st.session_state.pending_question = sugg
#                 st.rerun()

#     # Voice Input
#     st.markdown("**🎤 Voice Input**")
#     voice_key = f"voice_{len(st.session_state.messages)}"
#     text_from_voice = speech_to_text(
#         language="en",
#         start_prompt="🎤 Start Recording",
#         stop_prompt="⏹️ Stop Recording",
#         just_once=False,
#         use_container_width=True,  # ← यह component अभी support करता है (no warning)
#         key=voice_key
#     )

#     text_input = st.chat_input("Type your message here...")

#     if "pending_question" in st.session_state:
#         question = st.session_state.pending_question
#         del st.session_state.pending_question
#     else:
#         question = text_from_voice or text_input

#     if question:
#         st.session_state.messages.append({"role": "user", "content": question})
#         with st.chat_message("user", avatar="👤"):
#             st.markdown(question)

#         with st.chat_message("assistant"):
#             cols = st.columns([1, 12])
#             with cols[0]:
#                 try:
#                     st.image(r"C:\Users\shekhar\OneDrive\Desktop\AI_Interview_Chatbot\chatbot\robot.png", width=50)
#                 except:
#                     st.markdown("🤖")
#             with cols[1]:
#                 with st.spinner("🤔 सोच रहा हूँ..."):
#                     history = [m for m in st.session_state.messages[:-1]]
#                     response = generate_answer(question, history)
#                 st.markdown(response)
#                 play_audio(response)

#         st.session_state.messages.append({"role": "assistant", "content": response})

#     with st.sidebar:
#         st.header("⚙️ Options")
#         st.caption("🔊 Smart Voice + Reliable Fallback")
#         st.caption("🇮🇳 Hindi: Swati → Madhur")
#         st.caption("🇬🇧 English: Neerja")
#         if st.button("🗑️ Clear Chat", width="stretch"):
#             st.session_state.messages = []
#             st.rerun()








# import streamlit as st
# from streamlit_mic_recorder import speech_to_text
# from answer_generator import generate_answer
# import re
# import edge_tts
# import asyncio
# import io
# import base64

# # --------------------- Edge TTS with Reliable Fallback ---------------------
# async def get_edge_audio(text, voice):
#     communicate = edge_tts.Communicate(text, voice)
#     audio_bytes = io.BytesIO()
#     async for chunk in communicate.stream():
#         if chunk["type"] == "audio":
#             audio_bytes.write(chunk["data"])
#     audio_bytes.seek(0)
#     return audio_bytes.getvalue()

# def play_audio(text):
#     try:
#         clean_text = re.sub(r'(\*\*|__|\*|_|`|~|#|>|\|)', '', text)
#         clean_text = re.sub(r'\n+', '. ', clean_text)
#         clean_text = re.sub(r'\s+', ' ', clean_text)
#         clean_text = clean_text.strip()

#         if not clean_text:
#             return

#         # Devanagari script detection (covers Hindi, Marathi, etc.)
#         devanagari_count = sum(1 for c in clean_text if '\u0900' <= c <= '\u097F')
#         devanagari_ratio = devanagari_count / len(clean_text) if len(clean_text) > 0 else 0

#         if devanagari_ratio > 0.3:
#             primary_voice = "hi-IN-SwatiNeural"
#             fallback_voice = "hi-IN-MadhurNeural"
#             voice_display = "Hindi Accent (Hindi/Marathi content के लिए)"
#         else:
#             primary_voice = "en-IN-NeerjaNeural"
#             fallback_voice = None
#             voice_display = "English (Neerja)"

#         st.caption(f"🔊 Voice: **{voice_display}**")
#         if devanagari_ratio > 0.3:
#             st.caption("मराठी/हिंदी कंटेंट हिंदी voice में बोला जा रहा है")

#         try:
#             audio_data = asyncio.run(get_edge_audio(clean_text, primary_voice))
#             used_voice = primary_voice
#         except Exception as primary_error:
#             st.warning("Primary voice failed. Switching to fallback...")
#             if fallback_voice:
#                 try:
#                     audio_data = asyncio.run(get_edge_audio(clean_text, fallback_voice))
#                     used_voice = fallback_voice
#                 except Exception as fallback_error:
#                     st.error(f"All voices failed: {fallback_error}")
#                     return
#             else:
#                 st.error(f"Voice failed: {primary_error}")
#                 return

#         voice_name = "Hindi (Madhur)" if used_voice == "hi-IN-MadhurNeural" else \
#                      "Hindi (Swati)" if used_voice == "hi-IN-SwatiNeural" else \
#                      "English (Neerja)"
#         st.caption(f"✅ Speaking in: **{voice_name}**")

#         audio_base64 = base64.b64encode(audio_data).decode('utf-8')
#         audio_html = f"""
#         <audio autoplay="true" style="display:none;">
#             <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
#         </audio>
#         <script>
#             var audio = document.querySelector('audio');
#             if (audio) {{ audio.play().catch(e => console.log("Play failed:", e)); }}
#         </script>
#         """
#         st.markdown(audio_html, unsafe_allow_html=True)
#         st.markdown("🔊 **बोल रहा हूँ... पूरी सुनो!**")

#     except Exception as e:
#         st.error(f"आवाज़ में समस्या: {e}")
#         st.caption("इंटरनेट चेक करें या थोड़ी देर बाद ट्राई करें।")


# # --------------------- Page Setup ---------------------
# st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="centered")

# # Splash Screen
# if "started" not in st.session_state:
#     st.session_state.started = False

# if not st.session_state.started:
#     st.markdown("""
#         <style>
#         .welcome-container {
#             display: flex;
#             flex-direction: column;
#             align-items: center;
#             justify-content: center;
#             height: 100vh;
#             background: linear-gradient(to bottom, #f0f8ff, #e0f0ff);
#             text-align: center;
#             padding: 20px;
#         }
#         .title {font-size: 3.8rem; margin: 10px 0; font-weight: bold; color: #333;}
#         .subtitle {font-size: 1.8rem; margin: 20px 0 50px 0; color: #555;}
#         </style>
#     """, unsafe_allow_html=True)

#     st.markdown('<div class="welcome-container">', unsafe_allow_html=True)

#     try:
#         st.image(r"C:\Users\shekhar\OneDrive\Desktop\AI_Interview_Chatbot\chatbot\robot.png", width=450)
#     except:
#         st.markdown("<h1 style='font-size:10rem;'>🤖</h1>", unsafe_allow_html=True)

#     st.markdown("<div class='title'>AI Chat Assistant</div>", unsafe_allow_html=True)
#     st.markdown("<div class='subtitle'>Voice या Text से बात करो • हर जवाब automatic बोलेगा!</div>", unsafe_allow_html=True)

#     if st.button("🚀 Tap to Start Chat", width="stretch"):
#         st.session_state.started = True
#         st.rerun()

#     st.markdown("</div>", unsafe_allow_html=True)

# # --------------------- Main Chat Interface ---------------------
# else:
#     st.markdown("""
#         <h1 style='text-align: center; color: #4CAF50;'>🤖 AI Chat Assistant</h1>
#         <p style='text-align: center; color: #666;'>Ask Anything – Voice या Text से! 🔊 हर जवाब बोलेगा</p>
#         <hr>
#     """, unsafe_allow_html=True)

#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Display chat history
#     for msg in st.session_state.messages:
#         if msg["role"] == "user":
#             with st.chat_message("user", avatar="👤"):
#                 st.markdown(msg["content"])
#         else:
#             with st.chat_message("assistant"):
#                 cols = st.columns([1, 12])
#                 with cols[0]:
#                     try:
#                         st.image(r"C:\Users\shekhar\OneDrive\Desktop\AI_Interview_Chatbot\chatbot\robot.png", width=50)
#                     except:
#                         st.markdown("🤖")
#                 with cols[1]:
#                     st.markdown(msg["content"])

#     # Voice Input
#     st.markdown("**🎤 Voice Input**")
#     voice_key = f"voice_{len(st.session_state.messages)}"
#     text_from_voice = speech_to_text(
#         language="en",  # You can change to "hi" or "mr" if needed
#         start_prompt="🎤 Start Recording",
#         stop_prompt="⏹️ Stop Recording",
#         just_once=False,
#         use_container_width=True,
#         key=voice_key
#     )

#     text_input = st.chat_input("Type your message here...")

#     question = text_from_voice or text_input

#     if question:
#         st.session_state.messages.append({"role": "user", "content": question})
#         with st.chat_message("user", avatar="👤"):
#             st.markdown(question)

#         with st.chat_message("assistant"):
#             cols = st.columns([1, 12])
#             with cols[0]:
#                 try:
#                     st.image(r"C:\Users\shekhar\OneDrive\Desktop\AI_Interview_Chatbot\chatbot\robot.png", width=50)
#                 except:
#                     st.markdown("🤖")
#             with cols[1]:
#                 with st.spinner("🤔 सोच रहा हूँ..."):
#                     history = [m for m in st.session_state.messages[:-1]]
#                     response = generate_answer(question, history)
#                 st.markdown(response)
#                 play_audio(response)

#         st.session_state.messages.append({"role": "assistant", "content": response})

#     # Sidebar
#     with st.sidebar:
#         st.header("⚙️ Options")
#         st.caption("🔊 Smart Voice Selection")
#         st.caption("🇬🇧 English → Neerja Neural")
#         st.caption("🇮🇳 Hindi/Marathi → Hindi Voice (Swati/Madhur)")
#         st.caption("🎤 Mic: English set (change language='mr' for Marathi)")
#         if st.button("🗑️ Clear Chat", width="stretch"):
#             st.session_state.messages = []
#             st.rerun()








####################################################

# import streamlit as st
# from streamlit_mic_recorder import speech_to_text
# from answer_generator import generate_answer
# import re
# import edge_tts
# import asyncio
# import io
# import base64

# # --------------------- Edge TTS with Reliable Fallback ---------------------
# async def get_edge_audio(text, voice):
#     communicate = edge_tts.Communicate(text, voice)
#     audio_bytes = io.BytesIO()
#     async for chunk in communicate.stream():
#         if chunk["type"] == "audio":
#             audio_bytes.write(chunk["data"])
#     audio_bytes.seek(0)
#     return audio_bytes.getvalue()

# def play_audio(text):
#     try:
#         clean_text = re.sub(r'(\*\*|__|\*|_|`|~|#|>|\|)', '', text)
#         clean_text = re.sub(r'\n+', '. ', clean_text)
#         clean_text = re.sub(r'\s+', ' ', clean_text)
#         clean_text = clean_text.strip()

#         if not clean_text:
#             return

#         devanagari_count = sum(1 for c in clean_text if '\u0900' <= c <= '\u097F')
#         devanagari_ratio = devanagari_count / len(clean_text) if len(clean_text) > 0 else 0

#         if devanagari_ratio > 0.3:
#             primary_voice = "hi-IN-SwatiNeural"
#             fallback_voice = "hi-IN-MadhurNeural"
#             voice_display = "Hindi Accent (Hindi/Marathi content के लिए)"
#         else:
#             primary_voice = "en-IN-NeerjaNeural"
#             fallback_voice = None
#             voice_display = "English (Neerja)"

#         st.caption(f"🔊 Voice: **{voice_display}**")
#         if devanagari_ratio > 0.3:
#             st.caption("मराठी/हिंदी कंटेंट हिंदी voice में बोला जा रहा है")

#         try:
#             audio_data = asyncio.run(get_edge_audio(clean_text, primary_voice))
#             used_voice = primary_voice
#         except Exception as primary_error:
#             st.warning("Primary voice failed. Switching to fallback...")
#             if fallback_voice:
#                 try:
#                     audio_data = asyncio.run(get_edge_audio(clean_text, fallback_voice))
#                     used_voice = fallback_voice
#                 except Exception as fallback_error:
#                     st.error(f"All voices failed: {fallback_error}")
#                     return
#             else:
#                 st.error(f"Voice failed: {primary_error}")
#                 return

#         voice_name = "Hindi (Madhur)" if used_voice == "hi-IN-MadhurNeural" else \
#                      "Hindi (Swati)" if used_voice == "hi-IN-SwatiNeural" else \
#                      "English (Neerja)"
#         st.caption(f"✅ Speaking in: **{voice_name}**")

#         audio_base64 = base64.b64encode(audio_data).decode('utf-8')
#         audio_html = f"""
#         <audio autoplay="true" style="display:none;">
#             <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
#         </audio>
#         <script>
#             var audio = document.querySelector('audio');
#             if (audio) {{ audio.play().catch(e => console.log("Play failed:", e)); }}
#         </script>
#         """
#         st.markdown(audio_html, unsafe_allow_html=True)
#         st.markdown("🔊 **बोल रहा हूँ... पूरी सुनो!**")

#     except Exception as e:
#         st.error(f"आवाज़ में समस्या: {e}")
#         st.caption("इंटरनेट चेक करें या थोड़ी देर बाद ट्राई करें।")


# # --------------------- Page Setup ---------------------
# st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="centered")

# # Splash Screen
# if "started" not in st.session_state:
#     st.session_state.started = False

# if not st.session_state.started:
#     st.markdown("""
#         <style>
#         .welcome-container {
#             display: flex;
#             flex-direction: column;
#             align-items: center;
#             justify-content: center;
#             height: 100vh;
#             background: linear-gradient(to bottom, #f0f8ff, #e0f0ff);
#             text-align: center;
#             padding: 20px;
#         }
#         .title {font-size: 3.8rem; margin: 10px 0; font-weight: bold; color: #333;}
#         .subtitle {font-size: 1.8rem; margin: 20px 0 50px 0; color: #555;}
#         </style>
#     """, unsafe_allow_html=True)

#     st.markdown('<div class="welcome-container">', unsafe_allow_html=True)

#     try:
#         st.image(r"C:\Users\shekhar\OneDrive\Desktop\AI_Interview_Chatbot\chatbot\robot.png", width=450)
#     except:
#         st.markdown("<h1 style='font-size:10rem;'>🤖</h1>", unsafe_allow_html=True)

#     st.markdown("<div class='title'>AI Chat Assistant</div>", unsafe_allow_html=True)
#     st.markdown("<div class='subtitle'>Voice या Text से बात करो • Image/Video भेजो • हर जवाब बोलेगा!</div>", unsafe_allow_html=True)

#     if st.button("🚀 Tap to Start Chat", use_container_width=True):
#         st.session_state.started = True
#         st.rerun()

#     st.markdown("</div>", unsafe_allow_html=True)

# # --------------------- Main Chat Interface ---------------------
# else:
#     st.markdown("""
#         <h1 style='text-align: center; color: #4CAF50;'>🤖 AI Chat Assistant</h1>
#         <p style='text-align: center; color: #666;'>Voice, Text या Image/Video भेजो 🔊 हर जवाब बोलेगा</p>
#         <hr>
#     """, unsafe_allow_html=True)

#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Display chat history
#     for msg in st.session_state.messages:
#         if msg["role"] == "user":
#             with st.chat_message("user", avatar="👤"):
#                 if msg.get("content"):
#                     st.markdown(msg["content"])
#                 if msg.get("files"):
#                     for file in msg["files"]:
#                         if file.type.startswith("image/"):
#                             st.image(file, caption=file.name)
#                         elif file.type.startswith("video/"):
#                             st.video(file)
#         else:
#             with st.chat_message("assistant"):
#                 cols = st.columns([1, 12])
#                 with cols[0]:
#                     try:
#                         st.image(r"C:\Users\shekhar\OneDrive\Desktop\AI_Interview_Chatbot\chatbot\robot.png", width=50)
#                     except:
#                         st.markdown("🤖")
#                 with cols[1]:
#                     st.markdown(msg["content"])

#     # Voice Input
#     st.markdown("**🎤 Voice Input**")
#     voice_key = f"voice_{len(st.session_state.messages)}"
#     text_from_voice = speech_to_text(
#         language="en",
#         start_prompt="🎤 Start Recording",
#         stop_prompt="⏹️ Stop Recording",
#         just_once=False,
#         use_container_width=True,
#         key=voice_key
#     )

#     # Chat Input with File Upload (ChatGPT Style)
#     prompt = st.chat_input(
#         "Type your message... or attach image/video 📎",
#         accept_file=True,  # या "multiple" अगर multiple files allow करना हो
#         file_type=["jpg", "jpeg", "png", "gif", "webp", "mp4", "mov", "avi", "webm"]
#     )

#     user_text = text_from_voice or (prompt.text if prompt else None)
#     uploaded_files = prompt.files if prompt else None  # Note: prompt.files (docs के अनुसार)

#     if user_text or uploaded_files:
#         display_text = user_text or "Describe this image/video"

#         # Display user message
#         with st.chat_message("user", avatar="👤"):
#             if user_text:
#                 st.markdown(user_text)
#             if uploaded_files:
#                 for file in uploaded_files:
#                     if file.type.startswith("image/"):
#                         st.image(file, caption=file.name)
#                     elif file.type.startswith("video/"):
#                         st.video(file)

#         # Save user message with files
#         st.session_state.messages.append({
#             "role": "user",
#             "content": display_text,
#             "files": uploaded_files
#         })

#         # Generate response (अभी files ignore कर रहे हैं error avoid करने के लिए)
#         with st.chat_message("assistant"):
#             cols = st.columns([1, 12])
#             with cols[0]:
#                 try:
#                     st.image(r"C:\Users\shekhar\OneDrive\Desktop\AI_Interview_Chatbot\chatbot\robot.png", width=50)
#                 except:
#                     st.markdown("🤖")
#             with cols[1]:
#                 with st.spinner("🤔 सोच रहा हूँ..."):
#                     history = [
#                         {"role": m["role"], "content": m["content"]}
#                         for m in st.session_state.messages[:-1]
#                     ]
#                     # अब 3 arguments pass कर रहे हैं - vision के लिए
#                     response = generate_answer(display_text, history, uploaded_files)  # 3 arguments – अब safe है!
#                 st.markdown(response)
#                 play_audio(response)

#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": response
#         })

#     # Sidebar
#     with st.sidebar:
#         st.header("⚙️ Options")
#         st.caption("🔊 Smart Voice Selection")
#         st.caption("🇬🇧 English → Neerja Neural")
#         st.caption("🇮🇳 Hindi/Marathi → Hindi Voice (Swati/Madhur)")
#         st.caption("🎤 Mic: English (change to 'mr' for Marathi)")
#         st.caption("📎 Image & Video upload supported!")
#         if st.button("🗑️ Clear Chat", use_container_width=True):
#             st.session_state.messages = []
#             st.rerun()



######################%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&



# answer_generator.py (Updated with Vision Support using latest OpenAI model)

import streamlit as st
from streamlit_mic_recorder import speech_to_text
from answer_generator import generate_answer
import re
import edge_tts
import asyncio
import io
import base64

# --------------------- Edge TTS with Reliable Fallback ---------------------
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
        clean_text = re.sub(r'\s+', ' ', clean_text)
        clean_text = clean_text.strip()

        if not clean_text:
            return

        devanagari_count = sum(1 for c in clean_text if '\u0900' <= c <= '\u097F')
        devanagari_ratio = devanagari_count / len(clean_text) if len(clean_text) > 0 else 0

        if devanagari_ratio > 0.3:
            primary_voice = "hi-IN-SwatiNeural"
            fallback_voice = "hi-IN-MadhurNeural"
            voice_display = "Hindi Accent (Hindi/Marathi content के लिए)"
        else:
            primary_voice = "en-IN-NeerjaNeural"
            fallback_voice = None
            voice_display = "English (Neerja)"

        st.caption(f"🔊 Voice: **{voice_display}**")
        if devanagari_ratio > 0.3:
            st.caption("मराठी/हिंदी कंटेंट हिंदी voice में बोला जा रहा है")

        try:
            audio_data = asyncio.run(get_edge_audio(clean_text, primary_voice))
            used_voice = primary_voice
        except Exception as primary_error:
            st.warning("Primary voice failed. Switching to fallback...")
            if fallback_voice:
                try:
                    audio_data = asyncio.run(get_edge_audio(clean_text, fallback_voice))
                    used_voice = fallback_voice
                except Exception as fallback_error:
                    st.error(f"All voices failed: {fallback_error}")
                    return
            else:
                st.error(f"Voice failed: {primary_error}")
                return

        voice_name = "Hindi (Madhur)" if used_voice == "hi-IN-MadhurNeural" else \
                     "Hindi (Swati)" if used_voice == "hi-IN-SwatiNeural" else \
                     "English (Neerja)"
        st.caption(f"✅ Speaking in: **{voice_name}**")

        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        audio_html = f"""
        <audio autoplay="true" style="display:none;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        <script>
            var audio = document.querySelector('audio');
            if (audio) {{ audio.play().catch(e => console.log("Play failed:", e)); }}
        </script>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
        st.markdown("🔊 **बोल रहा हूँ... पूरी सुनो!**")

    except Exception as e:
        st.error(f"आवाज़ में समस्या: {e}")
        st.caption("इंटरनेट चेक करें या थोड़ी देर बाद ट्राई करें।")


# --------------------- Page Setup ---------------------
st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="centered")

# Splash Screen
if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.markdown("""
        <style>
        .welcome-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            background: linear-gradient(to bottom, #f0f8ff, #e0f0ff);
            text-align: center;
            padding: 20px;
        }
        .title {font-size: 3.8rem; margin: 10px 0; font-weight: bold; color: #333;}
        .subtitle {font-size: 1.8rem; margin: 20px 0 50px 0; color: #555;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="welcome-container">', unsafe_allow_html=True)

    try:
        st.image(r"C:\Users\shekhar\OneDrive\Desktop\AI_Interview_Chatbot\chatbot\robot.png", width=450)
    except:
        st.markdown("<h1 style='font-size:10rem;'>🤖</h1>", unsafe_allow_html=True)

    st.markdown("<div class='title'>AI Chat Assistant</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Voice या Text से बात करो • Image/Video भेजो • हर जवाब बोलेगा!</div>", unsafe_allow_html=True)

    if st.button("🚀 Tap to Start Chat", use_container_width=True):
        st.session_state.started = True
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------- Main Chat Interface ---------------------
else:
    st.markdown("""
        <h1 style='text-align: center; color: #4CAF50;'>🤖 AI Chat Assistant</h1>
        <p style='text-align: center; color: #666;'>Voice, Text या Image/Video भेजो 🔊 हर जवाब बोलेगा</p>
        <hr>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                if msg.get("content"):
                    st.markdown(msg["content"])
                if msg.get("files"):
                    for file in msg["files"]:
                        if file.type.startswith("image/"):
                            st.image(file, caption=file.name)
                        elif file.type.startswith("video/"):
                            st.video(file)
        else:
            with st.chat_message("assistant"):
                cols = st.columns([1, 12])
                with cols[0]:
                    try:
                        st.image(r"C:\Users\shekhar\OneDrive\Desktop\AI_Interview_Chatbot\chatbot\robot.png", width=50)
                    except:
                        st.markdown("🤖")
                with cols[1]:
                    st.markdown(msg["content"])

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

    # Chat Input with File Upload (ChatGPT Style)
    prompt = st.chat_input(
        "Type your message... or attach image/video 📎",
        accept_file=True,
        file_type=["jpg", "jpeg", "png", "gif", "webp", "mp4", "mov", "avi", "webm"]
    )

    user_text = text_from_voice or (prompt.text if prompt else None)
    uploaded_files = prompt.files if prompt else None

    if user_text or uploaded_files:
        display_text = user_text or "Describe this image/video"

        # Display user message
        with st.chat_message("user", avatar="👤"):
            if user_text:
                st.markdown(user_text)
            if uploaded_files:
                for file in uploaded_files:
                    if file.type.startswith("image/"):
                        st.image(file, caption=file.name)
                    elif file.type.startswith("video/"):
                        st.video(file)

        # Save user message with files
        st.session_state.messages.append({
            "role": "user",
            "content": display_text,
            "files": uploaded_files
        })

        # Generate response
        with st.chat_message("assistant"):
            cols = st.columns([1, 12])
            with cols[0]:
                try:
                    st.image(r"C:\Users\shekhar\OneDrive\Desktop\AI_Interview_Chatbot\chatbot\robot.png", width=50)
                except:
                    st.markdown("🤖")
            with cols[1]:
                with st.spinner("🤔 सोच रहा हूँ..."):
                    history = [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages[:-1]
                    ]
                    response = generate_answer(display_text, history, uploaded_files)
                st.markdown(response)
                play_audio(response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Options")
        st.caption("🔊 Smart Voice Selection")
        st.caption("🇬🇧 English → Neerja Neural")
        st.caption("🇮🇳 Hindi/Marathi → Hindi Voice (Swati/Madhur)")
        st.caption("🎤 Mic: English (change to 'mr' for Marathi)")
        st.caption("📎 Image & Video upload supported!")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()