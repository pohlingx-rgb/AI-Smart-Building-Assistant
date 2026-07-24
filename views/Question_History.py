import streamlit as st
import pandas as pd
import json
from modules.disclaimer import show_disclaimer

def show_question_history():
    st.title("📜 Question History")

    # --- Load history from session_state ---
    history = st.session_state.get("question_history", [])

    # --- Clear History Button ---
    if st.button("🗑️ Clear History"):
        st.session_state["question_history"] = []
        st.success("History cleared ✅")
        st.rerun()

    if not history:
        st.info("No questions asked yet.")
        return

    # --- Convert to DataFrame for table view ---
    df = pd.DataFrame(history)

    # Ensure required columns exist
    if "timestamp" not in df.columns:
        df["timestamp"] = pd.Timestamp.now()
    if "question" not in df.columns:
        df["question"] = df.astype(str).agg(" ".join, axis=1)
    if "category" not in df.columns:
        df["category"] = "Unknown"
    if "answer" not in df.columns:
        df["answer"] = "No answer recorded"

    # --- Show table with timestamp + category + question + answer ---
    st.dataframe(
        df[["timestamp", "category", "question", "answer"]],
        use_container_width=True
    )

    # --- Download history as JSON ---
    history_json = json.dumps(history, indent=4)
    st.download_button(
        label="⬇️ Download History",
        data=history_json,
        file_name="question_history.json",
        mime="application/json"
    )

    show_disclaimer()
