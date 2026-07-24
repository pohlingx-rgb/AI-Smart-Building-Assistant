import streamlit as st


def show_disclaimer():

    st.markdown("---")

    with st.expander(
        "⚠️ Important Notice & Disclaimer",
        expanded=False
    ):

        st.markdown("""
### IMPORTANT NOTICE

IMPORTANT NOTICE: This web application is developed as a proof-of-concept prototype. The information provided here is NOT intended for actual usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.
Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.
Always consult with qualified professionals for accurate and personalised advice.
        """)