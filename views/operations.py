import streamlit as st
from modules.rag_pipeline import generate_answer
import datetime
from modules.history_utils import append_history

def run_operations_query(user_query):
    """Retrieve relevant operations documents and generate an answer."""
    vector_store = st.session_state.get("vector_store_ops")
    if not vector_store:
        return "No SOP or O&M documents indexed yet. Please upload first."

    results = vector_store.similarity_search(user_query, k=3)
    answer = generate_answer(user_query, results)
    sources = [doc.metadata.get("source", "Unknown") for doc in results]
    if sources:
        answer += "\n\n📂 Sources: " + ", ".join(sources)
    return answer


if "question_history" not in st.session_state:
    st.session_state.question_history = []

def show_operations():
    st.header("⚙️ Operations Assistant")

    if "ops_chat" not in st.session_state:
        st.session_state.ops_chat = []

    # Display chat history
    for msg in st.session_state.ops_chat:
        st.chat_message(msg["role"]).write(msg["content"])

    # Chat input
    user_query = st.chat_input("Ask about SOP or O&M...")
    if user_query:
        st.session_state.ops_chat.append({"role": "user", "content": user_query})

        # Retrieve relevant chunks from vector store
        vector_store = st.session_state.get("vector_store_ops")
        if vector_store:
            results = vector_store.similarity_search(user_query, k=3)
            answer = generate_answer(user_query, results)

            # Build source reference list
            sources = [doc.metadata.get("source", "Unknown") for doc in results]
            if sources:
                answer += "\n\n📂 Sources: " + ", ".join(sources)
        else:
            answer = "No SOP or O&M documents indexed yet. Please upload first."

        st.session_state.ops_chat.append({"role": "assistant", "content": answer})
        st.session_state.question_history.append({
            "module": "Operations Assistant",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question": user_query,
            "answer": answer,
        })
        st.chat_message("assistant").write(answer)
