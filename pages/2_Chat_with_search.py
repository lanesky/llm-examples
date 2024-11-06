import streamlit as st

from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun

with st.sidebar:
    openai_base_url = st.text_input("Grok base url", key="openai_base_url", value="https://api.x.ai/v1")
    openai_api_key = st.text_input("Grok API Key", key="chatbot_api_key", type="password")
    "[Get an Grok API key](https://x.ai/blog/api)"
    openai_model = st.text_input("Grok model", key="openai_model",value="grok-beta")
    

st.title("🔎 LangChain - Chat with search")


"""
In this example, we're using `StreamlitCallbackHandler` to display the thoughts and actions of an agent in an interactive Streamlit app.
Try more LangChain 🤝 Streamlit Agent examples at [github.com/langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent).

"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Who won the Women's U.S. Open in 2018?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your api key to continue.")
        st.stop()

    if not openai_base_url:
        st.info("Please add your Base Url to continue.")
        st.stop()

    if not openai_model:
        st.info("Please add your model to continue.")
        st.stop()

    llm = ChatOpenAI(model_name=openai_model, openai_api_key=openai_api_key, base_url=openai_base_url, streaming=True)
    search = DuckDuckGoSearchRun(name="Search")
    search_agent = initialize_agent(
        [search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True
    )
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
