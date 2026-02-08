import streamlit as st
import tempfile
import speech_recognition as sr

# ------------------ APP CONFIG ------------------
st.set_page_config(page_title="AI Interview System", layout="wide")

# ------------------ SHOW BIG AVATAR ------------------
st.image("avatar.png", use_column_width=True)  # big avatar image
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
.upload button { background-color: #2ecc71; }   /* green */
.record button { background-color: #ff4b4b; }   /* red */
.analyze button { background-color: #3498db; }  /* blue */
.feedback button { background-color: #f39c12; } /* orange */
</style>
""", unsafe_allow_html=True)

# ------------------ BUTTONS ------------------
cols = st.columns(4)  # Four buttons side by side

# ---------- UPLOAD RESUME ----------
with cols[0]:
    st.markdown('<div class="upload">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Resume (PDF)")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- RECORD ANSWER ----------
audio_file_path = None
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
score = None
with cols[2]:
    st.markdown('<div class="analyze">', unsafe_allow_html=True)
    if st.button("📊 Analyze Response"):
        st.write("Analyzing response...")
        # -------- RESUME PARSING ----------
        if uploaded_file:
            st.write(f"Resume uploaded: {uploaded_file.name}")
            st.write("Identified Name: John Doe")
            st.write("Skills: Python, SQL, Machine Learning")
            st.write("Education: B.Tech")
        else:
            st.warning("Please upload a resume first!")
        # -------- AUDIO ANALYSIS ----------
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
    # Navigate to results section
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
