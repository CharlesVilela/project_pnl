import fitz  # PyMuPDF
import pandas as pd
import re
from os.path import join

from resource.key_world import palavras_chave
from helpers.extract_text import extrair_texto_pdf, extrair_frases_relevantes, salvar_txt, extract_relevant_phrases
from helpers.generated_dataset import gerar_dataset

# 4. Rodar tudo
def extract_data():
    base_path = "C:\Projetos\chatbot_with_pln"
    input_path = join(base_path, 'input')
    output_path = join(base_path, 'output')

    # caminho_pdf = join(base_path, "Capgemini_Top-Trends-2025_Retail-Banking.pdf")
    caminho_pdf = join(input_path, "artigo_01.pdf")
    # caminho_txt = join(base_path, "Capgemini_Top-Trends-2025_Retail-Banking.txt")

    texto = extrair_texto_pdf(caminho_pdf)
    # texto = extrair_texto_txt(caminho_txt)
    # frases = extrair_frases_relevantes(texto, palavras_chave)
    frases = extract_relevant_phrases(texto, palavras_chave)
    gerar_dataset(frases)
