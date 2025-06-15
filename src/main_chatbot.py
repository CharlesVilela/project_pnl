import streamlit as st
import time
from queue import Queue
from collections import deque
from helpers.chatbot_interection import conversation_chatbot, load_resources
from dao  import connection_bd
import pandas as pd


def historic():
    # Exibe todo o histórico
    for message in st.session_state.chatbot_responses:
        if message["role"] == "assistant":
            with st.chat_message("assistant"):
                for content in message["content"]:
                    if content["type"] == "text":
                        st.write(content["text"])
                    elif content["type"] == "audio_file":
                        st.audio(content["audio_file"])
        else:
            with st.chat_message("user"):
                for content in message["content"]:
                    if content["type"] == "text":
                        st.write(content["text"])
                    elif content["type"] == "audio_file":
                        st.audio(content["audio_file"])


def display_incremental_response(text):
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""
        for chunk in text.split():
            full_text += chunk + " "
            placeholder.markdown(full_text + "▌")
            time.sleep(0.05)
        placeholder.markdown(full_text)
    return full_text


@st.cache_data(show_spinner="Carregando dados do banco...")
def load_bd():
    bd = connection_bd.find_all()
    return pd.DataFrame(bd)


def main():
    st.title("TransforMind 🎈")

    # Inicializações
    if "resources" not in st.session_state:
        df = load_bd()
        st.session_state.df = df
        with st.spinner("Preparando modelos..."):
            st.session_state.resources = load_resources(df)

    if "chatbot_responses" not in st.session_state:
        st.session_state.chatbot_responses = deque()

    # Mostra histórico antes de gerar nova resposta
    historic()

    # Entrada do usuário
    prompt = st.chat_input("Me pergunte algo.")

    # Se houve nova pergunta
    if prompt:
        # Mostrar pergunta imediatamente
        with st.chat_message("user"):
            st.write(prompt)

        # Adicionar pergunta no histórico
        st.session_state.chatbot_responses.append({
            "role": "user",
            "content": [{"type": "text", "text": prompt}]
        })

        # Gerar resposta
        with st.spinner("Gerando..."):
            response = conversation_chatbot(prompt, st.session_state.df, st.session_state.resources)

        # Exibir resposta incrementalmente
        full_response = display_incremental_response(response)

        # Adicionar resposta no histórico
        st.session_state.chatbot_responses.append({
            "role": "assistant",
            "content": [{"type": "text", "text": full_response}]
        })

        st.rerun()


if __name__ == "__main__":
    main()