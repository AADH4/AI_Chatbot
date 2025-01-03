import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
import markdown

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
if 'input_history' not in st.session_state:
    st.session_state.input_history = []

# Function to simulate typing effect for the bot response
def typing_effect(text, delay=0.05):
    """Simulate a typing effect with the given delay per character."""
    for i in range(len(text) + 1):
        st.session_state.messages[-1]["content"] = text[:i]
        display_messages()
        time.sleep(delay)

def generate_response(prompt, history):
    # Construct the full prompt with history
    full_prompt = f"Conversation History:\n{history}\nUser: {prompt}"
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return "I'm sorry, I encountered an error processing your request."

def display_messages():
    """Display messages with appropriate style and formatting."""
    chat = st.empty()
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat.markdown(f"<div style='text-align: left; color: #0D6EFD; font-size: 16px;'><b>You</b>: {markdown.markdown(msg['content'])}</div>", unsafe_allow_html=True)
        else:
            chat.markdown(f"<div style='text-align: left; color: #28a745; font-size: 16px;'><b>Chatbot</b>: {markdown.markdown(msg['content'])}</div>", unsafe_allow_html=True)

# Add smooth scrolling CSS to the chat container
st.markdown("""
    <style>
        .streamlit-expanderHeader {
            font-size: 16px;
        }
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
        .stButton > button {
            background-color: #28a745;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
        }
        .stButton > button:hover {
            background-color: #218838;
        }
        .message-box {
            max-height: 400px;
            overflow-y: auto;
        }
    </style>
""", unsafe_allow_html=True)

# Chat display
chat_placeholder = st.empty()
display_messages()

# User input
question = st.text_input("Type your query:", key="input_field")

# Clear conversation button
if st.button("Clear Conversation"):
    st.session_state.messages = []
    chat_placeholder.empty()

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.input_history.append(question)  # Add to input history

    with st.spinner("Chatbot is thinking..."):
        # Construct conversation history string
        history = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages[:-1]])
        bot_response = generate_response(question, history)
        
    st.session_state.messages.append({"role": "chatbot", "content": ""})  # Placeholder for typing effect
    typing_effect(bot_response)  # Simulate typing effect
    display_messages()
