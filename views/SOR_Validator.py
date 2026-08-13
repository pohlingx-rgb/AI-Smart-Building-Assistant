import streamlit as st
from modules.vector_store import load_vector_store
from modules.chatbot import show_chatbot

def show_sor_validator():
    st.title("📑 SOR Validator")

    # --- Status indicator ---
    if "vector_store_sor" not in st.session_state:
        st.session_state.vector_store_sor = load_vector_store("SOR_index")

    if st.session_state.vector_store_sor:
        st.success("✅ SOR index loaded and ready")
    else:
        st.warning("⚠️ No SOR index found. Please upload documents first.")

    st.write(
        "Upload SOR documents on the **Upload Document** page. "
        "Then query them here using the chatbot below."
    )

    st.markdown("---")

    # --- Chatbot with summarization ---
    show_chatbot(
        vector_store=st.session_state.vector_store_sor,
        session_key="sor_chat",
        label="Ask a question about SOR documents",
        input_key="sor_chat_input",
        role="SOR validator"   # ✅ role context for summarization
    )
