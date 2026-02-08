import streamlit as st
import pdfplumber
import re
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI-Based Interview Evaluation System",
    page_icon="🎯",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}

.header {
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    padding: 35px;
    border-radius: 12px;
    color: white;
    font-size: 34px;
    font-weight: bold;
}

.subtext {
    font-size: 16px;
    margin-top: 8px;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-top: 20px;
}

.stButton>button {
    background-color: #ef4444;
    color: white;
    padding: 12px 25px;
    border-radius: 8px;
    font-size: 16px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="header">
AI-Based Interview Evaluation System
<div class="subtext">Upload your resume to get started</div>
</div>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def extract_name(text):
    lines = text.split("\n")
    for line in lines[:5]:  # mostly name is in top
        if len(line.split()) <= 3:
            return line.strip()
    return "Candidate"


def extract_skills(text):
    skill_list = ["Python", "SQL", "Machine Learning", "Java", "C", "Data Science"]
    found_skills = [skill for skill in skill_list if skill.lower() in text.lower()]
    return found_skills


def generate_scores(skills):
    base = 60
    tech_score = min(40, 20 + len(skills) * 5)
    comm_score = random.randint(12, 18)
    conf_score = random.randint(10, 14)

    final_score = tech_score + comm_score + conf_score
    return tech_score, comm_score, conf_score, final_score


# ---------------- MAIN CONTENT ----------------
col1, col2 = st.columns([1, 2])

# -------- LEFT SIDE --------
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📄 Upload Your Resume")
    resume = st.file_uploader("Browse files", type=["pdf"])
    analyze = st.button("Analyze Resume")
    st.markdown("</div>", unsafe_allow_html=True)

# -------- RIGHT SIDE --------
if resume and analyze:
    text = extract_text_from_pdf(resume)
    name = extract_name(text)
    skills = extract_skills(text)

    tech, comm, conf, final = generate_scores(skills)

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Resume Analysis")
        st.write(f"**Name:** {name}")
        st.write(f"**Skills:** {', '.join(skills) if skills else 'Not Detected'}")
        st.write("**Education:** B.E / B.Tech")
        st.write("**Project:** AI-Based Interview System")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🎥 Interview Simulation")

        c1, c2 = st.columns(2)
        with c1:
            st.info("👔 AI HR\n\nTell me about yourself")
        with c2:
            st.success(f"🎧 {name}\n\nAnswering...")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 Score Breakdown")

        st.write(f"Technical: **{tech} / 40**")
        st.write(f"Communication: **{comm} / 20**")
        st.write(f"Confidence: **{conf} / 15**")

        st.markdown(f"### 🏆 Final Score: **{final} / 100**")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📝 Feedback & Suggestions")

        st.write("✅ **Strengths:** Good technical understanding")
        st.write("⚠️ **Improvements:** Improve eye contact and fluency")
        st.write("💡 **Tip:** Practice mock interviews regularly")

        st.markdown("</div>", unsafe_allow_html=True)

else:
    with col2:
        st.info("👆 Upload resume and click **Analyze Resume** to start")

