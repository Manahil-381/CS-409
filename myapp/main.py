import os
import re
import datetime
import streamlit as st
from together import Together
import speech_recognition as sr

# Directly define the API key in the code
TOGETHER_API_KEY = '190361560686802671ab568d93d2c02560606a26ccef82e35251f4cded12a6a6'

# Initialize Together AI client
try:
    together_client = Together(api_key=TOGETHER_API_KEY)
except Exception as e:
    st.warning(f"Together AI key error occurred: {str(e)}")
    together_client = None

def mic_function():
    recognizer = sr.Recognizer()

    if st.button('Start Listening'):
        with st.spinner('Listening for your message...'):
            try:
                # This part works only on local machine, Streamlit does not have microphone support.
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)
                    speech_text = recognizer.recognize_google(audio)

                    st.text_area('You said:', speech_text)

                    if together_client:
                        try:
                            response = together_client.chat.completions.create(
                                model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
                                messages=[{"role": "user", "content": speech_text}],
                                max_tokens=512,
                                temperature=0.7,
                                top_p=0.7,
                                top_k=50,
                                repetition_penalty=1,
                                stop=["<|eot_id|>"],
                            )
                            ai_response = response.choices[0].message.content
                            st.text_area('AI Response:', ai_response)
                        except Exception as e:
                            st.error(f"Error getting AI response: {str(e)}")
                    else:
                        st.warning("Sorry, chat functionality is currently unavailable.")
            except sr.UnknownValueError:
                st.error("Could not understand the audio.")
            except sr.RequestError as e:
                st.error(f"Error with speech recognition service: {e}")

# Chat interface for Streamlit
def chat_interface():
    st.title("Chat with AI")
    
    # Text input for messages
    message = st.text_input("Type your message:")
    
    if message:
        st.text_area("Your message:", message)
        if together_client:
            try:
                response = together_client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
                    messages=[{"role": "user", "content": message}],
                    max_tokens=512,
                    temperature=0.7,
                    top_p=0.7,
                    top_k=50,
                    repetition_penalty=1,
                    stop=["<|eot_id|>"],
                )
                ai_response = response.choices[0].message.content
                st.text_area("AI's response:", ai_response)
            except Exception as e:
                st.error(f"Error fetching AI response: {str(e)}")
        else:
            st.warning("Sorry, AI service is unavailable.")
    
    # Option for microphone-based input
    mic_function()

def run_app():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Choose a page", ["Chat", "About"])
    
    if selection == "Chat":
        chat_interface()
    elif selection == "About":
        st.write("This is a simple AI chat app built with Streamlit and Together AI.")

if __name__ == "__main__":
    run_app()
