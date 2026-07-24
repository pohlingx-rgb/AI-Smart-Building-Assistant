import streamlit as st
import datetime
from langchain_openai import ChatOpenAI   # ✅ correct import for new versions

# Initialise LLM (adjust model_name if needed)
llm = ChatOpenAI(model_name="gpt-4", temperature=0.3)

def log_to_history(role, question, answer, results):
    """Log Q&A into global question_history with sources."""
    if "question_history" not in st.session_state:
        st.session_state["question_history"] = []

    sources = []
    for doc in results:
        src = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "N/A")
        sources.append(f"{src}, Page {page}")

    st.session_state["question_history"].append({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "category": role,
        "question": question,
        "answer": answer,
        "sources": sources
    })


def show_chatbot(vector_store, session_key="chat", label="Ask a question", input_key="chat_input", role="Assistant"):
    st.subheader(f"💬 {role}")

    if session_key not in st.session_state:
        st.session_state[session_key] = []

    question = st.chat_input(label, key=input_key)
    if question:
        # Append user message
        st.session_state[session_key].append({"role": "user", "content": question})

        if vector_store:
            results = vector_store.similarity_search(question, k=5)
            context = "\n\n".join([doc.page_content for doc in results])

            # ✅ Persona + strict grounding prompt
            prompt = f"""
            You are a seasoned Facilities Manager with deep expertise in building operations,
            maintenance, and compliance. Your role is to advise colleagues in a professional,
            practical, and human-like tone.

            IMPORTANT RULES:
            - Only use the provided context from uploaded documents.
            - Do not invent or hallucinate information outside the context.
            - If the context does not contain an answer, say clearly:
              "The uploaded documents do not provide guidance on this question."
            - When possible, present the answer as structured guidance (checklist, steps, or actionable advice).
            - Always cite the source document(s) at the end.

            Context:
            {context}

            Question:
            {question}

            Answer (as a Facilities Manager):
            """

            # ✅ Use .invoke() instead of .predict()
            response = llm.invoke(prompt)
            answer = response.content if hasattr(response, "content") else str(response)

            # ✅ Explicitly append sources to the answer
            if results:
                source_list = [f"{doc.metadata.get('source','unknown')}"
                               for doc in results]
                answer += "\n\nSources: " + ", ".join(source_list)

            log_to_history(role, question, answer, results)
        else:
            results = []
            answer = "⚠️ No index available yet. Please upload documents first."
            log_to_history(role, question, answer, results)

        # Append assistant message
        st.session_state[session_key].append({"role": "assistant", "content": answer})

    # Display chat history
    for msg in st.session_state[session_key]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
