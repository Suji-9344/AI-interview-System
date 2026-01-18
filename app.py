import streamlit as st
import pandas as pd
import numpy as np
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Interview System", layout="centered")

st.title("🤖 AI Interview System")
st.write("Resume-based Intelligent Interview Simulation")

# ---------------- DEFAULT DATASET (500 RECORDS) ----------------
@st.cache_data
def load_dataset():
    roles = ["Python Developer", "Data Analyst", "Java Developer", "HR"]
    skills = ["Python", "SQL", "Java", "ML", "Communication"]
    data = []
    for i in range(500):
        data.append({
            "ID": i,
            "Role": random.choice(roles),
            "Skill": random.choice(skills),
            "Difficulty": random.choice(["Easy", "Medium", "Hard"])
        })
    return pd.DataFrame(data)

dataset = load_dataset()

# ---------------- USER INPUT ----------------
name = st.text_input("Enter Candidate Name")
role = st.selectbox("Select Job Role", dataset["Role"].unique())

resume = st.file_uploader("Upload Resume (Optional)", type=["pdf"])

# ---------------- QUESTION BANK ----------------
question_bank = {
    "Python Developer": [
        "Explain list and tuple",
        "What is OOP?",
        "Explain exception handling"
    ],
    "Data Analyst": [
        "What is SQL?",
        "Explain joins",
        "What is data cleaning?"
    ],
    "Java Developer": [
        "What is JVM?",
        "Explain inheritance",
        "What is polymorphism?"
    ],
    "HR": [
        "Tell me about yourself",
        "What are your strengths?",
        "How do you handle pressure?"
    ]
}

# ---------------- SCORING FUNCTIONS ----------------
def evaluate_answer(answer):
    keywords = ["example", "used", "because", "important"]
    score = sum(1 for k in keywords if k in answer.lower())
    return min(score * 25, 100)

def confidence_score(answer):
    length = len(answer.split())
    if length < 10:
        return 40
    elif length < 25:
        return 70
    else:
        return 90

# ---------------- INTERVIEW ----------------
if st.button("🎯 Start Interview") and name:
    st.session_state.results = []

    questions = random.sample(question_bank[role], 3)

    for q in questions:
        st.subheader(f"🤖 Question: {q}")
        answer = st.text_area("Your Answer", key=q)

        if answer:
            score = evaluate_answer(answer)
            conf = confidence_score(answer)

            st.write(f"📊 Answer Score: {score}/100")
            st.write(f"💬 Confidence Score: {conf}/100")

            if score < 50:
                st.warning("Follow-up: Can you explain with an example?")

            st.session_state.results.append((score, conf))

    # ---------------- FINAL REPORT ----------------
    if st.session_state.results:
        avg_score = int(np.mean([r[0] for r in st.session_state.results]))
        avg_conf = int(np.mean([r[1] for r in st.session_state.results]))

        st.divider()
        st.header("📄 AI Interview Feedback Report")
        st.write(f"👤 Candidate: {name}")
        st.write(f"💼 Role: {role}")
        st.write(f"📈 Technical Score: {avg_score}/100")
        st.write(f"🗣 Confidence Score: {avg_conf}/100")

        if avg_score > 70 and avg_conf > 70:
            st.success("✅ Recommendation: Strong Candidate")
        elif avg_score > 50:
            st.warning("⚠️ Recommendation: Needs Improvement")
        else:
            st.error("❌ Recommendation: Practice More")

# ---------------- DATASET VIEW ----------------
st.divider()
st.subheader("📊 Default Dataset (500 Samples)")
st.dataframe(dataset.head())
