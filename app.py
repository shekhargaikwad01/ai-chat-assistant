
# import streamlit as st
# from streamlit_mic_recorder import speech_to_text
# from evaluator import evaluate_answer
# from question_generator import generate_question
# from answer_generator import generate_answer

# # Page setup
# st.set_page_config(page_title="AI Chatbot Pro", page_icon="🤖", layout="centered")

# # Beautiful Title
# st.markdown("""
#     <h1 style='text-align: center; color: #4CAF50;'>🤖 Advanced AI Chatbot</h1>
#     <p style='text-align: center; color: #666;'>Interview Prep + General Q&A with Voice & Text</p>
#     <hr>
# """, unsafe_allow_html=True)

# mode = st.selectbox("🌟 Choose Mode", ["Interview Preparation", "Q&A Assistant"])

# # ====================== INTERVIEW MODE ======================
# if mode == "Interview Preparation":
#     role = st.selectbox("Select Job Role", [
#         "Data Science", "Machine Learning Engineer", "Software Engineer",
#         "Python Developer", "HR", "Product Manager", "DevOps Engineer"
#     ])
    
#     if st.button("🎯 Start New Interview", use_container_width=True):
#         with st.spinner("Generating question..."):
#             st.session_state.question = generate_question(role)
#         st.session_state.mode = "interview"
    
#     if st.session_state.get("mode") == "interview" and "question" in st.session_state:
#         st.markdown("### 📌 Interview Question:")
#         st.info(st.session_state.question)
        
#         answer = st.text_area("✍️ Your Answer", height=150, key="interview_ans")
        
#         if st.button("Submit Answer", use_container_width=True):
#             with st.spinner("Evaluating your answer..."):
#                 feedback = evaluate_answer(st.session_state.question, answer)
#             st.success("### Feedback")
#             st.markdown(feedback)
        
#         # After the feedback display, add this:
#         if st.button("➡️ Next Question", use_container_width=True):
#             with st.spinner("Generating next question..."):
#                 st.session_state.question = generate_question(role)
#     # Keep the same role and mode
#             st.rerun() 

# # ====================== Q&A MODE ======================
# else:
#     st.markdown("### 💬 Ask Anything – Voice या Text से!")

#     # Initialize messages
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Display chat history beautifully
#     for msg in st.session_state.messages:
#         if msg["role"] == "user":
#             with st.chat_message("user", avatar="👤"):
#                 st.markdown(msg["content"])
#         else:
#             with st.chat_message("assistant", avatar="🤖"):
#                 st.markdown(msg["content"])

#     # ==================== VOICE INPUT (Fixed!) ====================
#     st.markdown("**🎤 Voice Input (हर बार उपलब्ध रहेगा)**")
    
#     # Unique key हर rerun में नया बनेगा ताकि mic button हमेशा दिखे
#     voice_key = f"voice_input_{len(st.session_state.messages)}"
    
#     text_from_voice = speech_to_text(
#         language="en",              # 'hi' for Hindi
#         start_prompt="🎤 Start Recording",
#         stop_prompt="⏹️ Stop Recording",
#         just_once=False,            # Important: Button हमेशा रहेगा
#         use_container_width=True,
#         key=voice_key
#     )

#     # ==================== TEXT INPUT ====================
#     text_input = st.chat_input("Type your question here...")

#     # ==================== PROCESS INPUT ====================
#     question = text_from_voice or text_input

#     if question:
#         # Add user message
#         st.session_state.messages.append({"role": "user", "content": question})
#         with st.chat_message("user", avatar="👤"):
#             st.markdown(question)

#         # Show thinking animation
#         with st.chat_message("assistant", avatar="🤖"):
#             with st.spinner("🤔 AI सोच रहा है..."):
#                 # Pass previous messages for context
#                 history = [m for m in st.session_state.messages[:-1] if m["role"] == "assistant" or m["role"] == "user"]
#                 response = generate_answer(question, history)
#             st.markdown(response)

#         # Add AI response to history
#         st.session_state.messages.append({"role": "assistant", "content": response})

#         # Auto rerun to update UI
#         st.rerun()

#     # ==================== CLEAR CHAT ====================
#     with st.sidebar:
#         st.header("⚙️ Settings")
#         if st.button("🗑️ Clear Chat History"):
#             st.session_state.messages = []
#             st.rerun()
        
