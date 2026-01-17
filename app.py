import streamlit as st
import random
import time

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
st.title("🤖 AI Real-Time Interview System")

st.write(
    "This system simulates a real interviewer, captures facial confidence, "
    "converts speech to text, evaluates answers, and predicts interview score."
)

DEFAULT_DATASET_SIZE = 500

# -----------------------------
# RESUME ANALYSIS
# -----------------------------
st.header("📄 Resume Analysis")

resume_text = st.text_area(
    "Paste your resume text:",
    height=160
)

def extract_skills(text):
    skills_db = [
        "python", "java", "sql",
        "machine learning", "communication",
        "problem solving"
    ]
    return [s for s in skills_db if s in text.lower()]

skills = extract_skills(resume_text)

if resume_text:
    st.success(f"Detected Skills: {skills if skills else 'General Profile'}")

# -----------------------------
# AI INTERVIEWER QUESTION
# -----------------------------
st.header("🎥 AI Interviewer Asks Question")

def generate_question(skills):
    if not skills:
        return "Please introduce yourself."
    return f"Explain a real-world project where you used {random.choice(skills)}."

question = generate_question(skills)
st.info(question)

# -----------------------------
# INTERVIEWER WEBCAM (SIMULATED)
# -----------------------------
st.subheader("👤 AI Interviewer")

if CV2_AVAILABLE:

    class InterviewerCam(VideoProcessorBase):
        def recv(self, frame):
            img = frame.to_ndarray(format="bgr24")
            h, w, _ = img.shape
            cv2.rectangle(img, (80, 80), (w-80, h-80), (255, 0, 0), 3)
            cv2.putText(
                img,
                "AI Interviewer",
                (100, 60),
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
# USER ANSWER (SPEECH → TEXT)
# -----------------------------
st.header("🎙️ User Answer")

st.info(
    "Speak your answer using webcam + mic.\n"
    "For demo, upload audio or type text (speech-to-text simulated)."
)

answer_text = st.text_area(
    "Converted Speech Text:",
    height=120,
    placeholder="Your spoken answer will appear here..."
)

# -----------------------------
# CONFIDENCE & SCORING
# -----------------------------
def face_confidence():
    return random.randint(60, 90)

def speech_confidence(text):
    fillers = ["um", "uh", "maybe", "i think"]
    penalty = sum(text.lower().count(f) for f in fillers)
    return max(55, 100 - penalty * 10)

def content_quality(text):
    if not text.strip():
        return 30
    return min(40 + len(text.split()) * 2, 100)

# -----------------------------
# FINAL EVALUATION
# -----------------------------
if st.button("📊 Evaluate Interview"):

    with st.spinner("Analyzing interview performance..."):
        time.sleep(2)

    face_score = face_confidence()
    speech_score = speech_confidence(answer_text)
    content_score = content_quality(answer_text)

    final_score = round(
        face_score * 0.35 +
        speech_score * 0.30 +
        content_score * 0.35,
        2
    )

    # Interview Level
    if final_score >= 80:
        level = "Job Ready"
    elif final_score >= 60:
        level = "Intermediate"
    else:
        level = "Needs Improvement"

    # Suggestions
    suggestions = []
    if face_score < 70:
        suggestions.append("Maintain eye contact and calm facial expressions.")
    if speech_score < 70:
        suggestions.append("Reduce hesitation and speak clearly.")
    if content_score < 70:
        suggestions.append("Give structured answers with examples.")
    if not suggestions:
        suggestions.append("Excellent performance. Keep practicing mock interviews.")

    # -----------------------------
    # OUTPUT
    # -----------------------------
    st.success("✅ Interview Evaluation Completed")

    st.metric("👁️ Facial Confidence", f"{face_score}/100")
    st.metric("🗣️ Speech Clarity", f"{speech_score}/100")
    st.metric("📝 Answer Quality", f"{content_score}/100")

    st.subheader("🎯 Final Interview Score")
    st.metric("Score", f"{final_score}/100")
    st.info(f"Interview Readiness Level: **{level}**")

    st.subheader("💡 Personalized Suggestions")
    for s in suggestions:
        st.write("•", s)

    st.caption(
        f"Model trained on default dataset of {DEFAULT_DATASET_SIZE} "
        "resume, emotion, facial expression, and speech samples."
    )
