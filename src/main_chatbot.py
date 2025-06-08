import streamlit as st
import time
from queue import Queue
from collections import deque
from helpers.chatbot_interection import conversation_chatbot


def historic():
     # Exibir todas as interações exceto a última resposta do assistente
    for i, message in enumerate(st.session_state.chatbot_responses):
        if i == len(st.session_state.chatbot_responses) - 1 and message["role"] == "assistant":
            break  # pula a última resposta do assistente para exibir incrementalmente

        if message["role"] == "assistant":
            if message.get("avatar"):
                st.image(message["avatar"], width=50)
            else:
                st.chat_message(message["role"])
            for content in message["content"]:
                if content["type"] == "text":
                    st.write(content["text"])
                elif content["type"] == "audio_file":
                    st.audio(content["audio_file"])
        else:
            with st.chat_message(message["role"]):
                for content in message["content"]:
                    if content["type"] == "text":
                        st.write(content["text"])
                    elif content["type"] == "audio_file":
                        st.audio(content["audio_file"])


def display_incremental_response(text):
    """Mostra resposta de forma incremental como o ChatGPT."""
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""
        for chunk in text.split():  # ou use 'for char in text' para caractere a caractere
            full_text += chunk + " "
            placeholder.markdown(full_text + "▌")
            time.sleep(0.05)
        placeholder.markdown(full_text)

def main():
    st.title("TransforMind 🎈")

    # Inicializar a fila de mensagens se ainda não existir
    if 'chatbot_responses' not in st.session_state:
        st.session_state.chatbot_responses = deque()
    
    historic()

    # Entrada do usuário
    if (prompt := st.chat_input("Me pergunte algo.")):
        isPrimary_question = False
        
        # ✅ Mostra a pergunta do usuário imediatamente na interface
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.spinner("Hummmm... Deixe-me pensar"):
            # Formatar a data e hora sem caracteres inválidos
          response = conversation_chatbot(prompt)

        # ✅ Mostra a resposta do assistente com efeito incremental
        display_incremental_response(response)

        # ✅ Agora sim, salva pergunta e resposta no histórico para exibição futura
        st.session_state.chatbot_responses.append({
            "role": "user",
            "content": [{
                "type": "text",
                "text": prompt,
            }]
        })
        st.session_state.chatbot_responses.append({
            "role": "assistant",
            "content": [{
                "type": "text",
                "text": response,
            }]
        })
        

if __name__ == '__main__':
    main()