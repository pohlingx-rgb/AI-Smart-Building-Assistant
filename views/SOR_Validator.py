import streamlit as st
from datetime import datetime

from modules.rag_pipeline import generate_sor_answer

from modules.disclaimer import show_disclaimer

st.title("🔍 SOR Validator")

st.write("""
Ask questions about Schedule of Rates (SOR)
contracts and coverage.
""")

if "question_history" not in st.session_state:
    st.session_state.question_history = []

question = st.text_input(
    "Enter SOR validation question"
)

vector_store = st.session_state.get(
    "vector_store"
)

if not vector_store:

    st.warning(
        "Please upload a document first."
    )

elif question:

    results = vector_store.similarity_search(
        question,
        k=3
    )

    answer = generate_sor_answer(
        question,
        results
    )

    history_item = {
        "module": "SOR Validator",
        "question": question,
        "answer": answer,
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    if (
        not st.session_state.question_history
        or
        st.session_state.question_history[-1]["question"] != question
    ):
        st.session_state.question_history.append(
            history_item
        )

    st.subheader("SOR Assessment")

    st.write(answer)

    st.subheader("Supporting Sources")

    for idx, doc in enumerate(results):

        st.write(
            f"Source {idx + 1}"
        )

        st.code(doc.page_content)

show_disclaimer()