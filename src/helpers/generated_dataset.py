import fitz  # PyMuPDF
import pandas as pd
import re
from os.path import join
import os

from helpers.classification_score_intent import atribuir_intent, atribuir_score


# 3. Gerar estrutura para DataFrame
def gerar_dataset(frases):
    dados = []
    for frase in frases:
        score = atribuir_score(frase)
        intent = atribuir_intent(frase)
        dados.append({
            "text": frase,
            "intent": intent,
            "maturity_score": score,
            "entities": "",  # pode preencher com extrações se desejar
            "category": "banco",
            "metadata": ""
        })
    save_dataframe(pd.DataFrame(dados))

def save_dataframe(df):
    base_path = "C:\Projetos\chatbot_with_pln"
    output_path = join(base_path, 'output')

    file_path = join(output_path, "digital_transformation_maturity.csv")

    if not os.path.exists(file_path):
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"✅ Arquivo salvo com {len(df)} exemplos.")
    else:
        df_dtm = pd.read_csv(file_path)
        df_concat = pd.concat([df_dtm, df])
        df_concat.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"✅ Arquivo salvo com {len(df)} exemplos.")

