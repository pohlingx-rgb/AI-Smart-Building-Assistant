import streamlit as st

from auth.login import login

st.set_page_config(
    page_title="AI Smart Building Assistant",
    page_icon="🏢"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "question_history" not in st.session_state:
    st.session_state.question_history = []

if "uploaded_documents" not in st.session_state:
    st.session_state.uploaded_documents = []

if not st.session_state.logged_in:

    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

    login()

else:

    with st.sidebar:

        st.title("🏢 Smart Building AI")

        page = st.radio(
            "Navigation",
            [
                "Home",
                "Operations Assistant",
                "SOR Validator",
                "Question History",
                "About Us",
                "Methodology"
            ]
        )

        st.write(
            f"👤 User: {st.session_state.username}"
        )

        st.write(
            f"🔑 Role: {st.session_state.role}"
        )

        st.markdown("---")

        st.metric(
            "📂 Documents",
            len(
                st.session_state.get(
                    "uploaded_documents",
                    []
                )
            )
        )

        st.metric(
            "📝 Questions",
            len(
                st.session_state.get(
                    "question_history",
                    []
                )
            )
        )

        st.markdown("---")

        if st.button("🚪 Logout"):

            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = ""

            st.rerun()
        
    st.title("🏢 AI Smart Building Assistant")

    if page == "Home":
        exec(open("views/home.py").read())

    elif page == "Operations Assistant":
        exec(open("views/operations.py").read())

    elif page == "SOR Validator":
        exec(open("views/SOR_validator.py").read())

    elif page == "Question History":
        exec(open("views/question_history.py").read())

    elif page == "About Us":
        exec(open("views/About Us.py").read())

    elif page == "Methodology":
        exec(open("views/methodology.py").read())
    