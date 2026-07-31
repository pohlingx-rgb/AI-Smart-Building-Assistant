import streamlit as st
import logging
from datetime import datetime
from modules.disclaimer import show_disclaimer

# Configure audit logging
logging.basicConfig(filename="audit.log", level=logging.INFO)

def log_event(event):
    logging.info(f"{datetime.now()} - {event}")

def show_methodology():
    st.title("📊 Methodology")

    st.write("""
    The assistant uses a Retrieval-Augmented Generation (RAG) pipeline:
    - Documents (SOP, O&M, SOR) are uploaded and stored.
    - A vector store indexes the content for semantic search.
    - Queries are matched against relevant document chunks.
    - An LLM generates answers using retrieved context.
    """)

    st.write("""
    This approach ensures responses are grounded in uploaded materials,
    while still leveraging AI for natural language understanding.
    """)

    log_event(f"{st.session_state.username} viewed Methodology page.")

    show_disclaimer()
