import streamlit as st

from modules.disclaimer import show_disclaimer

st.title("About Us")

st.write("""
Project: AI Assistant for Smart Building Operations

Purpose:
Help Facilities Management teams search operational documents using AI.

Use Case:
Users can upload manuals, SOPs, contracts and Schedule of Rates documents,
then ask questions using natural language.

Team:
Chloe Soh Shi Ying & Loh Poh Ling
""")

show_disclaimer()