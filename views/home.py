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

    👋Welcome to the **AI Smart Building Assistant** — your tool for streamlined knowledge retrieval and contract compliance validation in Facilities Management.

    ## 📌 What You Can Do Here

    - **About Us** → Learn about the project scope, objectives, and development team.  
    - **Methodology** → Explore the RAG pipeline and layered architecture powering this assistant.  
    - **Upload Document (Admin Only)** → Upload SOPs, O&M manuals, and SOR contracts for indexing and search.  
    - **Operations Assistant (SOP + O&M)** → Query uploaded manuals using natural language to get quick, source‑grounded answers.  
    - **SOR Validator (SOR Only)** → Validate repair or procurement items against the Schedule of Rates (SOR) with supporting citations.  
    - **Question History** → Review and download past queries and answers for audit and traceability.  
    """)

    # Audit log entry
    log_event(f"{username} viewed Home page as {role}.")

    show_disclaimer()
