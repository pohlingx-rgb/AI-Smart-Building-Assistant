import logging
from datetime import datetime

import streamlit as st

from modules.disclaimer import show_disclaimer

logging.basicConfig(filename="audit.log", level=logging.INFO)


def log_event(event):
    logging.info(f"{datetime.now()} - {event}")


def show_about():
    st.title("ℹ️ About Us")

    st.subheader("📌 Executive Summary")
    st.write(
        """
        This project presents a proof-of-concept AI Assistant for Smart Building Operations,
        built to support Facilities Management (FM) teams in streamlining workflows and reducing
        inefficiencies. It combines document validation and intelligent querying into a single
        Streamlit-based platform, allowing natural language interaction with SOPs, O&M manuals,
        and contracts while validating repair and procurement items against the Schedule of Rates (SOR).
        """
    )

    st.subheader("📐 Project Scope")
    st.write(
        """
        The assistant is designed to help facilities teams access operational knowledge faster,
        reduce compliance risks, and keep a traceable record of prior queries and decisions.
        It uses document indexing and retrieval-augmented generation so answers are grounded in
        uploaded source documents rather than generic responses.
        """
    )

    st.subheader("🎯 Objectives")
    st.write(
        """
        - Streamline information retrieval across FM documents
        - Reduce compliance risks by validating tasks against contract SOR
        - Support natural language interaction with SOPs and O&M manuals
        - Enhance trust and transparency with citations and history tracking
        """
    )

    st.subheader("📂 Data Sources")
    st.write(
        """
        The assistant works with uploaded documents such as SOR, SOPs, and O&M manuals. These are
        indexed in a FAISS vector store to support semantic search and contextual retrieval.
        """
    )

    st.subheader("⚙️ Features")
    st.write(
        """
        - SOR Validator: checks whether repair or procurement items are covered by contract pricing
        - Operations Assistant: answers questions from SOP and O&M documents
        - Question History: keeps a record of past queries and answers
        - Role-based access: Admins can upload and manage documents; Users can query them
        """
    )

    st.write("👨‍💻 Developed by: Soh Shi Ying, Chloe and Loh Poh Ling")
    st.write("🏫 Academic context: AI Bootcamp Project")

    log_event(f"{st.session_state.username} viewed About Us page.")
    show_disclaimer()
