import streamlit as st
import speech_recognition as sr
import pyttsx3
from PIL import Image
import numpy as np

# ---------------- HR SPEECH ----------------
def hr_speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# ---------------- PAGE ----------------
st.title("🎤 AI Interview Evaluation System")

# ---------------- HR AVATAR ----------------
col1, col2 = st.columns([1,3])

with col1:
    st.image("hr_avatar.png", width=150)

with col2:
    st.markdown("### 🤖 AI HR Interviewer")
    st.write("Welcome! This interview simulates a real HR round.")

# ---------------- QUESTION ----------------
question = "Tell me about yourself"
st.info(f"HR: {question}")

if st.button("🔊 HR Ask Question"):
    hr_speak(question)

# ---------------- WEBCAM (NO OPENCV) ----------------
st.subheader("📷 Face Capture")
img = st.camera_input("Keep your face in front of the camera")

confidence_score = 5
if img:
    st.success("Face captured successfully")
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
        st.success("Converted Text:")
        st.write(answer_text)
    except:
        st.error("Speech not recognized")

# ---------------- SCORE + FEEDBACK ----------------
if st.button("📊 Submit Interview"):
    if answer_text == "":
        st.warning("Please answer the question first")
    else:
        words = len(answer_text.split())
        communication = min(20, words // 2)
        technical = 20
        confidence = confidence_score

        final_score = communication + technical + confidence

        st.subheader("📊 Score Breakdown")
        st.write(f"🗣 Communication: {communication}/20")
        st.write(f"😌 Confidence: {confidence}/15")
        st.write(f"💻 Technical: {technical}/20")

        st.markdown(f"## ✅ Final Score: **{final_score}/100**")

        st.subheader("💡 HR Suggestions")

        if communication < 10:
            st.write("- Improve clarity and sentence formation")
        if confidence < 10:
            st.write("- Maintain eye contact and posture")
        if final_score >= 60:
            st.success("Good interview performance!")
        else:
            st.warning("Needs improvement. Practice mock interviews.")

        hr_speak("Thank you. Your interview is completed.")
