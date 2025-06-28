import streamlit as st
import time
from datetime import datetime
import threading
import numpy as np
import sounddevice as sd
import whisper
import queue

# =======================
# ⚙️ CONFIGURAÇÕES GERAIS
# =======================

FS = 16000
BUFFER_SIZE = 1024

# Escolha o índice correto do seu microfone
MIC_DEVICE_INDEX = None  # None usa o dispositivo padrão

# =======================
# 🔊 CARREGAR MODELO WHISPER
# =======================

@st.cache_resource
def carregar_modelo():
    model = whisper.load_model("small")
    if str(model.device) == 'cpu':
        model.fp16 = False
    return model

model = carregar_modelo()

# ================================
# 🎤 FUNÇÕES DE GRAVAÇÃO
# ================================

class GravadorAudio:
    def __init__(self):
        self.fs = FS
        self.buffer_size = BUFFER_SIZE
        self.device = MIC_DEVICE_INDEX
        self.stream = None
        self.frames = []
        self.gravando = False
        self.queue = queue.Queue()
    
    def callback(self, indata, frames, time_info, status):
        if status:
            print(f"Erro de áudio: {status}")
        if self.gravando:
            self.queue.put(indata.copy())
    
    def iniciar(self):
        if self.gravando:
            return
            
        self.gravando = True
        self.frames = []
        self.queue = queue.Queue()
        
        self.stream = sd.InputStream(
            samplerate=self.fs,
            channels=1,
            dtype=np.int16,
            blocksize=self.buffer_size,
            callback=self.callback,
            device=self.device
        )
        self.stream.start()
        return time.time()
    
    def parar(self):
        if not self.gravando:
            return np.array([], dtype=np.int16), 0
            
        self.gravando = False
        
        # Aguarda processamento dos últimos buffers
        time.sleep(0.5)
        
        # Coleta todos os frames da fila
        while not self.queue.empty():
            self.frames.append(self.queue.get())
        
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        
        if self.frames:
            audio_array = np.concatenate(self.frames, axis=0)
            duracao = len(audio_array) / self.fs
            return audio_array.flatten(), duracao
        else:
            return np.array([], dtype=np.int16), 0

# ================================
# 🎙️ FUNÇÃO DE TRANSCRIÇÃO
# ================================

def transcrever_audio(audio_array):
    if audio_array.size == 0:
        return "", 0, 0

    audio_float = audio_array.astype(np.float32) / 32768.0
    inicio = time.time()
    resultado = model.transcribe(audio_float, fp16=False)
    tempo_transcricao = time.time() - inicio
    texto = resultado["text"].strip()
    tempo_audio = len(audio_array) / FS

    print("📝 Transcrição:", texto)
    print("⏱ Tempo áudio:", tempo_audio, "Tempo transcrição:", tempo_transcricao)
    return texto, tempo_audio, tempo_transcricao

# =====================
# 🌐 INTERFACE STREAMLIT
# =====================

def main():
    st.title("🎙️ Transcrição de Áudio com Whisper")

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
        
        texto, tempo_audio, tempo_transcricao = transcrever_audio(audio_array)
        st.session_state.ultima_transcricao = texto
        st.session_state.tempo_audio = tempo_audio
        st.session_state.tempo_transcricao = tempo_transcricao
        st.session_state.timestamp = datetime.now()
        
        st.session_state["processar_audio"] = False
        st.rerun()

    # Mostrar transcrição
    if not st.session_state.gravador.gravando and st.session_state.ultima_transcricao:
        st.divider()
        st.subheader("📝 Transcrição:")
        st.write(st.session_state.ultima_transcricao)

        st.caption(f"⏱ **Duração do áudio:** {st.session_state.tempo_audio:.1f}s | "
                   f"**Tempo de transcrição:** {st.session_state.tempo_transcricao:.1f}s | "
                   f"**Velocidade:** {st.session_state.tempo_audio/st.session_state.tempo_transcricao:.1f}x")

        st.caption(f"🕒 **Timestamp:** {st.session_state.timestamp.strftime('%d/%m/%Y %H:%M:%S')}")

if __name__ == "__main__":
    main()