import streamlit as st
from google import genai
from google.genai import types
import os

# 1. Page Configuration
st.set_page_config(page_title="Gemini AI Assistant", page_icon="🤖")
st.title("🤖 My Free Gemini Assistant")
st.write("Welcome! Type a message below to chat with me for free.")

# 2. Automatically grab the key from Streamlit Cloud Secrets (or local environment)
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if api_key:
    # Initialize the Google GenAI Client automatically
    client = genai.Client(api_key=api_key)

    # 3. Initialize chat memory using Gemini's structure
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 4. Display past messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 5. Handle new user input
    if user_input := st.chat_input("Type something..."):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # 6. Get response from Gemini
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            
            try:
                # Format conversation history cleanly for the Gemini API
                formatted_history = []
                for msg in st.session_state.messages[:-1]:
                    api_role = "model" if msg["role"] == "assistant" else "user"
                    formatted_history.append(
                        types.Content(
                            role=api_role,
                            parts=[types.Part.from_text(text=msg["content"])]
                        )
                    )

                # Initialize chat session
                chat = client.chats.create(
                    model="gemini-2.5-flash",
                    history=formatted_history,
                    config=types.GenerateContentConfig(
                        system_instruction="You are a helpful, clear, and concise AI assistant."
                    )
                )
                
                response = chat.send_message(user_input)
                full_response = response.text
                response_placeholder.markdown(full_response)
                
            except Exception as e:
                st.error(f"Error: {e}")
                full_response = "I ran into a problem responding."
                response_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    st.error("🔑 API Key missing! Please add 'GEMINI_API_KEY' to your Streamlit Advanced Secrets dashboard.")