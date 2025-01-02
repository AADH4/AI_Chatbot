import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Initialize model
model = genai.GenerativeModel('gemini-1.5-pro')

# Set up Streamlit page
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 AI Chatbot")
# Store conversation in session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div style='text-align: left; color: #0D6EFD;'>**You**: {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left; color: #28a745;'>**Chatbot**: {msg['content']}</div>", unsafe_allow_html=True)
question = st.text_input("Type your query:", key="input_field")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.spinner("Chatbot is thinking..."):
        time.sleep(2)
    response = model.generate_content(question)
    bot_response = response.text
    st.session_state.messages.append({"role": "chatbot", "content": bot_response})
    # Display the updated conversation
    st.experimental_rerun()
st.markdown("""
    <style>
        .stTextInput input {
            border: 2px solid #00A0D6;
            border-radius: 20px;
            padding: 11px;
            font-size: 22px;
        }
        .stTextInput input:focus {
            outline: none;
            border: 3px solid #0098A6;
        }
    </style>
""", unsafe_allow_html=True)
