import streamlit as st
from modules.vector_store import load_vector_store
from modules.chatbot import show_chatbot

def show_operations():
    st.title("⚙️ Operations Assistant")

    # --- Status indicator ---
    if "vector_store_ops" not in st.session_state:
        st.session_state.vector_store_ops = load_vector_store("combined_ops_index")

    if st.session_state.vector_store_ops:
        st.success("✅ SOP & O&M index loaded and ready")
    else:
        st.warning("⚠️ No SOP/O&M index found. Please upload documents first.")

    st.write("Upload SOP and O&M documents on the **Upload Document** page. "
             "Then query them here using the chatbot below.")

    st.markdown("---")

    # --- Chatbot with summarization ---
    show_chatbot(
        vector_store=st.session_state.vector_store_ops,
        session_key="operations_chat",
        label="Ask a question about SOP or O&M documents",
        input_key="ops_chat_input",
        role="operations assistant"   # ✅ context for summarization
    )