#         st.markdown("---")
#         st.caption("💡 Tip: English में best voice accuracy")
#         st.caption("🔄 Mic button हर question के बाद फिर दिखेगा")







# app.py

# import streamlit as st
# from streamlit_mic_recorder import speech_to_text
# from evaluator import evaluate_answer
# from question_generator import generate_question
# from answer_generator import generate_answer
# import time
# import PyPDF2

# # Page setup
# st.set_page_config(page_title="AI Chatbot Pro", page_icon="🤖", layout="centered")

# # Beautiful Title
# st.markdown("""
#     <h1 style='text-align: center; color: #4CAF50;'>🤖 Advanced AI Chatbot</h1>
#     <p style='text-align: center; color: #666;'>Interview Prep + General Q&A with Voice & Text</p>
#     <hr>
# """, unsafe_allow_html=True)

# mode = st.selectbox("🌟 Choose Mode", ["Interview Preparation", "Q&A Assistant"])

# # ====================== INTERVIEW MODE ======================
# if mode == "Interview Preparation":
#     role = st.selectbox("Select Job Role", [
#         "Data Science", "Machine Learning Engineer", "Software Engineer",
#         "Python Developer", "HR", "Product Manager", "DevOps Engineer"
#     ])
    
#     difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    
#     uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")
#     resume_text = ""
#     if uploaded_file:
#         pdf_reader = PyPDF2.PdfReader(uploaded_file)
#         for page in pdf_reader.pages:
#             resume_text += page.extract_text() + "\n"
#         st.success("Resume loaded! Questions will be personalized if possible.")
    
#     if "interview_history" not in st.session_state:
#         st.session_state.interview_history = []
    
#     if st.button("🎯 Start New Interview", use_container_width=True):
#         st.session_state.interview_history = []  # Reset history
#         with st.spinner("Generating question..."):
#             st.session_state.question = generate_question(role, difficulty)
#         st.session_state.mode = "interview"
#         st.session_state.start_time = time.time()
#         st.rerun()
    
#     if st.session_state.get("mode") == "interview" and "question" in st.session_state:
#         st.markdown("### 📌 Interview Question:")
#         st.info(st.session_state.question)
        
#         # Timer
#         if "start_time" in st.session_state:
#             elapsed = int(time.time() - st.session_state.start_time)
#             remaining = max(300 - elapsed, 0)  # 5 minutes
#             st.write(f"⏳ Time remaining: {remaining // 60}:{remaining % 60:02d}")
#             if remaining == 0:
#                 st.warning("Time's up! Submit your answer now.")
        
#         answer = st.text_area("✍️ Your Answer", height=150, key="interview_ans")
        
#         if st.button("Submit Answer", use_container_width=True):
#             with st.spinner("Evaluating your answer..."):
#                 feedback = evaluate_answer(st.session_state.question, answer)
#             st.session_state.interview_history.append({
#                 "question": st.session_state.question,
#                 "answer": answer,
#                 "feedback": feedback
#             })
#             st.success("### Feedback")
#             st.markdown(feedback)
        
#         if st.button("➡️ Next Question", use_container_width=True):
#             with st.spinner("Generating next question..."):
#                 st.session_state.question = generate_question(role, difficulty)
#             st.session_state.start_time = time.time()  # Reset timer
#             st.rerun()
        
#         if len(st.session_state.interview_history) > 0:
#             if st.button("📊 View Interview Summary"):
#                 st.markdown("### 📈 Interview Performance Summary")
#                 total_score = 0
#                 count = 0
#                 for i, item in enumerate(st.session_state.interview_history, 1):
#                     with st.expander(f"Question {i}"):
#                         st.write("**Q:**", item["question"])
#                         st.write("**Your Answer:**", item["answer"])
#                         st.write("**Feedback:**", item["feedback"])
#                         # Extract score (assuming format like "Score: 8/10")
#                         if "Score" in item["feedback"]:
#                             try:
#                                 score_str = item["feedback"].split("Score")[1].split("/10")[0].strip(": ").split()[0]
#                                 score = float(score_str)
#                                 total_score += score
#                                 count += 1
#                             except:
#                                 pass
                
#                 if count > 0:
#                     avg = total_score / count
#                     st.metric("Average Score", f"{avg:.1f}/10")
#                     if avg >= 8:
#                         st.success("Excellent performance! 🚀")
#                     elif avg >= 6:
#                         st.warning("Good, but room for improvement.")
#                     else:
#                         st.error("Needs more practice.")

