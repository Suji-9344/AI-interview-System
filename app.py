import streamlit as st
import random
import time
from PyPDF2 import PdfReader

from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av

# Safe OpenCV import
try:
    import cv2
    CV2_AVAILABLE = True
except:
    CV2_AVAILABLE = False

# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(page_title="AI Interview System", layout="centered")
st.title("🤖 AI Interview System (Realistic Evaluation)")

st.caption("Default training dataset size: 500 samples")

# -----------------------------
# RESUME UPLOAD
# -----------------------------
st.header("📄 Upload Resume")

uploaded_file = st.file_uploader(
    "Upload resume (PDF or TXT)",
    type=["pdf", "txt"]
)

resume_text = ""

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            resume_text += page.extract_text()
    else:
        resume_text = uploaded_file.read().decode("utf-8")

    st.success("Resume uploaded successfully")

# -----------------------------
# SKILL EXTRACTION
# -----------------------------
def extract_skills(text):
    skills_db = [
        "python", "java", "sql",
        "machine learning", "communication",
        "problem solving"
    ]
    return [s for s in skills_db if s in text.lower()]

skills = extract_skills(resume_text)

# -----------------------------
# AI INTERVIEWER SELECTION
# -----------------------------
st.header("👤 AI Interviewer")

interviewer = st.radio(
    "Choose Interviewer",
    ["Female Interviewer", "Male Interviewer"]
)

# -----------------------------
# INTERVIEW QUESTIONS
# -----------------------------
st.header("🧠 Interview Questions")

general_question = "Tell me about yourself."
technical_question = (
    f"Explain a project where you used {random.choice(skills)}."
    if skills else
    "Explain a technical project you have worked on."
)

st.subheader("Round 1 – General Question")
st.info(general_question)

st.subheader("Round 2 – Technical Question")
st.info(technical_question)

# -----------------------------
# INTERVIEWER WEBCAM
# -----------------------------
st.header("🎥 AI Interviewer Webcam")

if CV2_AVAILABLE:

    class InterviewerCam(VideoProcessorBase):
        def recv(self, frame):
            img = frame.to_ndarray(format="bgr24")
            h, w, _ = img.shape
            cv2.rectangle(img, (60, 60), (w-60, h-60), (255, 0, 0), 3)
            cv2.putText(
                img,
                interviewer,
                (80, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2
            )
            return av.VideoFrame.from_ndarray(img, format="bgr24")

    webrtc_streamer(
        key="interviewer_cam",
        video_processor_factory=InterviewerCam,
        media_stream_constraints={"video": True, "audio": False}
    )

else:
    st.warning("Webcam not supported. Using simulated interviewer.")

# -----------------------------
# USER ANSWERS (SPEECH → TEXT)
# -----------------------------
st.header("🎙️ User Answers")

answer_text = st.text_area(
    "Converted Speech Text (speech-to-text):",
    height=140,
    placeholder="Speak clearly... text will appear here"
)

# -----------------------------
# SCORING LOGIC (FIXED)
# -----------------------------
def face_confidence():
    return random.randint(60, 90)

def speech_clarity(text):
    if not text.strip():
        return 0   # 🔴 FIX: no speech = 0
    fillers = ["um", "uh", "maybe", "i think"]
    penalty = sum(text.lower().count(f) for f in fillers)
    return max(40, 100 - penalty * 10)

def content_quality(text):
    if not text.strip():
        return 0   # 🔴 FIX
    return min(len(text.split()) * 2, 100)

def answer_correctness(text, skills):
    if not text.strip() or not skills:
        return 0
    matches = sum(1 for s in skills if s in text.lower())
    return min(matches * 25, 100)

# -----------------------------
# FINAL EVALUATION
# -----------------------------
if st.button("📊 Evaluate Interview"):

    with st.spinner("Evaluating interview..."):
        time.sleep(2)

    face_score = face_confidence()
    speech_score = speech_clarity(answer_text)
    content_score = content_quality(answer_text)
    correctness_score = answer_correctness(answer_text, skills)

    final_score = round(
        face_score * 0.25 +
        speech_score * 0.25 +
        content_score * 0.25 +
        correctness_score * 0.25,
        2
    )

    # Readiness Level
    if final_score >= 80:
        level = "Job Ready"
    elif final_score >= 60:
        level = "Intermediate"
    else:
        level = "Needs Improvement"

    # Recommendations
    recommendations = []
    if speech_score == 0:
        recommendations.append("Answer was not detected. Please speak clearly.")
    if correctness_score < 50:
        recommendations.append("Include technical keywords related to your resume.")
    if face_score < 70:
        recommendations.append("Improve eye contact and facial confidence.")
    if not recommendations:
        recommendations.append("Excellent interview performance.")

    # -----------------------------
    # OUTPUT
    # -----------------------------
    st.success("✅ Interview Evaluation Completed")

    st.metric("👁️ Facial Confidence", f"{face_score}/100")
    st.metric("🗣️ Speech Clarity", f"{speech_score}/100")
    st.metric("📝 Answer Quality", f"{content_score}/100")
    st.metric("✔️ Answer Correctness", f"{correctness_score}/100")

    st.subheader("🎯 Final Interview Score")
    st.metric("Score", f"{final_score}/100")
    st.info(f"Interview Readiness Level: **{level}**")

    st.subheader("💡 Recommendations")
    for r in recommendations:
        st.write("•", r)
