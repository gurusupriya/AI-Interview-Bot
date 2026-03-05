from gemini_utils import call_gemini, extract_json

def evaluate_answer(job_description, resume_text, question, answer):
    if len(answer.strip()) < 4:
        return 2, "Your answer is extremely short. Please try to explain your thoughts more clearly."

    prompt = f"""
You are a friendly and supportive interviewer evaluating a *fresher* candidate.

Focus on **encouraging their confidence**, while still giving fair evaluation based on:

1️ Relevance to the job description  
2️ Correctness and basic understanding  
3️ Logical reasoning and clarity  
4️ Effort shown in the answer  
5️ Communication quality  

JOB DESCRIPTION:
{job_description}

CANDIDATE RESUME:
{resume_text}

QUESTION ASKED:
{question}

ANSWER GIVEN:
{answer}

SCORING RULES (More supportive for freshers):
- **9–10** → Strong answer: correct, relevant, well communicated, shows clear understanding  
- **7–8** → Good attempt: mostly correct but could use small improvements  
- **5–6** → Shows effort but needs more clarity or connection to the topic  
- **3–4** → Limited understanding; encourage learning with guidance  
- **1–2** → Very short or irrelevant; offer supportive advice  

Your response MUST be **valid JSON ONLY** in this exact format:
{{
  "score": <integer 1–10>,
  "feedback": "<2–3 motivating sentences: highlight strengths first, then suggest one improvement politely. Sound like a helpful mentor, not strict evaluator>"
}}
"""

    raw = call_gemini(prompt)
    parsed = extract_json(raw)

    if parsed:
        return parsed["score"], parsed["feedback"]

    # fallback scoring
    length = len(answer)
    if length < 40:
        return 4, "Your answer is okay, but it needs more real examples and clarity."
    elif length < 80:
        return 6, "Good explanation. Try to structure it more clearly."
    else:
        return 8, "Strong and well-structured answer!"
