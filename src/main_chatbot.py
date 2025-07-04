import streamlit as st
import time
import uuid
from io import BytesIO
from datetime import datetime
from queue import Queue
from collections import deque
from helpers.chatbot_interection import conversation_chatbot, load_resources
from helpers.audio import transcrever_audio, texto_para_audio
from helpers.audio import GravadorAudio
from dao  import connection_bd
from utils import similarity_text, interaction
import pandas as pd
import soundfile as sf


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
    
    audio_bk = None

    # Inicializações
    if "resources" not in st.session_state:
        df = load_bd()
        st.session_state.df = df
        with st.spinner("Preparando modelos..."):
            st.session_state.resources = load_resources(df)
    if "chatbot_responses" not in st.session_state:
        st.session_state.chatbot_responses = deque()
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = str(uuid.uuid4())
        st.session_state['start_time'] = time.time()
    # isQuestionAudio = False 
    # isResponseAudio = False
    if 'isQuestionAudio' not in st.session_state:
        st.session_state.isQuestionAudio = False
    if 'isResponseAudio' not in st.session_state:
        st.session_state.isResponseAudio = False
    # Inicialização do gravador
    if 'gravador' not in st.session_state:
        st.session_state.gravador = GravadorAudio()
    
    # Inicialização de session_state
    if 'ultima_transcricao' not in st.session_state:
        st.session_state.ultima_transcricao = ""
    if 'tempo_audio' not in st.session_state:
        st.session_state.tempo_audio = 0
    if 'tempo_transcricao' not in st.session_state:
        st.session_state.tempo_transcricao = 0
    if 'timestamp' not in st.session_state:
        st.session_state.timestamp = None
    if 'pergunta_isaudio' not in st.session_state:
        st.session_state.pergunta_isaudio = False
    if 'audio_gravado' not in st.session_state:
        st.session_state.pergunta_isaudio = None
    if 'ultimo_audio' not in st.session_state:
        st.session_state.ultimo_audio = None
    
    with st.sidebar:
        st.title("Opções:")

        on = st.toggle("Ativar respostas em audio")

        # Botões de controle
        col1, col2 = st.columns([1, 3])

        with col1:
            if st.button("🎤 Iniciar Gravação", disabled=st.session_state.gravador.gravando):
                st.session_state.tempo_inicio = st.session_state.gravador.iniciar()
                st.rerun()

            if st.button("⏹️ Parar Gravação", disabled=not st.session_state.gravador.gravando):
                st.session_state["processar_audio"] = True

        with col2:
            if st.session_state.gravador.gravando:
                tempo_decorrido = time.time() - st.session_state.get('tempo_inicio', time.time())
                st.info(f"**Gravando...** Tempo: {tempo_decorrido:.1f} segundos")
                st.progress(min(tempo_decorrido / 60, 1.0))
            else:
                st.info("Pronto para gravar")

        # Processar áudio após parar gravação
        if st.session_state.get("processar_audio"):
            audio_array, duracao = st.session_state.gravador.parar()

            # Converter para BytesIO em formato WAV
            audio_buffer = BytesIO()
            sf.write(audio_buffer, audio_array, 16000, format='wav')
            audio_buffer.seek(0)

            st.session_state.ultimo_audio = audio_buffer
            texto, tempo_audio, tempo_transcricao = transcrever_audio(audio_array)
            st.session_state.ultima_transcricao = texto
            st.session_state.tempo_audio = tempo_audio
            st.session_state.tempo_transcricao = tempo_transcricao
            st.session_state.timestamp = datetime.now()

            # # Adiciona ao histórico
            # st.session_state.chatbot_responses.append({
            #     "role": "user",
            #     "content": [{
            #         "type": "audio_file",
            #         "audio_file": audio_buffer,
            #     }]
            # })
            
            # st.session_state.pergunta_isaudio = True
            
            st.session_state["processar_audio"] = False
            st.rerun()

        # # Mostrar transcrição
        # if not st.session_state.gravador.gravando and st.session_state.ultima_transcricao:
        #     st.divider()
        #     st.subheader("📝 Transcrição:")
        #     st.write(st.session_state.ultima_transcricao)

        #     st.caption(f"⏱ **Duração do áudio:** {st.session_state.tempo_audio:.1f}s | "
        #             f"**Tempo de transcrição:** {st.session_state.tempo_transcricao:.1f}s | "
        #             f"**Velocidade:** {st.session_state.tempo_audio/st.session_state.tempo_transcricao:.1f}x")

        #     st.caption(f"🕒 **Timestamp:** {st.session_state.timestamp.strftime('%d/%m/%Y %H:%M:%S')}")
            

    # Mostra histórico antes de gerar nova resposta
    historic()

    # Entrada do usuário
    user_input = st.chat_input("Me pergunte algo.")

    # Se houve entrada manual, prioriza ela; senão, usa transcrição se existir
    if user_input:
        prompt = user_input
        is_audio = False
        st.session_state.isQuestionAudio = False
    elif st.session_state.ultima_transcricao:
        prompt = st.session_state.ultima_transcricao
        # Limpa a transcrição após usar
        st.session_state.ultima_transcricao = ""
        is_audio = True
        st.session_state.isQuestionAudio = True
    else:
        prompt = None
        is_audio = False
        st.session_state.isQuestionAudio = False

    # Se houve nova pergunta
    if prompt:
        if is_audio:
             # Adiciona SOMENTE o áudio ao histórico
            with st.chat_message("user"):
                st.audio(st.session_state.ultimo_audio)
            
            st.session_state.chatbot_responses.append({
                "role": "user",
                "content": [{
                    "type": "audio_file",
                    "audio_file": st.session_state.ultimo_audio,
                }]
            })
            st.session_state.ultimo_audio = None
        else:
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
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            timestamp_start = datetime.now()
            # Gerar a resposta do chatbot
            previous_data = connection_bd.get_previous_questions()
            if previous_data is not None and len(previous_data) > 0:
                previous_questions = [item['question'] for item in previous_data]
                index, similarity = similarity_text.find_similar_question(prompt, previous_questions)
                if similarity > 0.95:
                    response = previous_data[index]['response']
                else:
                    response = conversation_chatbot(prompt, st.session_state.df, st.session_state.resources)
            else:
                response = conversation_chatbot(prompt, st.session_state.df, st.session_state.resources)

        # Checa se a conversão para áudio está ativada
        if on:
            # audio_path = f"script\\output\\audio_output_{st.session_state['user_id']}_{timestamp}.wav"
            audio = texto_para_audio(response)
            st.session_state.chatbot_responses.append({
                    "role": "assistant",
                    "content":[{
                        "type": "audio_file",
                        "audio_file": audio,
                    }]
                })
            st.session_state.isResponseAudio = True
            isResponseAudio = True
        else:
            # Exibir resposta incrementalmente
            full_response = display_incremental_response(response)

            # Adicionar resposta no histórico
            st.session_state.chatbot_responses.append({
                "role": "assistant",
                "content": [{"type": "text", "text": full_response}]
            })
        
        isQuestionAudio = st.session_state.isQuestionAudio
        isResponseAudio = st.session_state.isResponseAudio
        timestamp_end = datetime.now()
        delta = timestamp_end - timestamp_start
        time_in_seconds = delta.total_seconds()
        interaction.log_interaction(prompt, response, isQuestionAudio, isResponseAudio, time_in_seconds)

        st.rerun()


if __name__ == "__main__":
    main()