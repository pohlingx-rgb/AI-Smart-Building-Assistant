import streamlit as st
import os
from modules.vector_store import build_vector_store
from auth.login import log_event   # reuse logging from login.py

# --- Configuration ---
DATA_DIR = "data"
SOR_FOLDER = os.path.join(DATA_DIR, "SOR")
SOP_FOLDER = os.path.join(DATA_DIR, "SOP")
OM_FOLDER = os.path.join(DATA_DIR, "O&M")

def ensure_folder(folder):
    os.makedirs(folder, exist_ok=True)

def save_uploaded_file(uploaded_file, folder):
    """Save uploaded file permanently to disk."""
    ensure_folder(folder)
    file_path = os.path.join(folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def rebuild_index(label):
    """Rebuild FAISS index after file deletion or upload."""
    try:
        if label == "Schedule of Rate (SOR)":
            st.session_state.vector_store_sor = build_vector_store(SOR_FOLDER, "SOR_index")
            st.info("SOR index rebuilt ✅")
            # Debug check
            if os.path.exists("SOR_index"):
                st.write("SOR_index contents:", os.listdir("SOR_index"))
        elif label in ["Standard Operating Procedures (SOP)", "Operation & Maintenance Manuals (O&M)"]:
            st.session_state.vector_store_ops = build_vector_store([SOP_FOLDER, OM_FOLDER], "combined_ops_index")
            st.info("Combined SOP+O&M index rebuilt ✅")
            # Debug check
            if os.path.exists("combined_ops_index"):
                st.write("combined_ops_index contents:", os.listdir("combined_ops_index"))
    except Exception as e:
        st.warning(f"Index rebuild failed: {e}")

def list_files(folder, label):
    """List stored files with download/delete options."""
    ensure_folder(folder)
    files = os.listdir(folder)

    st.markdown(f"### {label}")
    if not files:
        st.info("No files uploaded yet.")
    else:
        st.write(f"📦 {len(files)} file(s) stored")
        for idx, file in enumerate(files):
            file_path = os.path.join(folder, file)
            with open(file_path, "rb") as f:
                file_bytes = f.read()

            col1, col2 = st.columns([3, 1])
            with col1:
                st.download_button(
                    label=f"📄 Download {file}",
                    data=file_bytes,
                    file_name=file,
                    mime="application/octet-stream",
                    key=f"download_{label}_{file}_{idx}"
                )
            with col2:
                if st.session_state.get("role") == "Admin":
                    if st.button("🗑️ Delete", key=f"delete_{label}_{file}_{idx}"):
                        try:
                            os.remove(file_path)
                            st.success(f"Deleted {file} from {label}")
                            log_event(f"{st.session_state.username} deleted {file} from {label}")

                            # ✅ Rebuild index after deletion
                            rebuild_index(label)

                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting {file}: {e}")

def show_upload_document():
    st.title("📤 Upload Documents")

    st.write("Upload your SOR, SOP, and O&M documents here. "
             "They will be permanently stored and automatically indexed into FAISS for chatbot use.")

    # --- Upload SOR ---
    st.markdown("#### Schedule of Rate (SOR)")
    if st.session_state.get("role") == "Admin":
        sor_files = st.file_uploader("Choose SOR files", accept_multiple_files=True, key="sor_upload")
        if sor_files:
            for uploaded_file in sor_files:
                file_path = save_uploaded_file(uploaded_file, SOR_FOLDER)
                st.success(f"✅ Uploaded {uploaded_file.name} to SOR folder")
                log_event(f"{st.session_state.username} uploaded {uploaded_file.name} to SOR")

            # ✅ Always rebuild index from full folder
            rebuild_index("Schedule of Rate (SOR)")
    else:
        st.warning("⚠️ Upload restricted to Admin users only.")

    list_files(SOR_FOLDER, "Schedule of Rate (SOR)")

    st.markdown("---")

    # --- Upload SOP ---
    st.markdown("#### Standard Operating Procedures (SOP)")
    if st.session_state.get("role") == "Admin":
        sop_files = st.file_uploader("Choose SOP files", accept_multiple_files=True, key="sop_upload")
        if sop_files:
            for uploaded_file in sop_files:
                file_path = save_uploaded_file(uploaded_file, SOP_FOLDER)
                st.success(f"✅ Uploaded {uploaded_file.name} to SOP folder")
                log_event(f"{st.session_state.username} uploaded {uploaded_file.name} to SOP")

            rebuild_index("Standard Operating Procedures (SOP)")
    else:
        st.warning("⚠️ Upload restricted to Admin users only.")

    list_files(SOP_FOLDER, "Standard Operating Procedures (SOP)")

    st.markdown("---")

    # --- Upload O&M ---
    st.markdown("#### Operation & Maintenance Manuals (O&M)")
    if st.session_state.get("role") == "Admin":
        om_files = st.file_uploader("Choose O&M files", accept_multiple_files=True, key="om_upload")
        if om_files:
            for uploaded_file in om_files:
                file_path = save_uploaded_file(uploaded_file, OM_FOLDER)
                st.success(f"✅ Uploaded {uploaded_file.name} to O&M folder")
                log_event(f"{st.session_state.username} uploaded {uploaded_file.name} to O&M")

            rebuild_index("Operation & Maintenance Manuals (O&M)")
    else:
        st.warning("⚠️ Upload restricted to Admin users only.")

    list_files(OM_FOLDER, "Operation & Maintenance Manuals (O&M)")
