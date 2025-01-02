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
st.set_page_config(page_title="AI Chatbot", page_icon="🧠", layout="wide")

# Add title
st.title("🧠 AI Chatbot")

# Store conversation in session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Placeholder for dynamic chat display
chat_placeholder = st.empty()

# Display conversation history dynamically
with chat_placeholder.container():
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div style='text-align: left; color: #478df5; font-weight: bold;'>You: {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: left; color: #0ab4c7; font-weight: bold;'>Chatbot: {msg['content']}</div>", unsafe_allow_html=True)

# User input
question = st.text_input("Type your query:", key="input_field")

# When the user submits a query
if question:
    # Append user query to session state
    st.session_state.messages.append({"role": "user", "content": question})
    
    # Show typing animation while fetching the response
    with st.spinner("Chatbot is thinking..."):
        time.sleep(1)  # Simulate thinking process
    
    # Get chatbot response
    response = model.generate_content(question)
    bot_response = response.text
    
    # Append chatbot response to session state
    st.session_state.messages.append({"role": "chatbot", "content": bot_response})
    
    # Update the chat with new messages
    chat_placeholder.empty()  # Clear the placeholder
    with chat_placeholder.container():  # Re-render the conversation
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"<div style='text-align: left; color: #0D6EFD;'>**You**: {msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: left; color: #28a745;'>**Chatbot**: {msg['content']}</div>", unsafe_allow_html=True)

# CSS for custom message bubbles
st.markdown("""
    <style>
        .stTextInput input {
            border: 2px dashed #0092d6;
            border-radius: 18px;
            padding: 10px;
            font-size: 18px;
        }
        .stTextInput input:focus {
            outline: none;
            border: 2px dotted #10b7c7;
        }
    </style>
""", unsafe_allow_html=True)
