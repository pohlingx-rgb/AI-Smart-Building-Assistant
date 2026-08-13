import streamlit as st
import pandas as pd

def show_history():
    st.title("📜 Question History")

    # --- Initialize pagination state ---
    if "history_page" not in st.session_state:
        st.session_state.history_page = 1

    # Load history from session_state
    history = st.session_state.get("question_history", [])

    if not history:
        st.info("No questions asked yet.")
        return

    # Convert to DataFrame for display
    df = pd.DataFrame(history)

    # Ensure columns exist
    if "timestamp" not in df.columns:
        df["timestamp"] = pd.Timestamp.now()
    if "category" not in df.columns:
        df["category"] = "General"
    if "question" not in df.columns:
        df["question"] = df.astype(str).agg(" ".join, axis=1)

    # --- Pagination setup ---
    page_size = 10
    total_pages = max(1, (len(df) + page_size - 1) // page_size)

    # Clamp history_page to valid range
    st.session_state.history_page = max(1, min(st.session_state.history_page, total_pages))

    # Slice DataFrame for current page
    start = (st.session_state.history_page - 1) * page_size
    end = start + page_size
    df_page = df.iloc[start:end][["timestamp", "category", "question"]]

    # --- Display table neatly ---
    st.dataframe(df_page, use_container_width=True)

    # --- Pagination controls (no rerun) ---
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("⏮ First", disabled=st.session_state.history_page <= 1):
            st.session_state.history_page = 1

    with col2:
        if st.button("◀ Prev", disabled=st.session_state.history_page <= 1):
            st.session_state.history_page -= 1

    with col3:
        if st.button("Next ▶", disabled=st.session_state.history_page >= total_pages):
            st.session_state.history_page += 1

    with col4:
        if st.button("Last ⏭", disabled=st.session_state.history_page >= total_pages):
            st.session_state.history_page = total_pages

    st.markdown(f"Page {st.session_state.history_page} of {total_pages}")

    # --- Clear history button ---
    if st.button("🧹 Clear History"):
        st.session_state["question_history"] = []
        st.session_state.history_page = 1
        st.success("Question history cleared.")
