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
    st.write("""
    This project presents a proof‑of‑concept AI Assistant for Smart Building Operations, built to support Facilities Management (FM) teams in streamlining workflows and reducing inefficiencies. Implemented as a Streamlit‑based application, the assistant integrates document validation and intelligent querying into a single platform. It enables natural language interaction with SOPs, O&M manuals, and contracts, while also validating repair and procurement items against the Schedule of Rates (SOR). By combining retrieval‑augmented generation (RAG), compliance validation, and role‑based governance, the system demonstrates both operational knowledge transfer and contractual compliance assurance.
    """)

    st.subheader("📐 Project Scope")

    st.write("""
    This project delivers a **proof‑of‑concept AI Assistant for Smart Building Operations**, designed to support Facilities Management (FM) teams in overcoming inefficiencies caused by fragmented data and manual processes. The assistant is implemented as a **Streamlit‑based web application**, integrating document validation and intelligent querying into a single platform.
    
    The scope covers:
    1. Development of a **domain‑specific AI system** (not a generic chatbot).
    2. Integration of **retrieval‑augmented generation (RAG)** for source‑grounded answers.
    3. Modular design with clear separation of **Admin vs User roles**.
    4. Deployment as a prototype to demonstrate feasibility and operational value.
    """)

    st.subheader("🎯 Objectives")

    st.write("""
    The project aims to:
    1. **Streamline information retrieval** across FM documents.
    2. **Reduce compliance risks** by validating repair and procurement items against contract SOR.
    3. **Enable natural language interaction** with SOPs, O&M manuals, and contracts.
    4. **Enhance trust and transparency** by providing answers with citations and history tracking.
    """)

    st.subheader("📂 Data Sources")

    st.write("""
    The assistant is powered by organisation‑specific FM documents, uploaded by Admins in supported formats (txt, docx, pdf).
    
    Key data sources include:
    1. **Schedule of Rates (SOR)** — Contractual reference for repair and procurement validation.
    2. **Standard Operating Procedures (SOPs)** — Compliance, Performance requirements and Operational guidelines for FM teams.
    3. **Operations & Maintenance Manuals (O&M)** — Technical references for building systems.
    
    All documents are embedded into a **FAISS vector store**, enabling semantic search and retrieval.
    """)

    st.subheader("⚙️ Features")

    st.write("""
    The assistant integrates two core modules:
    1. **SOR Validator** — Validates whether repair or procurement items fall within contracted SOR.
    2. **Operations Knowledge Assistant** — Provides natural language querying across SOPs, O&M manuals, and contracts, generating natural, human‑like answers with clear citations.
    
    Additional features include:
    1. Role‑based access control (Admin vs User).
    2. Audit logging with question history and admin clear/reset controls.
    3. Summarization toggle to switch between concise answers and detailed source excerpts.
    4. Error handling with clear warnings when indexes are missing or documents are not uploaded.
    """)

    st.subheader("🌐 System Overview")

    st.write("""
    The system architecture supports two primary use cases:
    
    💬 **Case A: Chat‑based FM Knowledge Retrieval** — Users query internal documents using plain language, and the assistant generates natural, human‑like answers grounded in uploaded sources with citations (e.g., AHU/FCU daily procedures).
    
    📑 **Case B: Intelligent SOR Search** — Users validate repair or procurement items against contract SOR to ensure compliance (e.g., deck‑mounted self‑closing tap replacement cost).
    
    Each use case follows a structured data flow from document upload to semantic search and LLM‑based summarization, ensuring transparency, traceability, and operational efficiency across all interactions.
    """)

    st.write("👨‍💻 Developed by: Soh Shi Ying, Chloe and Loh Poh Ling")
    st.write("🏫 Academic context: AI Bootcamp Project")

    log_event(f"{st.session_state.username} viewed About Us page.")

    show_disclaimer()
