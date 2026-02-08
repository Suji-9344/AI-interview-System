import streamlit as st
import cv2
import numpy as np
import speech_recognition as sr
import pyttsx3
from PIL import Image
import time

# ---------------- HR SPEECH FUNCTION ----------------
def hr_speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# ---------------- PAGE TITLE ----------------
st.markdown("## 🎤 AI Interview Simulation")

# ---------------- HR AVATAR ----------------
col1, col2 = st.columns([1,3])

with col1:
    st.image("hr_avatar.jpeg", width=150)

with col2:
    st.markdown("### 🤖 AI HR Interviewer")
    st.write("Please answer the questions honestly.")

# ---------------- HR QUESTION ----------------
question = "Tell me about yourself"
st.info(f"HR: {question}")

if st.button("🔊 HR Ask Question"):
    hr_speak(question)

# ---------------- WEBCAM CAPTURE ----------------
st.subheader("📷 Capture Face")

img_file = st.camera_input("Look into the camera")

face_score = 0
if img_file:
    img = Image.open(img_file)
    img_np = np.array(img)

    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        st.success("✅ Face detected")
        face_score = 15
    else:
        st.warning("⚠️ Face not detected")
        face_score = 5

# ---------------- SPEECH TO TEXT ----------------
st.subheader("🎙️ Answer (Speak & Submit)")

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
        st.error("Could not recognize speech")

# ---------------- SCORE PREDICTION ----------------
if st.button("📊 Submit Answer"):
    if answer_text == "":
        st.warning("Please answer first")
    else:
        length_score = min(len(answer_text.split()), 40)
        communication = min(20, length_score // 2)
        confidence = face_score
        technical = 20  # dummy for now

        final_score = communication + confidence + technical

        st.subheader("📊 Interview Score")

        st.write(f"🗣 Communication: {communication}/20")
        st.write(f"😌 Confidence: {confidence}/15")
        st.write(f"💻 Technical: {technical}/20")
        st.markdown(f"## ✅ Final Score: **{final_score}/100**")

        # ---------------- SUGGESTIONS ----------------
        st.subheader("💡 HR Suggestions")

        if communication < 10:
            st.write("- Improve clarity and sentence structure")
        if confidence < 10:
            st.write("- Maintain eye contact and posture")
        if final_score > 60:
            st.success("Good performance! Keep practicing mock interviews.")
        else:
            st.warning("Needs improvement. Practice speaking confidently.")

        hr_speak("Thank you. Your interview is completed.")