# # ====================== Q&A MODE ======================
# else:
#     st.markdown("### 💬 Ask Anything – Voice या Text से!")

#     # Initialize messages
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Display chat history beautifully
#     for msg in st.session_state.messages:
#         if msg["role"] == "user":
#             with st.chat_message("user", avatar="👤"):
#                 st.markdown(msg["content"])
#         else:
#             with st.chat_message("assistant", avatar="🤖"):
#                 st.markdown(msg["content"])

#     # ==================== VOICE INPUT (Fixed!) ====================
#     st.markdown("**🎤 Voice Input (हर बार उपलब्ध रहेगा)**")
    
#     # Unique key हर rerun में नया बनेगा ताकि mic button हमेशा दिखे
#     voice_key = f"voice_input_{len(st.session_state.messages)}"
    
#     text_from_voice = speech_to_text(
#         language="en",              # 'hi' for Hindi
#         start_prompt="🎤 Start Recording",
#         stop_prompt="⏹️ Stop Recording",
#         just_once=False,            # Important: Button हमेशा रहेगा
#         use_container_width=True,
#         key=voice_key
#     )

#     # ==================== TEXT INPUT ====================
#     text_input = st.chat_input("Type your question here...")

#     # ==================== PROCESS INPUT ====================
#     question = text_from_voice or text_input

#     if question:
#         # Add user message
#         st.session_state.messages.append({"role": "user", "content": question})
#         with st.chat_message("user", avatar="👤"):
#             st.markdown(question)

#         # Show thinking animation
#         with st.chat_message("assistant", avatar="🤖"):
#             with st.spinner("🤔 AI सोच रहा है..."):
#                 # Pass previous messages for context
#                 history = [m for m in st.session_state.messages[:-1] if m["role"] == "assistant" or m["role"] == "user"]
#                 response = generate_answer(question, history)
#             st.markdown(response)

#         # Add AI response to history
#         st.session_state.messages.append({"role": "assistant", "content": response})

#         # Auto rerun to update UI
#         st.rerun()

#     # ==================== CLEAR CHAT ====================
#     with st.sidebar:
#         st.header("⚙️ Settings")
#         if st.button("🗑️ Clear Chat History"):
#             st.session_state.messages = []
#             st.rerun()
        
#         st.markdown("---")
#         st.caption("💡 Tip: English में best voice accuracy")
#         st.caption("🔄 Mic button हर question के बाद फिर दिखेगा")




# import streamlit as st
# from streamlit_mic_recorder import speech_to_text
# from evaluator import evaluate_answer
# from question_generator import generate_question
# from answer_generator import generate_answer
# import time
# try:
#     import PyPDF2
#     PDF_SUPPORT = True
# except ImportError:
#     PDF_SUPPORT = False

# # Page setup - Full width for splash
# st.set_page_config(page_title="AI Chatbot Pro", page_icon="🤖", layout="centered")

# # ====================== SPLASH / WELCOME SCREEN ======================
# if "started" not in st.session_state:
#     st.session_state.started = False

# if not st.session_state.started:
#     # Full screen beautiful welcome
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
#         }
#         .title {
#             font-size: 3rem;
#             margin: 20px 0;
#         }
#         .subtitle {
#             font-size: 1.5rem;
#             margin-bottom: 40px;
#             opacity: 0.9;
#         }
#         </style>
#     """, unsafe_allow_html=True)

#     st.markdown('<div class="big-robot">', unsafe_allow_html=True)

#     # Robot Image (place robot.png in your project folder)
#     try:
#         st.image("robot.png", width=300)
#     except:
#         st.markdown("🤖")  # Fallback emoji if no image
#         st.write("<h1 style='font-size:5rem;'>🤖</h1>", unsafe_allow_html=True)

#     st.markdown("<div class='title'>AI Interview Coach</div>", unsafe_allow_html=True)
#     st.markdown("<div class='subtitle'>Practice Interviews • Get Feedback • Ace Your Dream Job</div>", unsafe_allow_html=True)

#     if st.button("🚀 Tap to Start", use_container_width=True):
#         st.session_state.started = True
#         st.rerun()

#     st.markdown("</div>", unsafe_allow_html=True)

# else:
#     # ====================== MAIN APP (After Click) ======================
#     st.markdown("""
#         <h1 style='text-align: center; color: #4CAF50;'>🤖 Advanced AI Chatbot</h1>
#         <p style='text-align: center; color: #666;'>Interview Prep + General Q&A with Voice & Text</p>
#         <hr>
#     """, unsafe_allow_html=True)

