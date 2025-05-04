import streamlit as st
import requests
import openai 
import os
import query_embeddings as qe

st.title("TorahAI")


def main():
    init_session_state()
    display_chat_history()
    handle_chat()

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You're a helpful Torah teacher for kids."}
        ]

def display_chat_history():
    for msg in st.session_state.messages[1:]:  # 1 skips system prompt
        st.chat_message(msg["role"]).write(msg["content"])

def handle_chat():
    user_input = st.chat_input("Ask me a question about the Torah")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        with st.spinner("Thinking... 🧠"):
            result = qe.vector_search_query(user_input) 
            similar_verses = qe.search_similar_verses(result)
            build_prompt = qe.build_prompt(similar_verses, user_input)
            response = qe.ask_openai(build_prompt)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
        
if __name__ == "__main__":
    main()
    