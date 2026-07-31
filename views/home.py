import streamlit as st
import logging
from datetime import datetime
from modules.disclaimer import show_disclaimer

# Configure audit logging
logging.basicConfig(filename="audit.log", level=logging.INFO)

if st.session_state.get("logged_in", False):

    # 🎉 Welcome banner
    st.markdown(
        f"### 👋 Welcome back, **{st.session_state.username}** ({st.session_state.role})"
    )
    st.info("You are now logged in. Use the sidebar to navigate.")

    # 🔓 Logout button
    if st.button("Logout", key="logout_home"):
        st.session_state.clear()
        st.rerun()

    st.title("📘 Operations Knowledge Assistant")
    # Sidebar navigation continues here...

def log_event(event):
    logging.info(f"{datetime.now()} - {event}")

def show_home():
    st.title("🏠 AI Smart Building Assistant")

    # Greeting
    username = st.session_state.get("username", "Guest")
    role = st.session_state.get("role", "Unknown")
    st.write(f"Welcome, **{username}**! You are logged in as **{role}**.")

    # Overview
    st.markdown("""
    ### 📌 What you can do here:
    - **Upload Document** → (Only for Admins) Upload SOP, O&M manuals and SOR.
    - **Operations Assistant** → Search inside uploaded manuals for quick answers.
    - **SOR Validator** → Validate Schedule of Rates queries with supporting sources.
    - **Question History** → Review and download past queries and answers.
    - **Operational Manual** → View SOR, SOP and O&M documents that are uploaded.
    - **About Us** → Learn about the project and team.
    - **Methodology** → Understand the RAG pipeline powering this assistant.
    """)

    # Audit log entry
    log_event(f"{username} viewed Home page as {role}.")

    show_disclaimer()
