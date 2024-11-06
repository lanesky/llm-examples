from openai import OpenAI
import streamlit as st

with st.sidebar:
    openai_base_url = st.text_input("Grok base url", key="openai_base_url", value="https://api.x.ai/v1")
    openai_api_key = st.text_input("Grok API Key", key="chatbot_api_key", type="password")
    "[Get an Grok API key](https://x.ai/blog/api)"
    openai_model = st.text_input("Grok model", key="openai_model",value="grok-beta")
 

st.title("💬 Grok Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your api key to continue.")
        st.stop()

    if not openai_base_url:
        st.info("Please add your Base Url to continue.")
        st.stop()

    if not openai_model:
        st.info("Please add your model to continue.")
        st.stop()

    client = OpenAI(base_url=openai_base_url, api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model=openai_model, messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
