import logging
from datetime import datetime

import streamlit as st

from modules.disclaimer import show_disclaimer

logging.basicConfig(filename="audit.log", level=logging.INFO)


def log_event(event):
    logging.info(f"{datetime.now()} - {event}")


def show_methodology():
    st.title("⚙️ Methodology")

    st.write(
        """
        Our AI Smart Building Assistant is implemented as a Streamlit-based application powered by
        Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG). The methodology
        explains how data flows through the system, how modules interact, and how each use case is
        supported.
        """
    )

    st.subheader("🔄 Data Flow Overview")
    st.write(
        """
        1. Document upload: Admins upload SOR, SOP, and O&M files.
        2. Vector-store indexing: Files are embedded into FAISS for semantic search.
        3. User query processing: Queries are matched to relevant document chunks.
        4. LLM summarization: Retrieved excerpts are used to generate grounded responses.
        5. User experience: Results are displayed with citations and query history.
        """
    )

    st.subheader("🛠️ Implementation Details")
    st.write(
        """
        - Streamlit pages host each module and feature area.
        - Session state manages roles, page navigation, and history.
        - FAISS stores embeddings for efficient similarity search.
        - LLM prompts are designed for domain-specific FM responses.
        - Audit logging and prompt-safety checks support governance and traceability.
        """
    )

    st.subheader("🔐 Role-Based Access Control")
    st.write(
        """
        The system separates Admin and User access. Admins can upload and manage documents, while
        regular users can ask questions and view results. This keeps control over source material
        restricted to authorized personnel.
        """
    )

    st.caption("Figure: Upload → Index → Search → Summarize → Display")

    log_event(f"{st.session_state.username} viewed Methodology page.")
    show_disclaimer()