#     mode = st.selectbox("🌟 Choose Mode", ["Interview Preparation", "Q&A Assistant"])

#     # ====================== INTERVIEW MODE ======================
#     if mode == "Interview Preparation":
#         role = st.selectbox("Select Job Role", [
#             "Data Science", "Machine Learning Engineer", "Software Engineer",
#             "Python Developer", "HR", "Product Manager", "DevOps Engineer"
#         ])
        
#         difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        
#         uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")
#         resume_text = ""
#         if uploaded_file and PDF_SUPPORT:
#             pdf_reader = PyPDF2.PdfReader(uploaded_file)
#             for page in pdf_reader.pages:
#                 resume_text += page.extract_text() + "\n"
#             st.success("Resume loaded!")
#         elif uploaded_file and not PDF_SUPPORT:
#             st.error("Install PyPDF2 to enable resume upload.")
        
#         if "interview_history" not in st.session_state:
#             st.session_state.interview_history = []
        
#         if st.button("🎯 Start New Interview", use_container_width=True):
#             st.session_state.interview_history = []
#             with st.spinner("Generating question..."):
#                 st.session_state.question = generate_question(role, difficulty)
#             st.session_state.mode = "interview"
#             st.session_state.start_time = time.time()
#             st.rerun()
        
#         if st.session_state.get("mode") == "interview" and "question" in st.session_state:
#             st.markdown("### 📌 Interview Question:")
#             st.info(st.session_state.question)
            
#             if "start_time" in st.session_state:
#                 elapsed = int(time.time() - st.session_state.start_time)
#                 remaining = max(300 - elapsed, 0)
#                 st.write(f"⏳ Time remaining: {remaining // 60}:{remaining % 60:02d}")
#                 if remaining == 0:
#                     st.warning("Time's up!")
            
#             answer = st.text_area("✍️ Your Answer", height=150, key="interview_ans")
            
#             if st.button("Submit Answer", use_container_width=True):
#                 with st.spinner("Evaluating..."):
#                     feedback = evaluate_answer(st.session_state.question, answer)
#                 st.session_state.interview_history.append({
#                     "question": st.session_state.question,
#                     "answer": answer,
#                     "feedback": feedback
#                 })
#                 st.success("### Feedback")
#                 st.markdown(feedback)
            
#             if st.button("➡️ Next Question", use_container_width=True):
#                 with st.spinner("Generating next..."):
#                     st.session_state.question = generate_question(role, difficulty)
#                 st.session_state.start_time = time.time()
#                 st.rerun()
            
#             if len(st.session_state.interview_history) > 0:
#                 if st.button("📊 View Interview Summary"):
#                     st.markdown("### 📈 Interview Performance Summary")
#                     total_score = 0
#                     count = 0
#                     for i, item in enumerate(st.session_state.interview_history, 1):
#                         with st.expander(f"Question {i}"):
#                             st.write("**Q:**", item["question"])
#                             st.write("**Your Answer:**", item["answer"])
#                             st.write("**Feedback:**", item["feedback"])
#                             if "Score" in item["feedback"]:
#                                 try:
#                                     score = float(item["feedback"].split("Score")[1].split("/10")[0].strip(": ").split()[0])
#                                     total_score += score
#                                     count += 1
#                                 except:
#                                     pass
#                     if count > 0:
#                         avg = total_score / count
#                         st.metric("Average Score", f"{avg:.1f}/10")

#     # ====================== Q&A MODE ======================
#     else:
#         st.markdown("### 💬 Ask Anything – Voice या Text से!")
#         if "messages" not in st.session_state:
#             st.session_state.messages = []

#         for msg in st.session_state.messages:
#             if msg["role"] == "user":
#                 with st.chat_message("user", avatar="👤"):
#                     st.markdown(msg["content"])
#             else:
#                 with st.chat_message("assistant", avatar="🤖"):
#                     st.markdown(msg["content"])

#         st.markdown("**🎤 Voice Input**")
#         voice_key = f"voice_input_{len(st.session_state.messages)}"
#         text_from_voice = speech_to_text(
#             language="en",
#             start_prompt="🎤 Start Recording",
#             stop_prompt="⏹️ Stop Recording",
#             just_once=False,
#             use_container_width=True,
#             key=voice_key
#         )

