import streamlit as st
import PyPDF2
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI-Based Interview Evaluation System",
    page_icon="🎯",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.main { background-color: #f5f7fb; }
.header {
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    padding: 30px;
    border-radius: 12px;
    color: white;
    font-size: 32px;
    font-weight: bold;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="header">
AI-Based Interview Evaluation System
<div style="font-size:16px;">Upload resume and attend AI interview</div>
</div>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS (UNCHANGED) ----------------
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_name(text):
    lines = text.split("\n")
    for line in lines[:6]:
        if len(line.split()) <= 3:
            return line.strip()
    return "Candidate"

def extract_skills(text):
    skills = ["Python", "SQL", "Machine Learning", "Java", "C"]
    return [s for s in skills if s.lower() in text.lower()]

def generate_scores(answer_text):
    tech = random.randint(25, 40)
    comm = random.randint(12, 20)
    conf = random.randint(10, 15)
    final = tech + comm + conf
    return tech, comm, conf, final

# ---------------- UI LAYOUT ----------------
col1, col2 = st.columns([1, 2])

# -------- LEFT: RESUME UPLOAD --------
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📄 Upload Resume")
    resume = st.file_uploader("Choose PDF", type=["pdf"])
    analyze = st.button("Analyze Resume")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- MAIN LOGIC ----------------
if resume and analyze:
    text = extract_text_from_pdf(resume)
    name = extract_name(text)
    skills = extract_skills(text)

    # Resume analysis (UNCHANGED)
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Resume Analysis")
        st.write(f"**Name:** {name}")
        st.write(f"**Skills:** {', '.join(skills)}")
        st.write("**Education:** B.E / B.Tech")
        st.write("**Project:** AI Interview Evaluation System")
        st.markdown("</div>", unsafe_allow_html=True)

    # -------- INTERVIEW SECTION (MODIFIED) --------
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🎥 Interview Simulation")

        c1, c2 = st.columns(2)

        # AI HR AVATAR
        with c1:
            st.image("hr_avatar.jpeg", caption="AI HR")
            st.info("Tell me about yourself")

        # USER CAMERA
        with c2:
            user_img = st.camera_input("Rahul - Webcam")

        st.markdown("</div>", unsafe_allow_html=True)

        # -------- MIC INPUT --------
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🎙 Answer using Mic")
        audio = st.audio_input("Speak now")

        answer_text = st.text_area("Or type your answer")

        if st.button("Submit Answer"):
            tech, comm, conf, final = generate_scores(answer_text)

            # HR RESPONSE
            st.success("AI HR: Thank you for your answer.")

            # SCORE
            st.markdown("### 📊 Score Breakdown")
            st.write(f"Technical: **{tech}/40**")
            st.write(f"Communication: **{comm}/20**")
            st.write(f"Confidence: **{conf}/15**")
            st.markdown(f"## 🏆 Final Score: **{final}/100**")

            # SUGGESTIONS
            st.markdown("### 📝 Suggestions")
            st.write("✅ Good explanation")
            st.write("⚠️ Improve eye contact")
            st.write("💡 Speak more confidently")

        st.markdown("</div>", unsafe_allow_html=True)

else:
    with col2:
        st.info("Upload resume and click Analyze Resume to start interview")
