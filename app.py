import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import markdown

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv('AIzaSyC6X6ttls6_Utpl4SgGtE4XvkbF7CafWDc'))

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
    """Display the conversation with proper formatting."""
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div style='text-align: left; color: #0D6EFD;'>You/User: {markdown.markdown(msg['content'])}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: left; color: #28a745;'>AI Chatbot: {markdown.markdown(msg['content'])}</div>", unsafe_allow_html=True)


# Chat display
display_messages()

# User input
question = st.text_input("Type your query:", key="input_field")

# Clear conversation button
if st.button("Clear Conversation"):
    st.session_state.messages = []

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.input_history.append(question)  # Add to input history

    with st.spinner("Chatbot is thinking..."):
        # Construct conversation history string
        history = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages[:-1]])
        bot_response = generate_response(question, history)

    # Add the bot's response to the session state
    st.session_state.messages.append({"role": "chatbot", "content": bot_response})

    # Refresh the chat interface
    display_messages()

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
