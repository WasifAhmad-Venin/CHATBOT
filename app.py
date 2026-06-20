import streamlit as st
from openai import OpenAI

# 1. Setup the web page look
st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖")
st.title("🤖 My First AI Assistant")
st.write("Welcome! Type a message below to chat with me.")

# 2. Ask the user for their API Key safely on the screen
api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")

if api_key:
    # Connect to OpenAI using the provided key
    client = OpenAI(api_key=api_key)

    # 3. Initialize chat memory
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful AI assistant."}
        ]

    # 4. Display past messages
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 5. Handle new user input
    if user_input := st.chat_input("Type something..."):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # 6. Get response from AI
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            try:
                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages,
                    stream=True,
                )
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)
            except Exception as e:
                st.error(f"Error: {e}")
                full_response = "I had trouble connecting. Please check your API key."

        st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    st.info("🔑 Please enter your OpenAI API key in the sidebar to start chatting!")