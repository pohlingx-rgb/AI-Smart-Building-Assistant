import streamlit as st

from modules.disclaimer import show_disclaimer

st.title("🏠 Home Dashboard")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Current User",
        st.session_state.username
    )

with col2:

    st.metric(
        "Role",
        st.session_state.role
    )

st.markdown("---")

st.subheader("Available Modules")

st.success("📘 Operations Knowledge Assistant")

st.success("🔍 SOR Validator")

st.success("📝 Question History")

st.success("ℹ️ About Us")

st.success("⚙️ Methodology")

show_disclaimer()
