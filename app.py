import streamlit as st
from state_manager import init_session
from interview_question import generate_question
from evaluate import evaluate_answer
from resume_upload import extract_resume_text
from report import create_pdf
import time
import random
import google.generativeai as genai

st.set_page_config(page_title="InterviewGenie AI", layout="centered")
st.title(" InterviewGenie AI")
st.write("This app asks 10–15 interview questions and scores your answers like a real interviewer.")

st.set_page_config(page_title="InterviewGenie AI", layout="centered")

# API Key Input
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

with st.sidebar.expander("How to get a Gemini API Key"):
    st.markdown("""
    1. Go to **Google AI Studio**: https://aistudio.google.com/
    2. Sign in with your **Google account**.
    3. Click **Get API Key**.
    4. Select **Create API Key**.
    5. Copy the generated key.
    6. Paste it in the **Gemini API Key field above**.
    """)

if not api_key:
    st.warning("Please enter your Gemini API key in the sidebar to start the interview.")
    st.stop()
if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("Please enter your Gemini API key in the sidebar to start.")
    st.stop()
# Inputs
uploaded_resume = st.file_uploader("Upload Resume (PDF or TXT only)", type=["pdf"])
resume_text = ""
if uploaded_resume:
    resume_text = extract_resume_text(uploaded_resume)
    if not resume_text:
        st.warning("Unable to extract text from this file. Please upload a valid PDF")
if resume_text:
    job_description = st.text_area("Paste Job Description")
    difficulty = st.selectbox("Difficulty", ["Easy", "Moderate", "Hard", "Adaptive"])

# Session Init
init_session()

if st.button("Start Interview"):
    st.session_state.questions.clear()
    st.session_state.answers.clear()
    st.session_state.scores.clear()
    st.session_state.feedbacks.clear()
    st.session_state.interview_started = True 
    st.session_state.index = 0
    st.rerun()

# Interview Flow
if st.session_state.interview_started and job_description and resume_text:

    total_questions = random.randint(10, 15)

    if st.session_state.index < total_questions:

        if len(st.session_state.questions) <= st.session_state.index:
            last = st.session_state.scores[-1] if st.session_state.scores else 5
            q = generate_question(job_description, resume_text, difficulty, last)
            st.session_state.questions.append(q)

        q = st.session_state.questions[st.session_state.index]
        st.subheader(f"Q{st.session_state.index + 1}: {q}")

        ans = st.text_area(" Your Answer:", key=f"ans_{st.session_state.index}")

        if st.button("Submit Answer"):
            if ans.strip() == "":
                st.warning("Please enter an answer.")
            else:
                score, feedback = evaluate_answer(job_description, resume_text, q, ans)

                st.session_state.answers.append(ans)
                st.session_state.scores.append(score)
                st.session_state.feedbacks.append(feedback)

                st.success(f"Score: {score}/10")
                st.info(f"Interviewer Feedback: {feedback}")

                with st.empty():
                    for i in range(10, 0, -1):
                        st.write(f"Moving to next question in **{i}** seconds...")
                        time.sleep(1)

                st.session_state.index += 1
                st.rerun()

    else:
        st.success(" Interview Completed!")
        st.subheader(" Final Interview Report")

        for i in range(total_questions):
            st.write(f"###  Q{i+1}: {st.session_state.questions[i]}")
            st.write(f"**Your Answer:** {st.session_state.answers[i]}")
            st.write(f"**Score:** {st.session_state.scores[i]}/10")
            st.write(f"**Interviewer Feedback:** {st.session_state.feedbacks[i]}")
            st.write("---")

        avg = sum(st.session_state.scores) / total_questions
        st.write(f"### Overall Score: **{avg:.2f}/10**")
        pdf = create_pdf(
            st.session_state.questions,
            st.session_state.answers,
            st.session_state.scores,
            st.session_state.feedbacks,
            avg
        )

        st.download_button(
            label="Download Interview Report (PDF)",
            data=pdf,
            file_name="Interview_Report.pdf",
        mime="application/pdf"
        )

