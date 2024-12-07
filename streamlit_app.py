import streamlit as st
import requests
import json

# Set up the Streamlit interface
st.title("AI Education Chatbot")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the conversation so far
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input area
user_input = st.chat_input("Type your question related to education:")

if user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display the user input in the chat
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send user input to Flask API and get the response
    try:
        # Sending the user input to the Flask API
        response = requests.post("http://127.0.0.1:5000/api/chat", json={"user_input": user_input})
        
        if response.status_code == 200:
            ai_response = response.json().get("response")
        else:
            ai_response = "Sorry, there was an error in getting the response from AI."

        # Display AI response in the chat
        with st.chat_message("assistant"):
            st.markdown(ai_response)

        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"})
        st.markdown(f"Error: {str(e)}")
