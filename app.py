import streamlit as st
from google import genai
from google.genai import types
import os

# 1. Page Configuration (Updated to VENIN Assistant)
st.set_page_config(page_title="VENIN Assistant", page_icon="🕷️", layout="centered")
st.title("🕷️ VENIN Assistant")
st.write("Welcome. Interact with the custom-built VENIN artificial intelligence framework below.")

# 2. Automatically grab the key from Streamlit Cloud Secrets or local environment
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if api_key:
    # Initialize the Google GenAI Client
    client = genai.Client(api_key=api_key)

    # 3. Initialize chat memory
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 4. Display past messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 5. Quick Starter Prompt Buttons
    st.write("---")
    st.caption("💡 Quick operations:")
    col1, col2 = st.columns(2)
    
    button_prompt = None
    with col1:
        if st.button("🧠 Code Analysis Riddle"):
            button_prompt = "Give me a fun, short riddle related to coding or computers, but don't tell me the answer right away!"
    with col2:
        if st.button("🚀 Disruptive Startup Pitch"):
            button_prompt = "Give me a unique, funny, or futuristic startup business idea in 3 bullet points."

    # 6. Handle input
    user_input = st.chat_input("Command VENIN...")
    final_input = user_input or button_prompt

    if final_input:
        with st.chat_message("user"):
            st.markdown(final_input)
        st.session_state.messages.append({"role": "user", "content": final_input})

        # 7. Get response from Gemini
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            
            try:
                formatted_history = []
                for msg in st.session_state.messages[:-1]:
                    api_role = "model" if msg["role"] == "assistant" else "user"
                    formatted_history.append(
                        types.Content(
                            role=api_role,
                            parts=[types.Part.from_text(text=msg["content"])]
                        )
                    )

                # Initialize chat session with the customized VENIN personality
                chat = client.chats.create(
                    model="gemini-2.5-flash",
                    history=formatted_history,
                    config=types.GenerateContentConfig(
                        system_instruction="You are VENIN, a brilliant, sharp, witty, and highly capable AI assistant built by Wasif."
                    )
                )
                
                response = chat.send_message(final_input)
                full_response = response.text
                response_placeholder.markdown(full_response)
                
            except Exception as e:
                st.error(f"Error: {e}")
                full_response = "VENIN framework encountered a connection problem."
                response_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        if button_prompt:
            st.rerun()
else:
    st.error("🔑 API Key missing! Please add 'GEMINI_API_KEY' to your Streamlit Advanced Secrets dashboard.")