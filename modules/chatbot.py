import streamlit as st
from langchain_openai import ChatOpenAI
import datetime

# Ensure global history exists once
if "question_history" not in st.session_state:
    st.session_state["question_history"] = []

def summarize_answer(question, docs, role="assistant"):
    context = "\n\n".join([doc.page_content for doc in docs])
    sources = [doc.metadata.get("source", "Unknown file") for doc in docs]

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    prompt = f"""
    You are a {role}. Summarize the following information in a clear, human-like tone
    to answer the user's question: "{question}". Avoid copying text verbatim; explain naturally.
    Include key steps or insights if relevant.

    Context:
    {context}
    """
    summary = llm.invoke(prompt).content
    return f"**Answer:** {summary}\n\n**Sources:** " + ", ".join(sources)


def show_chatbot(vector_store, session_key, label, input_key, role="assistant"):
    st.markdown("---")
    st.subheader("💬 Chatbot")

    show_sources_only = st.toggle(
        "Show sources only (no full excerpts)",
        value=False,
        key=f"sources_toggle_{session_key}"
    )

    if session_key not in st.session_state:
        st.session_state[session_key] = []

    question = st.chat_input(label, key=input_key)

    # Only log when a *new* question is asked
    if question:
        st.session_state[session_key].append({"role": "user", "content": question})

        # Append to global history safely
        st.session_state["question_history"].append({
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": role,
            "question": question
        })

        if vector_store:
            results = vector_store.similarity_search(question, k=3)
            if show_sources_only:
                answer_parts = [f"📄 **{doc.metadata.get('source','Unknown')}**" for doc in results]
                answer = "Based on the documents:\n\n" + "\n\n".join(answer_parts)
            else:
                answer = summarize_answer(question, results, role=role)
        else:
            answer = "⚠️ No indexed documents found. Please upload first."

        st.session_state[session_key].append({"role": "assistant", "content": answer})

    # Display chat history
    for message in st.session_state[session_key]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if st.button("🧹 Clear Chat", key=f"clear_{session_key}"):
        st.session_state[session_key] = []
        st.success("Chat history cleared.")
