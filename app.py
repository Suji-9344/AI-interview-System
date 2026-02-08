import streamlit as st
import speech_recognition as sr

st.set_page_config(page_title="AI Interview System", layout="centered")

st.title("🎤 AI-Based Interview Evaluation System")

# ---------------- HR AVATAR ----------------
col1, col2 = st.columns([1, 3])
with col1:
    st.image("hr_avatar.jpeg", width=130)
with col2:
    st.markdown("### 🤖 AI HR Interviewer")
    st.write("Welcome! This simulates a real interview process.")

# ---------------- RESUME INPUT (TEXT) ----------------
st.subheader("📄 Resume Details")
candidate_name = st.text_input("Enter your name")
skills_text = st.text_area("Enter your skills (comma separated)")

skills = [s.strip() for s in skills_text.split(",") if s.strip()]

if candidate_name:
    st.success(f"Candidate Name: {candidate_name}")
    st.write("Skills:", ", ".join(skills))

# ---------------- HR QUESTION ----------------
if candidate_name:
    question = f"Hello {candidate_name}, tell me about yourself."
    st.info(f"**HR:** {question}")

# ---------------- CAMERA ----------------
st.subheader("📷 Confidence Check")
img = st.camera_input("Keep your face in front of the camera")

confidence_score = 5
if img:
    st.success("Face detected")
    confidence_score = 15

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
        st.success("Speech converted to text")
        st.write(answer_text)
    except:
        st.error("Speech recognition failed")

# ---------------- EVALUATION ----------------
if st.button("📊 Submit Interview"):
    if not answer_text:
        st.warning("Please upload your answer audio")
    else:
        word_count = len(answer_text.split())

        communication = min(30, word_count // 2)
        confidence = confidence_score
        technical = 20 if any(skill.lower() in answer_text.lower() for skill in skills) else 10

        final_score = communication + confidence + technical

        st.subheader("📊 Interview Result")
        st.write(f"🗣 Communication: {communication}/30")
        st.write(f"😌 Confidence: {confidence}/15")
        st.write(f"💻 Technical: {technical}/20")

        st.markdown(f"## ✅ Final Score: **{final_score}/100**")

        st.subheader("💡 HR Suggestions")
        if communication < 15:
            st.write("• Improve clarity and sentence structure")
        if confidence < 10:
            st.write("• Maintain eye contact and calm posture")
        if technical < 15:
            st.write("• Include more technical keywords")

        st.info("🤖 HR: Thank you. Interview completed.")