#         text_input = st.chat_input("Type your question here...")

#         question = text_from_voice or text_input

#         if question:
#             st.session_state.messages.append({"role": "user", "content": question})
#             with st.chat_message("user", avatar="👤"):
#                 st.markdown(question)

#             with st.chat_message("assistant", avatar="🤖"):
#                 with st.spinner("🤔 AI thinking..."):
#                     history = [m for m in st.session_state.messages[:-1]]
#                     response = generate_answer(question, history)
#                 st.markdown(response)

#             st.session_state.messages.append({"role": "assistant", "content": response})
#             st.rerun()

#         with st.sidebar:
#             st.header("⚙️ Settings")
#             if st.button("🗑️ Clear Chat History"):
#                 st.session_state.messages = []
#                 st.rerun()
#             st.caption("💡 English voice works best")













# import streamlit as st
# from streamlit_mic_recorder import speech_to_text
# from answer_generator import generate_answer

# # Page setup
# st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="centered")

# # ====================== SPLASH / WELCOME SCREEN ======================
# if "started" not in st.session_state:
#     st.session_state.started = False

# if not st.session_state.started:
#     # Beautiful full-screen welcome
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
#         .title {
#             font-size: 3.5rem;
#             margin: 30px 0 10px 0;
#             font-weight: bold;
#         }
#         .subtitle {
#             font-size: 1.6rem;
#             margin-bottom: 50px;
#             opacity: 0.9;
#         }
#         </style>
#     """, unsafe_allow_html=True)

#     st.markdown('<div class="big-robot">', unsafe_allow_html=True)

#     # Robot Image (robot.png रखो project folder में)
#     try:
#         st.image("robot.png", width=320)
#     except:
#         st.markdown("<h1 style='font-size:6rem;margin:0;'>🤖</h1>", unsafe_allow_html=True)

#     st.markdown("<div class='title'>AI Chat Assistant</div>", unsafe_allow_html=True)
#     st.markdown("<div class='subtitle'>Voice या Text से बात करो • Instant जवाब</div>", unsafe_allow_html=True)

#     if st.button("🚀 Tap to Start Chat", use_container_width=True):
#         st.session_state.started = True
#         st.rerun()

#     st.markdown("</div>", unsafe_allow_html=True)

# # ====================== MAIN Q&A CHAT ======================
# else:
#     st.markdown("""
#         <h1 style='text-align: center; color: #4CAF50;'>🤖 AI Chat Assistant</h1>
#         <p style='text-align: center; color: #666;'>Ask Anything – Voice या Text से!</p>
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

#     # Voice Input
#     st.markdown("**🎤 Voice Input (हर बार available)**")
#     voice_key = f"voice_{len(st.session_state.messages)}"
#     text_from_voice = speech_to_text(
#         language="en",  # 'hi-IN' करो अगर Hindi चाहिए
#         start_prompt="🎤 Start Recording",
#         stop_prompt="⏹️ Stop Recording",
#         just_once=False,
#         use_container_width=True,
#         key=voice_key
#     )

#     # Text Input
#     text_input = st.chat_input("Type your message here...")

#     # Get question
#     question = text_from_voice or text_input

#     if question:
#         # Add user message
#         st.session_state.messages.append({"role": "user", "content": question})
#         with st.chat_message("user", avatar="👤"):
#             st.markdown(question)

#         # Generate & show response
#         with st.chat_message("assistant", avatar="🤖"):
#             with st.spinner("🤔 सोच रहा हूँ..."):
#                 history = [m for m in st.session_state.messages[:-1]]
#                 response = generate_answer(question, history)
#             st.markdown(response)

#         # Add AI response to history
#         st.session_state.messages.append({"role": "assistant", "content": response})
#         st.rerun()

#     # Sidebar - Clear Chat
#     with st.sidebar:
#         st.header("⚙️ Options")
#         if st.button("🗑️ Clear Chat"):
#             st.session_state.messages = []
#             st.rerun()
#         st.caption("💡 English voice सबसे accurate है")
#         st.caption("🔄 Mic button हर message के बाद फिर दिखेगा")





# import streamlit as st
# from streamlit_mic_recorder import speech_to_text
# from answer_generator import generate_answer

