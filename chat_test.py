import streamlit as st

st.title("Chat Test")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

question = st.chat_input("Ask me anything")
if question:
    st.session_state.chat_history.append({"role": "user", "content": question})
    st.session_state.chat_history.append({"role": "assistant", "content": f"You asked: {question}"})

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
