import streamlit as st
import base64

def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;       /* Makes image full-screen */
            background-repeat: no-repeat; /* Prevent tiling */
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("background.png")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("user_avatar.png", width=1000)
    st.markdown("<h3 style='color:white; text-align:center;'>🧑 Candidate</h3>", unsafe_allow_html=True)
    # Buttons below

