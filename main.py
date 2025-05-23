import streamlit as st
import requests
import openai 
import os

role = st.sidebar.selectbox("Assistant personality", ["Kid-friendly", "Scholarly", "Storyteller"])
images = st.sidebar.selectbox("Image mode", ["Answers with images", "Answers without images"])
BACKEND_QUERY_URL = os.getenv("BACKEND_QUERY_URL", "http://localhost:8080/query?role=")
BACKEND_QUERY_IMAGE_URL = os.getenv("BACKEND_QUERY_IMAGE_URL", "http://localhost:8080/query/image?role=")

def main():
    init_ui()
    init_session_state()
    display_chat_history()
    handle_chat()
    
def init_ui():
    st.title("TorahAI")
    st.toast("Welcome to TorahAI! Ask me anything about the Torah.", icon="👋")
    with st.sidebar:
        st.markdown("""
        <style>
            body {
                background-color: #fcf8f3;
            }
            .stChatMessage {
                border-radius: 10px;
                padding: 10px;
            }
            .stChatMessage.user {
                background-color: #dceefb;
            }
            .stChatMessage.assistant {
                background-color: #fff9e6;
            }
        </style>
        """, unsafe_allow_html=True)

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": role, "content": "You're a helpful Torah teacher for kids."}
        ]
       
def display_chat_history():
    for msg in st.session_state.messages[1:]:  # 1 skips system prompt
        st.chat_message(msg["role"]).write(msg["content"])

def handle_chat():
    user_input = st.chat_input("Ask me a question about the Torah")
    if user_input:
        st.session_state.messages.append({"role": role, "content": user_input})
        st.chat_message("user").write(user_input)

        with st.spinner("📜..."):
            response = fetch_data(user_input)
            print(response)
            

        st.chat_message("assistant").write(response)
        
        if images == "Answers with images":
            with st.spinner("📷..."):
                image_response = fetch_image_data(response)
                st.image(image_response, caption="AI-generated illustration")
        
def fetch_data(user_input):
        url = BACKEND_QUERY_URL + "?role=" + role
        print(url)
        payload = {
                "input": user_input,
            }
        headers = {
            "Content-Type": "application/json",
            "Authorization": os.environ.get("OPENAI_API_KEY")
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.text
    
def fetch_image_data(queryResponse):
        url = BACKEND_QUERY_IMAGE_URL + "?role=" + role
        print(url)
        payload = {
            "queryResponse": queryResponse 
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": os.environ.get("OPENAI_API_KEY")
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.text

if __name__ == "__main__":
    main()
    