import streamlit as st

# -------------------- TITLE --------------------
st.markdown("<h1 style='text-align:center; color:white;'>🧑 Candidate Interview</h1>", unsafe_allow_html=True)

# -------------------- SHOW USER AVATAR FULL-SCREEN --------------------
st.image("user_avatar.png", use_column_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)  # spacing

# -------------------- BUTTONS --------------------
if st.button("🎤 Record Answer"):
    st.write("Recording started...")

if st.button("📄 Upload Resume"):
    uploaded_file = st.file_uploader("Upload your resume (PDF)")
    if uploaded_file:
        st.write(f"Resume uploaded: {uploaded_file.name}")

if st.button("📊 Analyze Response"):
    st.write("Analyzing response...")

if st.button("✅ Get Feedback"):
    st.write("Showing feedback & suggestions...")
