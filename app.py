import streamlit as st
import textwrap
import google.generativeai as genai

def to_markdown(text):
    text = text.replace('•', ' *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

genai.configure(api_key='AIzaSyC6X6ttls6_Utpl4SgGtE4XvkbF7CafWDc')
model = genai.GenerativeModel('gemini-1.5-pro')

st.title("Gemini AI Chatbot")
question = st.text_input("Type your query:")

if question:
    response = model.generate_content(question)
    markdown_response = f"Chatbot -> {to_markdown(response.text)}"
    st.markdown(markdown_response)
