import streamlit as st
import csv
import os
from utils import write_message
from agent import generate_response

# Streamlit page configuration
st.set_page_config(
    page_title="IFC Chatbot",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm an IFC reader chatbot! How can I help you?"}
    ]

# Function to handle message submission
def handle_submit(message):
    with st.spinner('Thinking...'):
        # Generate assistant's response
        response = generate_response(message)

        # Display the response in the chat
        write_message('assistant', response)

        # ✅ Save interaction to CSV
        file_path = "chat_log.csv"
        file_exists = os.path.isfile(file_path)

        with open(file_path, mode="a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["User", "Assistant"])  # Write header if file doesn't exist
            writer.writerow([message, response])       # Write the current interaction

# Display chat history
for message in st.session_state.messages:
    write_message(message['role'], message['content'], save=False)

# Handle user input
if prompt := st.chat_input("Ask something about your IFC model..."):
    # Add user message to session
    write_message('user', prompt)

    # Process and respond
    handle_submit(prompt)
