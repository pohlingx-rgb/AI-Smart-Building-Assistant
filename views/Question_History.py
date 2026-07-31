import streamlit as st
import json
import logging
import os
from datetime import datetime
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

import re

def highlight_text(text, term):
    """Highlight search term inside text using HTML <mark>, case-insensitive."""
    if not term:
        return text
    # Escape term to avoid regex issues
    pattern = re.compile(re.escape(term), re.IGNORECASE)
    return pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)

def show_history():
    if "question_history" not in st.session_state:
        st.session_state.question_history = load_history()

    history = st.session_state.question_history

    st.title("📝 Question History")
    st.metric("Total Questions Asked", len(history))

    # Filter by module
    modules = sorted(set([item["module"] for item in history])) if history else []
    selected_module = st.selectbox("Filter by module:", ["All"] + modules)

    # Search bar
    search_term = st.text_input("Search history (by question or answer):")

    # Clear history
    if st.button("🗑 Clear History", key="clear_history"):
        st.session_state.question_history = []
        save_history(st.session_state.question_history)
        st.success("History cleared.")
        log_event(f"{st.session_state.username} cleared question history.")
        st.rerun()

    # Apply filters
    filtered = history if selected_module == "All" else [h for h in history if h["module"] == selected_module]
    if search_term:
        filtered = [
            h for h in filtered
            if search_term.lower() in h["question"].lower() or search_term.lower() in h["answer"].lower()
        ]

    # Pagination setup
    items_per_page = 10
    total_pages = max(1, (len(filtered) + items_per_page - 1) // items_per_page)

    if "current_page" not in st.session_state:
        st.session_state.current_page = 1

    # Navigation buttons
    col1, col2, col3, col4 = st.columns([1,1,1,1])
    with col1:
        if st.button("⏮ First", disabled=st.session_state.current_page <= 1):
            st.session_state.current_page = 1
    with col2:
        if st.button("⬅️ Previous", disabled=st.session_state.current_page <= 1):
            st.session_state.current_page -= 1
    with col3:
        if st.button("Next ➡️", disabled=st.session_state.current_page >= total_pages):
            st.session_state.current_page += 1
    with col4:
        if st.button("Last ⏭", disabled=st.session_state.current_page >= total_pages):
            st.session_state.current_page = total_pages

    st.write(f"Page {st.session_state.current_page} of {total_pages}")

    start_idx = (st.session_state.current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_items = filtered[start_idx:end_idx]

    # Display history with highlights
    if not page_items:
        st.info("No matching entries found.")
    else:
        for item in reversed(page_items):
            with st.expander(f"{item['module']} | {item['timestamp']}"):
                st.markdown(
                    f"❓ Question: {highlight_text(item['question'], search_term)}",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"✅ Answer: {highlight_text(item['answer'], search_term)}",
                    unsafe_allow_html=True
                )

    # Export history
    history_json = json.dumps(history, indent=4)
    st.download_button(
        label="⬇️ Download Full History",
        data=history_json,
        file_name="question_history.json",
        mime="application/json",
        key="download_history"
    )
    if history:
        log_event(f"{st.session_state.username} downloaded question history.")

    show_disclaimer()
