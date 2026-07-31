from modules.rag_pipeline import generate_sor_answer
import streamlit as st

import datetime

if "question_history" not in st.session_state:
    st.session_state.question_history = []

def show_sor_validator():
    st.title("🔍 SOR Validator")

    if "sor_chat" not in st.session_state:
        st.session_state.sor_chat = []

    # Display chat history
    for msg in st.session_state.sor_chat:
        st.chat_message(msg["role"]).write(msg["content"])

    # Chat input
    user_query = st.chat_input("Ask about SOR contracts...")
    if user_query:
        st.session_state.sor_chat.append({"role": "user", "content": user_query})

        # Retrieve relevant chunks from vector store
        vector_store = st.session_state.get("vector_store_sor")
        if vector_store:
            results = vector_store.similarity_search(user_query, k=3)
            answer = generate_sor_answer(user_query, results)

            # Build source reference list
            sources = [doc.metadata.get("source", "Unknown") for doc in results]
            if sources:
                answer += "\n\n📂 Sources: " + ", ".join(sources)
        else:
            answer = "No SOR documents indexed yet. Please upload first."

        st.session_state.sor_chat.append({"role": "assistant", "content": answer})
        st.session_state.question_history.append({
            "module": "SOR Validator",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question": user_query,
            "answer": answer
        })
        st.chat_message("assistant").write(answer)



