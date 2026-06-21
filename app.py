import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration
st.set_page_config(page_title="Gemini AI Assistant", page_icon="🤖")
st.title("🤖 My Free Gemini Assistant")
st.write("Welcome! Type a message below to chat with me for free.")

# 2. Ask the user for their Gemini API Key in the sidebar
api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

if api_key:
    # Initialize the Google GenAI Client
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
                for msg in st.session_state.messages[:-1]:  # Exclude the newest input
                    # Map role names to match Gemini's expectations ('user' and 'model')
                    api_role = "model" if msg["role"] == "assistant" else "user"
                    formatted_history.append(
                        types.Content(
                            role=api_role,
                            parts=[types.Part.from_text(text=msg["content"])]
                        )
                    )

                # Initialize a stateful chat session with history
                chat = client.chats.create(
                    model="gemini-2.5-flash",
                    history=formatted_history,
                    config=types.GenerateContentConfig(
                        system_instruction="You are a helpful, clear, and concise AI assistant."
                    )
                )
                
                # Send the newest message and capture the response
                response = chat.send_message(user_input)
                full_response = response.text
                response_placeholder.markdown(full_response)
                
            except Exception as e:
                st.error(f"Error: {e}")
                full_response = "I had trouble connecting. Please check your Gemini API key."
                response_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    st.info("🔑 Please enter your Google Gemini API key in the sidebar to start chatting!")