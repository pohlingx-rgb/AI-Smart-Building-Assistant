import streamlit as st

from modules.chatbot import log_to_history, show_chatbot
from modules.disclaimer import show_disclaimer
from modules.vector_store import load_vector_store


def show_operations_assistant():
    st.title("📑 Operations Assistant")

    if "vector_store_ops" not in st.session_state or st.session_state.vector_store_ops is None:
        st.session_state.vector_store_ops = load_vector_store("combined_ops_index")

    vector_store = st.session_state.vector_store_ops

    if vector_store:
        st.success("✅ SOP+O&M index loaded and ready")
    else:
        st.info(
            "⚠️ No SOP+O&M index found yet. Chatbot is still available, but answers won’t be based on SOP/O&M documents."
        )

    st.write("Upload SOP and O&M documents on the **Upload Document** page. Then query them here.")
    st.markdown("---")

    show_sources_only = st.checkbox("Show sources only")

    if show_sources_only:
        if vector_store:
            query = st.text_input("Enter a query to fetch sources only", key="ops_sources_input")
            if query:
                results = vector_store.similarity_search(query, k=5)
                st.subheader("📖 Supporting Sources")
                for doc in results:
                    src = doc.metadata.get("source", "unknown")
                    page = doc.metadata.get("page", "N/A")
                    st.write(f"As a Facilities Manager, I found relevant guidance in **{src}**, page {page}:")
                    st.code(doc.page_content[:500])

                log_to_history("Operations Assistant", query, "Sources only mode", results)
        else:
            st.warning("⚠️ Sources-only mode requires an index. Please upload SOP/O&M documents first.")
    else:
        show_chatbot(
            vector_store=vector_store,
            session_key="ops_chat",
            label="Ask a question about SOP/O&M documents",
            input_key="ops_chat_input",
            role="Operations Assistant",
        )

    show_disclaimer()
