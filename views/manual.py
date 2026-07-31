import streamlit as st
import os
from PyPDF2 import PdfReader
import docx

def extract_text(file_path):
    """Extract text from PDF, DOCX, or TXT files."""
    text = ""
    if file_path.endswith(".pdf"):
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() or ""
        except Exception:
            text = ""
    elif file_path.endswith(".docx"):
        try:
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        except Exception:
            text = ""
    elif file_path.endswith(".txt"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception:
            text = ""
    return text.lower()

def show_manual():
    st.title("📘 Operational Manual (View Only)")

    # Search bar
    search_query = st.text_input("🔍 Search manuals by filename or content").lower()

    data_dir = "data"
    sop_folder = os.path.join(data_dir, "SOP")
    om_folder = os.path.join(data_dir, "O&M")

    def list_files(folder, label, search_query):
        if not os.path.exists(folder):
            st.warning(f"No {label} documents uploaded yet.")
            return
        files = os.listdir(folder)

        # Apply search filter (filename + content)
        filtered_files = []
        for f in files:
            file_path = os.path.join(folder, f)
            if search_query in f.lower():
                filtered_files.append(f)
            else:
                content = extract_text(file_path)
                if search_query and search_query in content:
                    filtered_files.append(f)

        if search_query and not filtered_files:
            st.info(f"No {label} manuals match your search.")
            return

        if not files:
            st.info(f"No {label} manuals available.")
            return

        st.markdown(f"### {label}")
        for file in filtered_files if search_query else files:
            file_path = os.path.join(folder, file)
            st.download_button(
                label=f"Download {file}",
                data=open(file_path, "rb").read(),
                file_name=file,
                mime="application/octet-stream"
            )

    # Show SOP and O&M separately
    list_files(sop_folder, "Standard Operating Procedures (SOP)", search_query)
    st.markdown("---")
    list_files(om_folder, "Operation & Maintenance Manuals (O&M)", search_query)

    st.markdown("---")
    st.markdown("📝 These manuals were uploaded by Admins via the **Upload Document** page.")
