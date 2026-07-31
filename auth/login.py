import streamlit as st
import logging
from datetime import datetime

# Configure audit logging
logging.basicConfig(filename="audit.log", level=logging.INFO)

# Example hardcoded users (replace with DB or secure auth later)
USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "user": {"password": "user123", "role": "User"}
}

def log_event(event):
    logging.info(f"{datetime.now()} - {event}")

def show_login():
    # If already logged in, show status + logout
    if st.session_state.get("username"):
        st.sidebar.success(f"Logged in as {st.session_state.username} ({st.session_state.role})")
        if st.sidebar.button("🚪 Logout", key="logout_login"):
            log_event(f"{st.session_state.username} logged out")
            st.session_state.clear()
            st.rerun()
        return

    # Otherwise show login form
    st.title("🔐 Login")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.username = username
            st.session_state.role = USERS[username]["role"]

            st.success(f"Welcome, {username}! Role: {st.session_state.role}")
            log_event(f"{username} logged in as {st.session_state.role}")
            st.rerun()
        else:
            st.error("Invalid username or password")
            log_event(f"Failed login attempt for {username}")
