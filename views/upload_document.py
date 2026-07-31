import os
import streamlit as st
from modules.vector_store import build_vector_store, update_vector_store

DATA_DIR = "data"

def list_indexed_files(category):
    """Return a list of files currently stored in the given category folder."""
    folder_path = os.path.join(DATA_DIR, category)
    if not os.path.exists(folder_path):
        return []
    return os.listdir(folder_path)

def show_upload_document():
    st.title("📂 Upload Document")

    # 🔒 Restrict access to Admins only
    if st.session_state.get("role") != "Admin":
        st.error("🚫 Permission Denied: Only Admins can upload documents.")
        return

    category = st.selectbox("Select document category:", ["SOP", "O&M", "SOR"])
    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "txt"])

    if uploaded_file is not None:
        # Save file to correct folder
        folder_path = os.path.join(DATA_DIR, category)
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"✅ Successfully uploaded: {uploaded_file.name}")

        # 🔄 Auto‑index based on category
        if category in ["SOP", "O&M"]:
            st.session_state.vector_store_ops = update_vector_store(file_path, "combined_ops_index")
        elif category == "SOR":
            st.session_state.vector_store_sor = update_vector_store(file_path, "SOR_index")

    # 📋 Show currently indexed files
    st.markdown("---")
    st.subheader(f"📑 Indexed {category} Files")
    files = list_indexed_files(category)
    if files:
        for f in files:
            st.write(f"• {f}")
    else:
        st.warning(f"No {category} documents indexed yet.")
