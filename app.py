import streamlit as st
import base64
import tempfile
import os
import speech_recognition as sr
from datetime import datetime

# ------------------ SET BACKGROUND ------------------
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("background.png")  # <-- full-screen background

# ------------------ APP TITLE ------------------
st.markdown("<h1 style='text-align:center; color:white;'>AI INTERVIEW ASSESSMENT SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ------------------ SHOW AVATAR ------------------
st.image("avatar.png", use_column_width=True)  # Big user avatar
st.markdown("<br>", unsafe_allow_html=True)

# ------------------ BUTTON CSS ------------------
st.markdown("""
<style>
div.stButton > button {
    width: 250px;
    height: 60px;
    font-size: 18px;
    font-weight: bold;
    color: white;
    margin: 10px;
    border-radius: 12px;
}
.upload button { background-color: #2ecc71; }
.record button { background-color: #ff4b4b; }
.analyze button { background-color: #3498db; }
.feedback button { background-color: #f39c12; }
</style>
""", unsafe_allow_html=True)

# ------------------ BUTTONS ------------------
cols = st.columns(4)  # Four buttons in a row

uploaded_file = None
audio_file_path = None
score = None

# ----------- UPLOAD RESUME -----------
with cols[0]:
    st.markdown('<div class="upload">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Resume (PDF)")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------- RECORD ANSWER -----------
with cols[1]:
    st.markdown('<div class="record">', unsafe_allow_html=True)
    if st.button("🎤 Record Answer"):
        st.write("Recording answer via microphone...")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Please speak now...")
            audio_data = r.listen(source, phrase_time_limit=10)
            # Save temporary audio file
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            with open(tmp_file.name, "wb") as f:
                f.write(audio_data.get_wav_data())
            audio_file_path = tmp_file.name
            st.success(f"Audio recorded: {audio_file_path}")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------- ANALYZE RESPONSE -----------
with cols[2]:
    st.markdown('<div class="analyze">', unsafe_allow_html=True)
    if st.button("📊 Analyze Response"):
        st.write("Analyzing resume and answer...")
        # --------- RESUME PARSING PLACEHOLDER ---------
        if uploaded_file:
            st.write(f"Resume uploaded: {uploaded_file.name}")
            st.write("Identified Name: John Doe")
            st.write("Skills: Python, SQL, Machine Learning")
            st.write("Education: B.Tech")
        else:
            st.warning("Please upload a resume first!")
        # --------- AUDIO ANALYSIS PLACEHOLDER ---------
        if audio_file_path:
            st.write("Processing recorded audio...")
            # Placeholder: analyze confidence, communication
            score = 78  # Example score
            st.write(f"Score Prediction: {score}/100")
        else:
            st.warning("Please record your answer first!")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------- GET FEEDBACK -----------
with cols[3]:
    st.markdown('<div class="feedback">', unsafe_allow_html=True)
    if st.button("✅ Get Feedback"):
        st.write("Showing feedback and suggestions...")
        if score:
            if score >= 80:
                st.success("Excellent performance! Keep it up.")
            elif score >= 60:
                st.info("Good, but improve confidence and clarity.")
            else:
                st.warning("Needs improvement: Practice more and work on communication skills.")
            st.write("- Improve confidence and body language")
            st.write("- Clear pronunciation and structured answers")
        else:
            st.warning("Please analyze response first!")
    st.markdown('</div>', unsafe_allow_html=True)
