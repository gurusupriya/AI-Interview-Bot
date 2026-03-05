import streamlit as st

def init_session():
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "answers" not in st.session_state:
        st.session_state.answers = []
    if "scores" not in st.session_state:
        st.session_state.scores = []
    if "feedbacks" not in st.session_state:
        st.session_state.feedbacks = []
    if "index" not in st.session_state:
        st.session_state.index = 0
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False
