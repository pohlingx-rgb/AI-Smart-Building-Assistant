import json
import logging
import os
import re
from datetime import datetime

import pandas as pd
import streamlit as st

from modules.disclaimer import show_disclaimer

logging.basicConfig(filename="audit.log", level=logging.INFO)
HISTORY_FILE = "data/question_history.json"


def log_event(event):
    logging.info(f"{datetime.now()} - {event}")


def save_history(history):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def highlight_text(text, term):
    """Highlight search term inside text using HTML <mark>, case-insensitive."""
    if not term:
        return text
    pattern = re.compile(re.escape(term), re.IGNORECASE)
    return pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)


def show_question_history():
    if "question_history" not in st.session_state:
        st.session_state.question_history = load_history()

    history = st.session_state.question_history
    st.title("📜 Question History")

    if st.button("🗑️ Clear History"):
        st.session_state["question_history"] = []
        save_history(st.session_state["question_history"])
        st.success("History cleared ✅")
        st.rerun()

    if not history:
        st.info("No questions asked yet.")
        show_disclaimer()
        return

    df = pd.DataFrame(history)
    if "timestamp" not in df.columns:
        df["timestamp"] = pd.Timestamp.now()
    if "question" not in df.columns:
        df["question"] = df.astype(str).agg(" ".join, axis=1)
    if "category" not in df.columns:
        df["category"] = "Unknown"
    if "answer" not in df.columns:
        df["answer"] = "No answer recorded"

    st.dataframe(
        df[["timestamp", "category", "question", "answer"]],
        use_container_width=True,
    )

    history_json = json.dumps(history, indent=4)
    st.download_button(
        label="⬇️ Download History",
        data=history_json,
        file_name="question_history.json",
        mime="application/json",
    )

    show_disclaimer()