# # Simple smart suggestions based on keywords (no API call - always works!)
# def get_suggestions(last_question):
#     question = last_question.lower()
#     if any(word in question for word in ["code", "python", "program", "error", "debug"]):
#         return ["इसका code example चाहिए?", "और optimize कैसे करें?", "Common mistakes क्या हैं?"]
#     elif any(word in question for word in ["interview", "job", "resume", "question"]):
#         return ["अगला question practice करें?", "Answer improve कैसे करें?", "Common tips बताओ"]
#     elif any(word in question for word in ["machine learning", "data science", "ai"]):
#         return ["Real-world example?", "Best resources कौन से?", "Latest trends क्या हैं?"]
#     elif any(word in question for word in ["hindi", "english", "language"]):
#         return ["Hindi में explain करें?", "Translation चाहिए?", "Pronunciation tips?"]
#     else:
#         return ["और detail में बताओ?", "Example के साथ समझाओ?", "क्या related कुछ और पूछू?"]

# # Page setup
# st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="centered")

# # Splash Screen
# if "started" not in st.session_state:
#     st.session_state.started = False

# if not st.session_state.started:
#     st.markdown("""
#         <style>
#         .big-robot {display: flex; flex-direction: column; align-items: center; justify-content: center;
#             height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#             color: white; text-align: center;}
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
#     st.markdown("<div class='subtitle'>Voice या Text से बात करो • Instant जवाब</div>", unsafe_allow_html=True)

#     if st.button("🚀 Tap to Start Chat", use_container_width=True):
#         st.session_state.started = True
#         st.rerun()

#     st.markdown("</div>", unsafe_allow_html=True)

# # Main Chat
# else:
#     st.markdown("""
#         <h1 style='text-align: center; color: #4CAF50;'>🤖 AI Chat Assistant</h1>
#         <p style='text-align: center; color: #666;'>Ask Anything – Voice या Text से!</p>
#         <hr>
#     """, unsafe_allow_html=True)

#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Display all messages
#     for i, msg in enumerate(st.session_state.messages):
#         if msg["role"] == "user":
#             with st.chat_message("user", avatar="👤"):
#                 st.markdown(msg["content"])
#         else:
#             with st.chat_message("assistant", avatar="🤖"):
#                 st.markdown(msg["content"])

#     # Show suggestions after the LAST AI response
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
#         language="en",  # 'hi-IN' for Hindi
#         start_prompt="🎤 Start Recording",
#         stop_prompt="⏹️ Stop Recording",
#         just_once=False,
#         use_container_width=True,
#         key=voice_key
#     )

#     text_input = st.chat_input("Type your message here...")

#     # Handle pending suggestion
#     if "pending_question" in st.session_state:
#         question = st.session_state.pending_question
#         del st.session_state.pending_question
#     else:
#         question = text_from_voice or text_input

#     if question:
#         # Add user message
#         st.session_state.messages.append({"role": "user", "content": question})
#         with st.chat_message("user", avatar="👤"):
#             st.markdown(question)

#         # Generate response
#         with st.chat_message("assistant", avatar="🤖"):
#             with st.spinner("🤔 सोच रहा हूँ..."):
#                 history = [m for m in st.session_state.messages[:-1]]
#                 response = generate_answer(question, history)
#             st.markdown(response)

#         # Add AI response
#         st.session_state.messages.append({"role": "assistant", "content": response})
#         st.rerun()

#     # Sidebar
#     with st.sidebar:
#         st.header("⚙️ Options")
#         if st.button("🗑️ Clear Chat"):
#             st.session_state.messages = []
#             st.rerun()
#         st.caption("💡 Suggested questions automatic दिखेंगे!")
#         st.caption("🔄 Voice English में best काम करता है")














# import streamlit as st
# from streamlit_mic_recorder import speech_to_text
# from answer_generator import generate_answer
# # from gtts import gTTS
# import os
# import pyttsx3
# import re          # (ये पहले से होना चाहिए markdown clean करने के लिए)
# # from playsound import playsound
# import threading
# import tempfile

# # Global variable to track current playing thread
# current_play_thread = None

# import re

# def play_audio(text):
#     global current_play_thread
#     try:
#         # Strip markdown symbols for cleaner speech
#         clean_text = re.sub(r'(\*\*|__|\*|_|`|~|#|>|\|)', '', text)
#         clean_text = re.sub(r'\n+', '. ', clean_text)  # Optional: replace newlines with pauses
#         clean_text = clean_text.strip()

