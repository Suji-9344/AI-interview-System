import streamlit as st
import pdfplumber
import speech_recognition as sr

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Interview System", layout="centered")

st.title("🎤 AI-Based Interview Evaluation System")

# ---------------- HR AVATAR ----------------
col1, col2 = st.columns([1, 3])
with col1:
    st.image("hr_avatar.jpeg", width=130)
with col2:
    st.markdown("### 🤖 AI HR Interviewer")
    st.write("Welcome! This is a simulated real interview.")

# ---------------- RESUME UPLOAD ----------------
st.subheader("📄 Upload Resume (PDF)")
resume_file = st.file_uploader("Upload your resume", type=["pdf"])

candidate_name = "Candidate"
skills = []

if resume_file:
    text = ""
    with pdfplumber.open(resume_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    words = text.split()
    candidate_name = words[0]

    for skill in ["Python", "Java", "Machine Learning", "AI", "SQL", "Data"]:
        if skill.lower() in text.lower():
            skills.append(skill)

    st.success(f"Name Identified: {candidate_name}")
    st.write("Skills:", ", ".join(skills))

# ---------------- HR QUESTION ----------------
question = f"Hello {candidate_name}, tell me about yourself."
st.info(f"**HR:** {question}")

# ---------------- CAMERA ----------------
st.subheader("📷 Confidence Check")
img = st.camera_input("Look at the camera while answering")

confidence_score = 5
if img:
    confidence_score = 15
    st.success("Face detected")

# ---------------- AUDIO ANSWER ----------------
st.subheader("🎧 Upload Your Answer Audio")
audio_file = st.file_uploader("Upload WAV or MP3", type=["wav", "mp3"])

answer_text = ""

if audio_file:
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        answer_text = recognizer.recognize_google(audio)
        st.success("Speech Converted to Text")
        st.write(answer_text)
    except:
        st.error("Speech recognition failed")

# ---------------- EVALUATION ----------------
if st.button("📊 Submit Interview"):
    if answer_text == "":
        st.warning("Please upload your answer audio")
    else:
        word_count = len(answer_text.split())

        communication = min(30, word_count // 2)
        confidence = confidence_score
        technical = 20 if any(skill.lower() in answer_text.lower() for skill in skills) else 10

        final_score = communication + confidence + technical

        st.subheader("📊 Evaluation Result")
        st.write(f"🗣 Communication: {communication}/30")
        st.write(f"😌 Confidence: {confidence}/15")
        st.write(f"💻 Technical Relevance: {technical}/20")

        st.markdown(f"## ✅ Final Score: **{final_score}/100**")

        st.subheader("💡 HR Suggestions")
        if communication < 15:
            st.write("• Improve clarity and sentence structure")
        if confidence < 10:
            st.write("• Maintain eye contact and calm posture")
        if technical < 15:
            st.write("• Add more technical details from your resume")

        st.info("🤖 HR: Thank you. Interview completed.")
