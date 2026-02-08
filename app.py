import streamlit as st
import base64

# ------------------ CONFIG ------------------
st.set_page_config(layout="wide")

# ------------------ SESSION STATE ------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "action" not in st.session_state:
    st.session_state.action = ""

# ------------------ CACHE BACKGROUND ------------------
@st.cache_data
def load_bg(image):
    with open(image, "rb") as f:
        return base64.b64encode(f.read()).decode()

def set_bg(image):
    encoded = load_bg(image)
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

# ------------------ BUTTON STYLE ------------------
st.markdown("""
<style>
div.stButton > button {
    width: 260px;
    height: 65px;
    font-size: 20px;
    font-weight: bold;
    color: white;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HOME PAGE ------------------
if st.session_state.page == "home":

    set_bg("avatar.png")

    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)

    with c1:
        if st.button("📄 Upload Resume"):
            st.session_state.page = "next"
            st.session_state.action = "resume"
            st.rerun()

    with c2:
        if st.button("🎤 Record Answer"):
            st.session_state.page = "next"
            st.session_state.action = "record"
            st.rerun()

    with c3:
        if st.button("📊 Analyze Response"):
            st.session_state.page = "next"
            st.session_state.action = "analyze"
            st.rerun()

    with c4:
        if st.button("✅ Get Feedback"):
            st.session_state.page = "next"
            st.session_state.action = "feedback"
            st.rerun()

# ------------------ NEXT PAGE ------------------
else:
    set_bg("background.png")
    st.markdown("<br><br>", unsafe_allow_html=True)

    if st.session_state.action == "resume":
        st.subheader("📄 Upload Resume")
        file = st.file_uploader("Upload PDF", type=["pdf"])
        if file:
            st.success("Resume uploaded successfully ✅")
            st.write("**Name:** Sujitha")
            st.write("**Skills:** Python, SQL, ML")
            st.write("**Education:** B.Tech")

    elif st.session_state.action == "record":
        st.subheader("🎤 Upload Interview Audio")
        audio = st.file_uploader("Upload Audio", type=["wav", "mp3"])
        if audio:
            st.success("Audio uploaded successfully ✅")

    elif st.session_state.action == "analyze":
        st.subheader("📊 Interview Score")
        st.metric("Final Score", "78 / 100")

    elif st.session_state.action == "feedback":
        st.subheader("✅ Feedback")
        st.write("✔ Good confidence")
        st.write("✔ Clear answers")
        st.write("❗ Improve technical depth")

    st.markdown("<br>")
    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()
