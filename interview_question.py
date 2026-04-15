from gemini_utils import call_groq, extract_json
import streamlit as st

def generate_question(job_description, resume_text, difficulty, last_score):
    # Determine difficulty
    if difficulty != "Adaptive":
        level = difficulty
    else:
        if last_score >= 8:
            level = "Hard"
        elif last_score <= 4:
            level = "Easy"
        else:
            level = "Moderate"

    previous_questions = "\n".join(st.session_state.questions)

    prompt = f"""
You are a professional Interview Question Generator for a fresher candidate.

JOB DESCRIPTION:
{job_description}

CANDIDATE RESUME:
{resume_text}

DIFFICULTY level: {level}

Previously Asked Questions:
{previous_questions}

Rules:
- Generate 1 new interview question which is not in previously asked questions.
- the candidate is fresher, ask only fresher questions
- Maximum 1–2 lines.
- Must NOT repeat or rephrase previous questions.
- Must be job-specific based on resume + JD.
- 80% technical questions, 20% behavioral.
- Return ONLY the question text.
"""
    return call_groq(prompt).strip()
