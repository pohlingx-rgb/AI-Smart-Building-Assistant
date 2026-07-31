import streamlit as st
from auth.login import show_login
from views.home import show_home
from views.about_us import show_about
from views.methodology import show_methodology
from views.upload_document import show_upload_document
from views.operations import show_operations
from views.sor_validator import show_sor_validator
from views.question_history import show_history
from views.manual import show_manual

from modules.vector_store import load_vector_store

# --- Initialize session state keys ---
if "question_history" not in st.session_state:
    st.session_state.question_history = []

if "vector_store_ops" not in st.session_state:
    st.session_state.vector_store_ops = load_vector_store("combined_ops_index")

if "vector_store_sor" not in st.session_state:
    st.session_state.vector_store_sor = load_vector_store("SOR_index")

# --- Main app ---
def main():
    # Check login state
    if "username" not in st.session_state:
        show_login()
        return

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to:",
        [
            "Home",
            "About Us",
            "Methodology",
            "Upload Document (Admin)",
            "Operations Assistant (SOP + O&M)",
            "SOR Validator (SOR only)",
            "Question History",
            "Operational Manual (View Only)"
            
        ],
        key="nav_radio_app"
    )

    # 🔓 Logout button always visible in sidebar
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", key="logout_sidebar"):
        st.session_state.clear()
        st.rerun()

    # Routing
    if page == "Home":
        show_home()
    elif page == "About Us":
            show_about()
    elif page == "Methodology":
        show_methodology()
    elif page == "Upload Document (Admin)":
        show_upload_document()
    elif page == "Operations Assistant (SOP + O&M)":
        show_operations()
    elif page == "SOR Validator (SOR only)":
        show_sor_validator()
    elif page == "Question History":
        show_history()
    elif page == "Operational Manual (View Only)":
        show_manual()
   


if __name__ == "__main__":
    main()
