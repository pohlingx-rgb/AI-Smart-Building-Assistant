import logging
from datetime import datetime

import streamlit as st

from modules.disclaimer import show_disclaimer

logging.basicConfig(filename="audit.log", level=logging.INFO)


def log_event(event):
    logging.info(f"{datetime.now()} - {event}")


def show_home():
    st.title("🏠 AI Smart Building Assistant")

    username = st.session_state.get("username", "Guest")
    role = st.session_state.get("role", "Unknown")
    st.write(f"Welcome, **{username}**! You are logged in as **{role}**.")

    st.markdown(
        """
        👋Welcome to the **AI Smart Building Assistant** — your tool for streamlined knowledge
        retrieval and contract compliance validation in Facilities Management.

        ## 📌 What You Can Do Here

        - **About Us** → Learn about the project scope, objectives, and development team.
        - **Methodology** → Explore the RAG pipeline and layered architecture powering this assistant.
        - **Upload Document (Admin Only)** → Upload SOPs, O&M manuals, and SOR contracts for indexing and search.
        - **Operations Assistant (SOP + O&M)** → Query uploaded manuals using natural language.
        - **SOR Validator (SOR Only)** → Validate repair or procurement items against the contract SOR.
        - **Question History** → Review and download past queries and answers for audit and traceability.
        """
    )

    log_event(f"{username} viewed Home page as {role}.")
    show_disclaimer()
