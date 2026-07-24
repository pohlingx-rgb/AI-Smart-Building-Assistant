import streamlit as st
import json

from modules.disclaimer import show_disclaimer

history = st.session_state.get(
    "question_history",
    []
)

st.title("📝 Question History")

st.metric(
    "Total Questions Asked",
    len(history)
)

if st.button("🗑 Clear History"):
    st.session_state.question_history = []
    st.rerun()

if not history:
    st.info(
        "No questions asked yet."
    )
else:
    for item in reversed(history):
        with st.expander(
            f"{item['module']} | {item['timestamp']}"
        ):
            st.write(
                f"❓ Question: {item['question']}"
            )
            st.write(
                f"✅ Answer: {item['answer']}"
            )

history_json = json.dumps(
    history,
    indent=4
)

history_json = json.dumps(
    history,
    indent=4
)

st.download_button(
    label="⬇️ Download History",
    data=history_json,
    file_name="question_history.json",
    mime="application/json"
)

show_disclaimer()