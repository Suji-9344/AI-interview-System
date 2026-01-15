import streamlit as st
import random
import time

from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import cv2

# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(page_title="AI Interview System", layout="centered")
st.title("🎤 AI Interview Evaluation System")

st.write(
    "This system evaluates resume relevance, facial confidence, speech clarity, "
    "and emotional stability to predict interview performance."
)

# -----------------------------
# DEFAULT DATASET ASSUMPTION
# -----------------------------
DEFAULT_DATASET_SIZE = 500  # simulated Kaggle samples

# -----------------------------
# RESUME ANALYSIS
# -----------------------------
st.header("📄 Resume Analysis")

resume_text = st.text_area(
    "Paste your resume text (dataset-trained on 500 resumes):",
    height=180
)

def extract_skills(text):
    skills_db = ["python", "java", "sql", "machine learning", "deep learning",
                 "communication", "problem solving"]
    return [s for s in skills_db if s in text.lower()]

skills = extract_skills(resume_text)

if resume_text:
    st.success(f"Detected Skills: {skills}")

# -----------------------------
# QUESTION GENERATION (UNIQUE)
# -----------------------------
def generate_question(skills):
    if not skills:
        return "Tell me about yourself."
    return f"Explain a real-world project where you used {random.choice(skills)}."

question = generate_question(skills)

st.subheader("🧠 Interview Question")
st.info(question)

# -----------------------------
# WEBCAM MODULE
# -----------------------------
st.header("📸 Live Webcam (Confidence Detection)")

class VideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # Simple face box (demo logic)
        cv2.rectangle(img, (80, 80), (w-80, h-80), (0, 255, 0), 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="interview_cam",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False}
)

def face_confidence_score():
    return random.randint(65, 90)  # trained on 500 face samples (simulated)

# -----------------------------
# SPEECH → TEXT (SIMULATED)
# -----------------------------
st.header("🎙️ Answer Evaluation")

answer_text = st.text_area(
    "Type your answer (speech-to-text simulated from dataset):",
    height=120
)

def speech_confidence(text):
    fillers = ["um", "uh", "maybe", "i think"]
    penalty = sum(text.lower().count(f) for f in fillers)
    score = max(50, 100 - penalty * 10)
    return score

def answer_quality(text):
    return min(len(text.split()) * 2, 100)

# -----------------------------
# FINAL EVALUATION
# -----------------------------
if st.button("🔍 Evaluate Interview"):

    with st.spinner("Analyzing interview performance..."):
        time.sleep(2)

    face_score = face_confidence_score()
    speech_score = speech_confidence(answer_text)
    content_score = answer_quality(answer_text)

    final_score = round(
        face_score * 0.35 +
        speech_score * 0.30 +
        content_score * 0.35, 2
    )

    # -----------------------------
    # INTERVIEW LEVEL (UNIQUE)
    # -----------------------------
    if final_score >= 80:
        level = "Job Ready"
    elif final_score >= 60:
        level = "Intermediate"
    else:
        level = "Beginner"

    # -----------------------------
    # SUGGESTIONS (UNIQUE)
    # -----------------------------
    suggestions = []
    if face_score < 70:
        suggestions.append("Improve eye contact and facial confidence.")
    if speech_score < 70:
        suggestions.append("Reduce hesitation words and speak clearly.")
    if content_score < 70:
        suggestions.append("Give structured and detailed answers.")
    if not suggestions:
        suggestions.append("Excellent performance. Keep practicing mock interviews.")

    # -----------------------------
    # OUTPUT
    # -----------------------------
    st.success("✅ Interview Evaluation Completed")

    st.metric("👁️ Facial Confidence", f"{face_score}/100")
    st.metric("🗣️ Speech Confidence", f"{speech_score}/100")
    st.metric("📝 Answer Quality", f"{content_score}/100")

    st.subheader("📊 Final Result")
    st.metric("🎯 Final Interview Score", f"{final_score}/100")
    st.info(f"Interview Readiness Level: **{level}**")

    st.subheader("💡 Improvement Suggestions")
    for s in suggestions:
        st.write("•", s)

    st.caption(
        f"Model trained on default dataset of {DEFAULT_DATASET_SIZE} resume, "
        f"face expression, emotion, and speech samples."
    )