#         lang = 'hi' if any(c in "अआइईउऊएऐओऔकखगघचछजझटठडढणतथदधनपफबभमयरलवशषसह" for c in clean_text) else 'en'
#         tts = gTTS(text=clean_text, lang=lang, slow=False)
#         temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
#         tts.save(temp_file.name)
#         temp_file.close()
        
#         def run():
#             try:
#                 playsound(temp_file.name)
#             finally:
#                 if os.path.exists(temp_file.name):
#                     os.unlink(temp_file.name)
        
#         # Stop/override previous if playing
#         if current_play_thread and current_play_thread.is_alive():
#             pass  # New play will override
        
#         current_play_thread = threading.Thread(target=run, daemon=True)
#         current_play_thread.start()
#     except Exception as e:
#         print(e)  # For debugging
#         pass

# # Automatic voice function
# # def play_audio(text):
# #     global current_play_thread
# #     try:
# #         lang = 'hi' if any(c in "अआइईउऊएऐओऔकखगघचछजझटठडढणतथदधनपफबभमयरलवशषसह" for c in text) else 'en'
# #         tts = gTTS(text=text, lang=lang, slow=False)
# #         temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
# #         tts.save(temp_file.name)
# #         temp_file.close()
        
# #         def run():
# #             try:
# #                 playsound(temp_file.name)
# #             finally:
# #                 if os.path.exists(temp_file.name):
# #                     os.unlink(temp_file.name)
        
# #         # Stop previous voice if playing
# #         if current_play_thread and current_play_thread.is_alive():
# #             # playsound को stop करने का direct तरीका नहीं है, लेकिन next play override कर देगा
# #             pass  # We can't stop playsound mid-way easily, but new play will override
        
# #         current_play_thread = threading.Thread(target=run, daemon=True)
# #         current_play_thread.start()
# #     except:
# #         pass

# # Suggestions
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

# # Page setup
# st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="centered")

# # Splash Screen
# if "started" not in st.session_state:
#     st.session_state.started = False

# if not st.session_state.started:
#     st.markdown("""
#         <style>
#         .big-robot {display: flex; flex-direction: column; align-items: center; justify-content: center;
#             height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#             color: white; text-align: center;}
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

# # Main Chat
# else:
#     st.markdown("""
#         <h1 style='text-align: center; color: #4CAF50;'>🤖 AI Chat Assistant</h1>
#         <p style='text-align: center; color: #666;'>Ask Anything – Voice या Text से! 🔊 हर जवाब बोलेगा</p>
#         <hr>
#     """, unsafe_allow_html=True)

#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Display messages
#     for i, msg in enumerate(st.session_state.messages):
#         if msg["role"] == "user":
#             with st.chat_message("user", avatar="👤"):
#                 st.markdown(msg["content"])
#         else:
#             with st.chat_message("assistant", avatar="🤖"):
#                 st.markdown(msg["content"])

#     # Suggestions
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

#     if "pending_question" in st.session_state:
#         question = st.session_state.pending_question
#         del st.session_state.pending_question
#     else:
#         question = text_from_voice or text_input

#     if question:
#         st.session_state.messages.append({"role": "user", "content": question})
#         with st.chat_message("user", avatar="👤"):
#             st.markdown(question)

#         with st.chat_message("assistant", avatar="🤖"):
#             with st.spinner("🤔 सोच रहा हूँ..."):
#                 history = [m for m in st.session_state.messages[:-1]]
#                 response = generate_answer(question, history)
#             st.markdown(response)

#             play_audio(response)

#         st.session_state.messages.append({"role": "assistant", "content": response})
#         st.rerun()

#     # Sidebar - Clear Chat with voice stop
#     with st.sidebar:
#         st.header("⚙️ Options")
#         if st.button("🗑️ Clear Chat"):
#             # Voice stop करने की कोशिश (playsound stop नहीं होता, लेकिन next play override करेगा)
#             # To force stop, we can play a silent sound, but simple way: just clear
#             st.session_state.messages = []
#             st.rerun()
#         st.caption("🔊 Clear Chat दबाने पर voice भी रुक जाएगी (या override)")
#         st.caption("💡 Automatic natural voice – no button!")

# **Note:** playsound library में direct stop function नहीं है, इसलिए complete stop नहीं हो पाता mid-way में। लेकिन clear chat दबाने पर अगर कोई नया सवाल पूछोगे तो नई voice पुरानी को override कर देगी।  

