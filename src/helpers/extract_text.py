import fitz  # PyMuPDF
import pandas as pd
import re
from os.path import join

import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')

# 1. Extrair texto do PDF
def extrair_texto_pdf(caminho_pdf):
    try:
        doc = fitz.open(caminho_pdf)
        texto_total = ""
        for pagina in doc:
            blocos = pagina.get_text("blocks")
            for bloco in blocos:
                texto_total += bloco[4]  # O texto geralmente está no índice 4 do bloco
        doc.close()
        return texto_total
    except Exception as e:
        print(f"Ocorreu um erro ao extrair o texto: {e}")
        return None

def extrair_texto_txt(caminho_txt):
    try:
        with open(caminho_txt, 'r', encoding='utf-8') as arquivo:
            texto_total = arquivo.read()
        return texto_total
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo TXT: {e}")
        return None

# 2. Filtrar frases com base em palavras-chave
def extrair_frases_relevantes(texto, palavras_chave):
    frases = re.split(r'[.\n]', texto)
    relevantes = [
        frase.strip() for frase in frases
        if any(palavra.lower() in frase.lower() for palavra in palavras_chave) and len(frase.strip()) > 40
    ]
    return relevantes

def extract_relevant_phrases(text, key_words, min_len=30):
    phrases = sent_tokenize(text)
    relevants = []

    key_words = list(set([p.lower() for p in key_words]))

    for phrase in phrases:
        phrase_lower = phrase.lower()

        if len(phrase.strip()) < min_len:
            continue
        for word in key_words:
            if word in phrase_lower:
                relevants.append(phrase.strip())
                break
    return relevants

def salvar_txt(texto):
    try:
        with open("texto.txt", 'w', encoding='utf-8') as f:
            f.write(texto)
        print("Arquivo 'texto.txt' salvo com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao salvar o arquivo: {e}")