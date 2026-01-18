import streamlit as st
import speech_recognition as sr
import pandas as pd
import numpy as np
import random
import time

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Interview System", layout="centered")

st.title("🎤 AI Interview System")
st.write("Real-time AI-based Interview Simulation")

# ------------------ DEFAULT DATASET (500 RECORDS) ------------------
@st.cache_data
def load_dataset():
    roles = ["Python Developer", "Data Analyst", "Java Developer", "HR"]
    skills = ["Python", "SQL", "Java", "Communication", "ML"]
    data = []
    for i in range(500):
        data.append({
            "candidate_id": i,
            "role": random.choice(roles),
            "skill": random.choice(skills),
            "difficulty": random.choice(["Easy", "Medium", "Hard"])
        })
    return pd.DataFrame(data)

dataset = load_dataset()

# ------------------ USER INPUT ------------------
name = st.text_input("Enter your name")
role = st.selectbox("Select Job Role", dataset["role"].unique())

st.write("📄 Resume Upload (Optional)")
resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# ------------------ QUESTIONS BANK ------------------
question_bank = {
    "Python Developer": [
        "Explain list and tuple",
        "What is OOP?",
        "Explain exception handling",
        "What is a dictionary?"
    ],
    "Data Analyst": [
        "What is SQL?",
        "Explain joins",
        "What is data cleaning?",
        "Explain pandas"
    ],
    "Java Developer": [
        "What is JVM?",
        "Explain inheritance",
        "What is exception handling?",
        "Difference between abstract and interface"
    ],
    "HR": [
        "Tell me about yourself",
        "What are your strengths?",
        "How do you handle pressure?",
        "Why should we hire you?"
    ]
}

# ------------------ VOICE TO TEXT ------------------
def voice_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙 Speak now...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except:
        return ""

# ------------------ ANSWER EVALUATION ------------------
def evaluate_answer(answer):
    keywords = ["because", "example", "used", "important"]
    score = sum(1 for k in keywords if k in answer.lower())
    return min(score * 25, 100)

def confidence_score(answer):
    words = len(answer.split())
    if words < 10:
        return 40
    elif words < 25:
        return 70
    else:
        return 90

# ------------------ INTERVIEW PROCESS ------------------
if st.button("🎯 Start Interview") and name:
    st.session_state.scores = []
    st.session_state.questions = random.sample(question_bank[role], 3)

    for q in st.session_state.questions:
        st.subheader(f"🤖 AI Question: {q}")
        if st.button(f"🎤 Answer: {q}"):
            answer = voice_to_text()

            if answer:
                st.success(f"Your Answer: {answer}")

                score = evaluate_answer(answer)
                conf = confidence_score(answer)

                st.session_state.scores.append((score, conf))

                st.write(f"📊 Answer Score: {score}/100")
                st.write(f"💬 Confidence Score: {conf}/100")

                # FOLLOW-UP QUESTION
                if score < 50:
                    st.warning("AI Follow-up Question: Can you explain with an example?")
            else:
                st.error("Could not recognize voice")

    # ------------------ FINAL REPORT ------------------
    if st.session_state.scores:
        avg_score = np.mean([s[0] for s in st.session_state.scores])
        avg_conf = np.mean([s[1] for s in st.session_state.scores])

        st.divider()
        st.header("📄 AI Interview Feedback Report")

        st.write(f"👤 Candidate: {name}")
        st.write(f"💼 Role: {role}")
        st.write(f"📈 Technical Score: {int(avg_score)}/100")
        st.write(f"🗣 Confidence Score: {int(avg_conf)}/100")

        if avg_score > 70 and avg_conf > 70:
            st.success("✅ Recommendation: Strong Candidate")
        elif avg_score > 50:
            st.warning("⚠️ Recommendation: Needs Improvement")
        else:
            st.error("❌ Recommendation: Practice More")

# ------------------ INTERVIEW HISTORY ------------------
st.divider()
st.subheader("📊 Interview Dataset Summary")
st.write(dataset.head())
