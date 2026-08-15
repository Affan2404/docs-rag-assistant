import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/query"

st.set_page_config(page_title="Freshdesk Docs Assistant", page_icon="💬")
st.title("Freshdesk Docs Assistant")
st.caption("Ask about Freshdesk's knowledge base, automation rules, or multilingual support.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("Sources"):
                for src in message["sources"]:
                    st.write(f"- {src['source_file']} (distance: {src['distance']:.3f})")

question = st.chat_input("Ask a question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"question": question}, timeout=30)
                response.raise_for_status()
                data = response.json()
                answer = data["answer"]
                sources = data["sources"]
            except requests.exceptions.RequestException as e:
                answer = f"Couldn't reach the backend API. Is it running? ({e})"
                sources = []

        st.markdown(answer)
        if sources:
            with st.expander("Sources"):
                for src in sources:
                    st.write(f"- {src['source_file']} (distance: {src['distance']:.3f})")

    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})