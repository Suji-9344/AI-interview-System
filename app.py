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
    st.write("Welcome! This is a real-time AI-based interview simulation.")

# ---------------- HR QUESTION ----------------
question = "Tell me about yourself"
st.info(f"**HR:** {question}")

# ---------------- CAMERA ----------------
st.subheader("📷 Face Capture")
img = st.camera_input("Keep your face steady while answering")

confidence_score = 5
if img:
    st.success("Face detected")
    confidence_score = 15

# ---------------- SPEECH TO TEXT ----------------
st.subheader("🎙️ Speak Your Answer")

answer_text = ""

if st.button("🎤 Record Answer"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = r.listen(source)

    try:
        answer_text = r.recognize_google(audio)
        st.success("Converted Text")
        st.write(answer_text)
    except:
        st.error("Speech not recognized. Try again.")

# ---------------- INTERVIEW EVALUATION ----------------
if st.button("📊 Submit Interview"):
    if answer_text == "":
        st.warning("Please answer the question")
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
            st.write("• Improve clarity and structured answers")
        if confidence < 10:
            st.write("• Maintain eye contact and calm posture")
        if final_score >= 60:
            st.success("Good performance! You are interview ready.")
        else:
            st.warning("Needs improvement. Practice mock interviews.")

        st.info("🤖 HR: Thank you. Your interview is completed.")
