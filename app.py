import streamlit as st
import google.generativeai as genai

genai.configure(api_key='AIzaSyC6X6ttls6_Utpl4SgGtE4XvkbF7CafWDc')
model = genai.GenerativeModel('gemini-1.5-pro')

st.title("AI Chatbot")
question = st.text_input("Type your query:")

if question:
    response = model.generate_content(question)
    markdown_response = f"Chatbot → {response.text}"
    st.markdown(markdown_response)