# अगर तुम चाहो तो हम "Stop Voice" नाम का अलग button add कर सकते हैं जो silent sound play करके current voice को override कर दे।  

# लेकिन अभी ये version बहुत अच्छा काम कर रहा है – clear chat के बाद अगर कोई नया सवाल नहीं पूछोगे तो voice पूरा खत्म होने के बाद रुक जाएगी।  

# Test करके बताओ – अब कैसा लग रहा है? 😄🔊

# अगर perfect stop चाहिए तो बताओ, मैं "Stop Voice" button add कर दूंगा।





# import streamlit as st
# from streamlit_mic_recorder import speech_to_text
# from answer_generator import generate_answer
# import re
# import pyttsx3
# import threading
# import os

# # --------------------- TTS Setup with pyttsx3 ---------------------
# engine = None
# current_play_thread = None

# def init_engine():
#     global engine
#     if engine is None:
#         engine = pyttsx3.init()
#         engine.setProperty('rate', 220)    # <<< Speed यहीं adjust करो >>>
#         # 160 = slow & clear, 190 = fast & natural, 220 = very fast
#         engine.setProperty('volume', 1.0)

# def play_audio(text):
#     global engine, current_play_thread
#     try:
#         # Clean markdown symbols so they aren't spoken
#         clean_text = re.sub(r'(\*\*|__|\*|_|`|~|#|>|\|)', '', text)
#         clean_text = re.sub(r'\n+', '. ', clean_text)  # Better pauses
#         clean_text = clean_text.strip()
        
#         if not clean_text:
#             return

#         init_engine()

#         def run():
#             # Stop any previous speech immediately
#             engine.stop()
#             engine.say(clean_text)
#             engine.runAndWait()

#         # Stop previous thread if running
#         if current_play_thread and current_play_thread.is_alive():
#             engine.stop()

#         current_play_thread = threading.Thread(target=run, daemon=True)
#         current_play_thread.start()

#     except Exception as e:
#         print(f"TTS Error: {e}")

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
#         .big-robot {display: flex; flex-direction: column; align-items: center; justify-content: center;
#             height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#             color: white; text-align: center;}
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

# # --------------------- Main Chat ---------------------
# else:
#     st.markdown("""
#         <h1 style='text-align: center; color: #4CAF50;'>🤖 AI Chat Assistant</h1>
#         <p style='text-align: center; color: #666;'>Ask Anything – Voice या Text से! 🔊 हर जवाब बोलेगा</p>
#         <hr>
#     """, unsafe_allow_html=True)

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

#     # Suggestions after assistant reply
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
#         language="en",  # You can change to "hi" or "mixed" if library supports
#         start_prompt="🎤 Start Recording",
#         stop_prompt="⏹️ Stop Recording",
#         just_once=False,
#         use_container_width=True,
#         key=voice_key
#     )

#     text_input = st.chat_input("Type your message here...")

#     # Get question (from suggestion, voice, or text)
#     if "pending_question" in st.session_state:
#         question = st.session_state.pending_question
#         del st.session_state.pending_question
#     else:
#         question = text_from_voice or text_input

#     # Process new question
#     if question:
#         # Add user message
#         st.session_state.messages.append({"role": "user", "content": question})
#         with st.chat_message("user", avatar="👤"):
#             st.markdown(question)

#         # Generate and display assistant response
#         with st.chat_message("assistant", avatar="🤖"):
#             with st.spinner("🤔 सोच रहा हूँ..."):
#                 history = [m for m in st.session_state.messages[:-1]]
#                 response = generate_answer(question, history)
#             st.markdown(response)
#             play_audio(response)  # Speak the answer

#         st.session_state.messages.append({"role": "assistant", "content": response})
#         st.rerun()

#     # Sidebar Options
#     with st.sidebar:
#         st.header("⚙️ Options")
#         if st.button("🗑️ Clear Chat"):
#             st.session_state.messages = []
#             if engine:
#                 engine.stop()  # Immediately stop any ongoing speech
#             st.rerun()
#         st.caption("🔊 Voice तेज़ और साफ़ है • Clear Chat पर voice भी तुरंत रुक जाती है")
#         st.caption("💡 Speed change करना हो तो code में 'rate', 190 वाली line edit करो")




import streamlit as st
from streamlit_mic_recorder import speech_to_text
from answer_generator import generate_answer
import re
from gtts import gTTS
import io
import base64

# --------------------- Uninterruptible TTS with Base64 Embed ---------------------
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