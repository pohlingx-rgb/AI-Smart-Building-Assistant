import streamlit as st
from auth.login import show_login   # adjust path if needed
from views.home import show_home
from views.about_us import show_about
from views.methodology import show_methodology   # ✅ lowercase file name for consistency
from views.upload_document import show_upload_document
from views.operations import show_operations_assistant   # ✅ aligned with operations.py
from views.sor_validator import show_sor_validator       # ✅ lowercase file name for consistency
from views.question_history import show_question_history          # ✅ lowercase file name for consistency

# --- Initialize session state keys ---
if "question_history" not in st.session_state:
    st.session_state.question_history = []

def main():
    # --- Initialize session state keys ---
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Home"
    if "question_history" not in st.session_state:
        st.session_state.question_history = []

    # --- Show login first ---
    if "username" not in st.session_state:
        show_login()
        return

    # Sidebar navigation
    st.sidebar.title("Navigation")

    # Role badge
    st.sidebar.markdown(
        f"**Role:** {'🔑 Admin' if st.session_state.get('role') == 'Admin' else '👤 User'}"
    )

    # Build navigation options dynamically
    nav_options = [
        "Home",
        "About Us",
        "Methodology",
        "Operations Assistant (SOP + O&M)",
        "SOR Validator (SOR only)",
        "Question History"
    ]

    # Only Admins see Upload Document
    if st.session_state.get("role") == "Admin":
        nav_options.insert(3, "Upload Document")

    selected_page = st.sidebar.radio("Go to:", nav_options, key="nav_radio_app")
    st.session_state["current_page"] = selected_page

    # Logout button
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", key="logout_sidebar"):
        st.session_state.clear()
        st.rerun()

    # Admin-only tools
    if st.session_state.get("role") == "Admin":
        st.sidebar.markdown("### Admin Tools")
        try:
            with open("audit.log", "rb") as f:
                st.sidebar.download_button(
                    label="📥 Download Audit Log",
                    data=f,
                    file_name="audit.log",
                    mime="text/plain",
                    key="download_audit_log"
                )
        except FileNotFoundError:
            st.sidebar.warning("⚠️ No audit log found yet.")

    # Routing
    page = st.session_state["current_page"]

    if page == "Home":
        show_home()
    elif page == "About Us":
        show_about()
    elif page == "Methodology":
        show_methodology()
    elif page == "Upload Document":
        show_upload_document()
    elif page == "Operations Assistant (SOP + O&M)":
        show_operations_assistant()   # ✅ no argument needed, loads index internally
    elif page == "SOR Validator (SOR only)":
        show_sor_validator()          # ✅ no argument needed, loads index internally
    elif page == "Question History":
        show_question_history()

if __name__ == "__main__":
    main()
