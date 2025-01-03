import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import markdown
import time
from datetime import datetime

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Initialize model
model = genai.GenerativeModel('gemini-1.5-pro')

# Set up Streamlit page
st.set_page_config(page_title="AI Chatbot", page_icon="🧠", layout="wide")
st.title("🧠 AI Chatbot")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'last_request_time' not in st.session_state:
    st.session_state.last_request_time = 0

# Sidebar for user options
with st.sidebar:
    st.header("Options")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
    
    if st.button("Export Conversation"):
        conversation = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages])
        st.download_button(
            label="Download Conversation",
            data=conversation,
            file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

@st.cache_data(ttl=3600)
def generate_response(prompt, history):
    # Implement rate limiting
    current_time = time.time()
    if current_time - st.session_state.last_request_time < 1:  # 1 second delay between requests
        time.sleep(1)
    st.session_state.last_request_time = current_time

    # Construct the full prompt with history
    full_prompt = f"System: You are a helpful AI assistant.\nConversation History:\n{history}\nUser: {prompt}"
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return "I'm sorry, I encountered an error processing your request."

def display_messages():
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div style='text-align: left; color: #0D6EFD;'>You: {markdown.markdown(msg['content'])}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: left; color: #28a745;'>AI: {markdown.markdown(msg['content'])}</div>", unsafe_allow_html=True)

# Chat display in the main area
display_messages()

# User input
question = st.text_input("Type your query:", key="input_field")

if question:
    # Input validation
    if question.strip() == "":
        st.warning("Please enter a valid question.")
    else:
        st.session_state.messages.append({"role": "user", "content": question})

        with st.spinner("AI is thinking..."):
            # Construct conversation history string
            history = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages[:-1]])
            
            # Stream the response
            placeholder = st.empty()
            full_response = ""
            for chunk in generate_response(question, history).split():
                full_response += chunk + " "
                placeholder.markdown(f"AI: {full_response}")
                time.sleep(0.05)

        # Add the bot's response to the session state
        st.session_state.messages.append({"role": "assistant", "content": full_response.strip()})

        # Refresh the chat interface
        display_messages()

# CSS for custom styling
st.markdown("""
    <style>
        .stTextInput input {
            border: 2px solid #0092d6;
            border-radius: 18px;
            padding: 10px;
            font-size: 18px;
        }
        .stTextInput input:focus {
            outline: none;
            border: 2px solid #10b7c7;
        }
        .stButton button {
            border-radius: 20px;
            padding: 10px 24px;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)
