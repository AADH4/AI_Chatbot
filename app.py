import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-pro')
st.title("AI Chatbot")
question = st.text_input("Type your query:")
if question:
    response = model.generate_content(question)
    markdown_response = f"Chatbot → {response.text}"
    st.markdown(markdown_response)
