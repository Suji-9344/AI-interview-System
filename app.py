import streamlit as st
import base64

# ------------------ PAGE CONFIG ------------------
st.set_page_config(layout="wide")

# ------------------ SESSION STATE ------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "action" not in st.session_state:
    st.session_state.action = ""

# ------------------ BACKGROUND FUNCTION ------------------
def set_bg(image):
    with open(image, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ------------------ HOME PAGE ------------------
if st.session_state.page == "home":

    set_bg("avatar.png")

    st.markdown("""
    <style>
    .btn {
        width: 260px;
        height: 65px;
        font-size: 20px;
        font-weight: bold;
        color: white;
        border-radius: 15px;
        border: none;
        margin: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        if st.button("📄 Upload Resume", key="resume"):
            st.session_state.page = "next"
            st.session_state.action = "resume"

    with col2:
        if st.button("🎤 Record Answer", key="record"):
            st.session_state.page = "next"
            st.session_state.action = "record"

    with col3:
        if st.button("📊 Analyze Response", key="analyze"):
            st.session_state.page = "next"
            st.session_state.action = "analyze"

    with col4:
        if st.button("✅ Get Feedback", key="feedback"):
            st.session_state.page = "next"
            st.session_state.action = "feedback"

# ------------------ NEXT PAGE ------------------
elif st.session_state.page == "next":

    set_bg("background.png")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # -------- UPLOAD RESUME --------
    if st.session_state.action == "resume":
        st.subheader("📄 Upload Resume")
        resume = st.file_uploader("Upload PDF Resume", type=["pdf"])

        if resume:
            st.success("Resume uploaded successfully ✅")
            st.write("**Name:** Sujitha")
            st.write("**Skills:** Python, SQL, ML")
            st.write("**Education:** B.Tech")

    # -------- RECORD ANSWER --------
    elif st.session_state.action == "record":
        st.subheader("🎤 Upload Interview Answer Audio")
        audio = st.file_uploader("Upload Audio File", type=["wav", "mp3"])

        if audio:
            st.success("Audio uploaded successfully ✅")

    # -------- ANALYZE RESPONSE --------
    elif st.session_state.action == "analyze":
        st.subheader("📊 Interview Score")
        st.metric("Final Score", "78 / 100")

    # -------- GET FEEDBACK --------
    elif st.session_state.action == "feedback":
        st.subheader("✅ Interview Feedback")
        st.write("✔ Good confidence")
        st.write("✔ Clear answers")
        st.write("❗ Improve technical depth")
        st.write("❗ Maintain eye contact")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
