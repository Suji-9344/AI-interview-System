import streamlit as st
import speech_recognition as sr
from PIL import Image

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Interview System", layout="centered")

# ---------------- HEADER ----------------
st.title("🎤 AI Interview Evaluation System")

col1, col2 = st.columns([1, 3])

with col1:
    st.image("hr_avatar.jpeg", width=140)

with col2:
    st.markdown("### 🤖 AI HR Interviewer")
    st.write("Welcome! This simulates a real interview environment.")

# ---------------- HR QUESTION ----------------
question = "Tell me about yourself"
st.info(f"**HR:** {question}")

# ---------------- CAMERA ----------------
st.subheader("📷 Face Capture")
img = st.camera_input("Keep your face steady")

confidence_score = 5
if img:
    st.success("Face captured successfully")
    confidence_score = 15

# ---------------- AUDIO UPLOAD (REPLACES MIC) ----------------
st.subheader("🎧 Upload Your Answer (Audio)")

audio_file = st.file_uploader(
    "Upload WAV or MP3 file",
    type=["wav", "mp3"]
)

answer_text = ""

if audio_file is not None:
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

    try:
        answer_text = recognizer.recognize_google(audio_data)
        st.success("Converted Text")
        st.write(answer_text)
    except:
        st.error("Could not recognize speech")

# ---------------- INTERVIEW EVALUATION ----------------
if st.button("📊 Submit Interview"):
    if answer_text == "":
        st.warning("Please upload your answer audio")
    else:
        words = len(answer_text.split())

        communication = min(25, words // 2)
        confidence = confidence_score
        technical = 20

        final_score = communication + confidence + technical

        st.subheader("📊 Score Analysis")
        st.write(f"🗣 Communication: {communication}/25")
        st.write(f"😌 Confidence: {confidence}/15")
        st.write(f"💻 Technical Knowledge: {technical}/20")

        st.markdown(f"## ✅ Final Score: **{final_score}/100**")

        st.subheader("💡 HR Suggestions")

        if communication < 10:
            st.write("• Improve clarity and sentence structure")
        if confidence < 10:
            st.write("• Maintain eye contact and calm posture")
        if final_score >= 60:
            st.success("Good interview performance!")
        else:
            st.warning("Needs improvement. Practice mock interviews.")

        st.info("🤖 HR: Thank you. Interview completed.")
