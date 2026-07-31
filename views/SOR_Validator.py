import streamlit as st

from modules.chatbot import log_to_history, show_chatbot
from modules.disclaimer import show_disclaimer
from modules.vector_store import load_vector_store


def show_sor_validator():
    st.title("📑 SOR Validator")

    if "vector_store_sor" not in st.session_state or st.session_state.vector_store_sor is None:
        st.session_state.vector_store_sor = load_vector_store("SOR_index")

    vector_store = st.session_state.vector_store_sor

    if vector_store:
        st.success("✅ SOR index loaded and ready")
    else:
        st.info("⚠️ No SOR index found yet. Chatbot is still available, but answers won’t be based on SOR documents.")

    st.write("Upload SOR documents on the **Upload Document** page. Then query them here.")
    st.markdown("---")

    show_sources_only = st.checkbox("Show sources only")

    if show_sources_only:
        if vector_store:
            query = st.text_input("Enter a query to fetch sources only", key="sor_sources_input")
            if query:
                results = vector_store.similarity_search(query, k=5)
                st.subheader("📖 Supporting Sources")
                for doc in results:
                    src = doc.metadata.get("source", "unknown")
                    page = doc.metadata.get("page", "N/A")
                    st.write(f"As a Facilities Manager, I found relevant contract clause in **{src}**, page {page}:")
                    st.code(doc.page_content[:500])

                log_to_history("SOR Validator", query, "Sources only mode", results)
        else:
            st.warning("⚠️ Sources-only mode requires an index. Please upload SOR documents first.")
    else:
        show_chatbot(
            vector_store=vector_store,
            session_key="sor_chat",
            label="Ask a question about SOR documents",
            input_key="sor_chat_input",
            role="SOR Validator",
        )

    show_disclaimer()
