import streamlit as st
import tempfile
import speech_recognition as sr

# ------------------ APP CONFIG ------------------
st.set_page_config(page_title="AI Interview System", layout="wide")

# ------------------ DISPLAY BIG AVATAR ------------------
st.image("avatar.png", use_column_width=True)  # Big avatar image
st.markdown("<br><br>", unsafe_allow_html=True)

# ------------------ BUTTON CSS ------------------
st.markdown("""
<style>
/* Style all buttons */
div.stButton > button {
    width: 220px;
    height: 60px;
    font-size: 18px;
    font-weight: bold;
    color: white;
    border-radius: 12px;
    margin: 10px;
}

/* Color for each button */
.upload button { background-color: #2ecc71 !important; }    /* green */
.record button { background-color: #ff4b4b !important; }    /* red */
.analyze button { background-color: #3498db !important; }   /* blue */
.feedback button { background-color: #f39c12 !important; }  /* orange */
.next button { background-color: #9b59b6 !important; }       /* purple for next page */
</style>
""", unsafe_allow_html=True)

# ------------------ BUTTONS ------------------
cols = st.columns(4)  # Four buttons side by side

uploaded_file = None
audio_file_path = None
score = None

# ---------- UPLOAD RESUME ----------
with cols[0]:
    st.markdown('<div class="upload">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Resume (PDF)")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- RECORD ANSWER ----------
with cols[1]:
    st.markdown('<div class="record">', unsafe_allow_html=True)
    if st.button("🎤 Record Answer"):
        st.write("Recording answer via microphone...")
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                st.info("Please speak now (max 10 seconds)...")
                audio_data = r.listen(source, phrase_time_limit=10)
                tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                with open(tmp_file.name, "wb") as f:
                    f.write(audio_data.get_wav_data())
                audio_file_path = tmp_file.name
                st.success("Audio recorded successfully!")
        except Exception as e:
            st.error(f"Microphone not accessible: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- ANALYZE RESPONSE ----------
with cols[2]:
    st.markdown('<div class="analyze">', unsafe_allow_html=True)
    if st.button("📊 Analyze Response"):
        st.write("Analyzing response...")
        # -------- RESUME PARSING PLACEHOLDER ---------
        if uploaded_file:
            st.write(f"Resume uploaded: {uploaded_file.name}")
            st.write("Identified Name: John Doe")
            st.write("Skills: Python, SQL, Machine Learning")
            st.write("Education: B.Tech")
        else:
            st.warning("Please upload a resume first!")
        # -------- AUDIO ANALYSIS PLACEHOLDER ---------
        if audio_file_path:
            st.write("Processing recorded audio...")
            # Placeholder: calculate score
            score = 78
            st.write(f"Score Prediction: {score}/100")
        else:
            st.warning("Please record your answer first!")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- GET FEEDBACK ----------
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

# ------------------ NEXT PAGE BUTTON ------------------
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("➡ Go to Processed Results"):
    st.markdown('<div class="next">', unsafe_allow_html=True)
    st.write("Showing processed results...")
    if uploaded_file:
        st.write(f"Resume Name: John Doe")
        st.write("Skills: Python, SQL, Machine Learning")
        st.write("Education: B.Tech")
    if audio_file_path:
        st.write("Audio file processed successfully")
    if score:
        st.write(f"Score: {score}/100")
        st.write("Feedback: See suggestions above")
    st.markdown('</div>', unsafe_allow_html=True)
