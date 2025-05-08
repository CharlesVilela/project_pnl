import fitz  # PyMuPDF
import pandas as pd
import re
from os.path import join
import os

from helpers.classification_score_intent import atribuir_intent, atribuir_score, atribuir_entities, extract_new_intent

from pathlib import Path
base_path = Path(__file__).resolve().parents[2]

# 3. Gerar estrutura para DataFrame
def gerar_dataset(frases, new_key_words, model):
    data = []
    data_path = join(base_path, 'data')
    df_scores_intents = pd.read_csv(join(data_path, "palavras_chave_com_scores_e_intents.csv"))

    df_scores_intents = extract_new_intent(frases, new_key_words, model, df_scores_intents)

    score_map = {p.lower(): s for p, s in zip(df_scores_intents["palavra_chave"], df_scores_intents["score"])}
    intent_map = {p.lower(): intent for p, intent in zip(df_scores_intents["palavra_chave"], df_scores_intents["intent"])}
    for frase in frases:
        score = atribuir_score(frase, score_map)
        intent = atribuir_intent(frase, intent_map)
        entities = atribuir_entities(frase)
        data.append({
            "text": frase,
            "intent": intent,
            "maturity_score": score,
            "entities": entities,
            "category": "",
            "metadata": ""
        })
    save_dataframe(pd.DataFrame(data))

def save_dataframe(df):

    output_path = join(base_path, 'output')
    file_path = join(output_path, "digital_transformation_maturity.csv")
    print(df['maturity_score'].value_counts())

    if not os.path.exists(file_path):
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"✅ Arquivo salvo com {len(df)} exemplos.")
    else:
        df_dtm = pd.read_csv(file_path)
        df_concat = pd.concat([df_dtm, df])
        df_concat.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"✅ Arquivo salvo com {len(df)} exemplos.")

