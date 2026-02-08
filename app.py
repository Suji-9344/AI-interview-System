import streamlit as st
import base64
import re

# ---------------- CONFIG ----------------
st.set_page_config(layout="wide")

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "action" not in st.session_state:
    st.session_state.action = ""

# ---------------- BACKGROUND CACHE ----------------
@st.cache_data
def load_bg(image):
    with open(image, "rb") as f:
        return base64.b64encode(f.read()).decode()

def set_bg(image):
    img = load_bg(image)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------- BUTTON STYLE ----------------
st.markdown("""
<style>
.bottom-buttons {
    position: fixed;
    bottom: 30px;
    width: 100%;
    display: flex;
    justify-content: center;
    gap: 20px;
}
div.stButton > button {
    width: 230px;
    height: 60px;
    font-size: 18px;
    font-weight: bold;
    color: white;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HOME PAGE ----------------
if st.session_state.page == "home":
    set_bg("avatar.png")

    st.markdown('<div class="bottom-buttons">', unsafe_allow_html=True)

    if st.button("📄 Upload Resume"):
        st.session_state.page = "next"
        st.session_state.action = "resume"
        st.rerun()

    if st.button("🎤 Record Answer"):
        st.session_state.page = "next"
        st.session_state.action = "record"
        st.rerun()

    if st.button("📊 Analyze Interview"):
        st.session_state.page = "next"
        st.session_state.action = "analyze"
        st.rerun()

    if st.button("✅ Get Feedback"):
        st.session_state.page = "next"
        st.session_state.action = "feedback"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- NEXT PAGE ----------------
else:
    set_bg("background.png")
    st.markdown("<br><br>", unsafe_allow_html=True)

    # -------- RESUME NLP (RULE-BASED) --------
    if st.session_state.action == "resume":
        st.subheader("📄 Resume Analysis")
        file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

        if file:
            text = file.name.lower()  # demo NLP logic
            name = "Sujitha"
            skills = ["Python", "SQL", "Machine Learning"]
            education = "B.Tech"

            st.success("Resume analyzed successfully ✅")
            st.write("**Name:**", name)
            st.write("**Skills:**", ", ".join(skills))
            st.write("**Education:**", education)

    # -------- RECORD ANSWER --------
    elif st.session_state.action == "record":
        st.subheader("🎤 Interview Answer")
        audio = st.file_uploader("Upload Answer Audio", type=["wav", "mp3"])

        if audio:
            st.success("Answer recorded successfully ✅")

    # -------- ANALYSIS --------
    elif st.session_state.action == "analyze":
        st.subheader("📊 Interview Analysis")

        st.write("**HR Question 1:** Tell me about yourself.")
        st.write("**HR Question 2:** Explain Python and its applications.")

        score = 76
        st.metric("Final Interview Score", f"{score} / 100")

    # -------- FEEDBACK --------
    elif st.session_state.action == "feedback":
        st.subheader("✅ Communication Feedback")

        st.write("✔ Good clarity in answers")
        st.write("✔ Structured response flow")
        st.write("❗ Improve confidence while speaking")
        st.write("❗ Reduce pauses and filler words")
        st.write("❗ Maintain consistent speaking pace")

    st.markdown("<br>")
    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()
