import streamlit as st

# Display avatars
col1, col2 = st.columns([1, 2])
with col1:
    st.image("hr_avatar.jpeg", width=200)
with col2:
    st.image("user_avatar.png", width=200)

# Buttons
if st.button("🎤 Record Answer"):
    st.write("Recording started...")

if st.button("📄 Upload Resume"):
    st.write("Resume upload dialog opened...")

if st.button("📊 Analyze Response"):
    st.write("Analyzing answer...")

if st.button("✅ Get Feedback"):
    st.write("Showing feedback...")
