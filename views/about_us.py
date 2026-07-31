import streamlit as st
import logging
from datetime import datetime
from modules.disclaimer import show_disclaimer

# Configure audit logging
logging.basicConfig(filename="audit.log", level=logging.INFO)

def log_event(event):
    logging.info(f"{datetime.now()} - {event}")

def show_about():
    st.title("ℹ️ About Us")

    st.write("""
    This AI Smart Building Assistant was developed as part of an academic project.
    It integrates document search, SOR validation, and operational support features
    to help facility managers and engineers streamline their work.
    """)

    st.write("👨‍💻 Developed by: Soh Shi Ying, Chloe and Loh Poh Ling")
    st.write("🏫 Academic context: AI Bootcamp Project")

    log_event(f"{st.session_state.username} viewed About Us page.")

    show_disclaimer()
