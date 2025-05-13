from os.path import join

import nltk
import pandas as pd
import numpy as np
import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel
from nltk.corpus import stopwords
from pprint import pprint
import pyLDAvis
import pyLDAvis.gensim_models
import matplotlib.pyplot as plt
import spacy
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.pipeline import Pipeline
import joblib

from helpers.entity_extraction import extract_entities, add_custom_entities, load_nlp_with_patterns
from helpers.preprocess import load_spacy_model, preprocess_with_spacy
from helpers.classifier import build_pipeline, train_intent_classifier

# Exemplo de estrutura real de dados (adaptar para seu contexto):
real_data = {
    "texts": [
        "Qual é o nível de adoção de cloud computing na empresa?",
        "Vocês usam ferramentas de análise de dados?",
        "Como é a cultura de inovação aqui?",
        "Quais tecnologias são utilizadas no processo produtivo?",
        "A empresa tem estratégia clara para transformação digital?"
    ],
    "intents": ["tecnologia", "tecnologia", "cultura", "processos", "estratégia"],
    "maturidade": [3, 2, 1, 2, 4]  # Exemplo de scores (0-5)
}


def process():

    base_path = "C:\Projetos\chatbot_with_pln"
    input_path = join(base_path, 'input')
    output_path = join(base_path, 'output')

    df = pd.read_csv(join(output_path, "digital_transformation_maturity2.csv"))
    # df = pd.DataFrame(real_data)

    # Configurações iniciais
    nltk.download('stopwords')
    spacy_model = load_spacy_model()
    # Criar um Entity Ruler personalizado
    nlp = load_nlp_with_patterns(spacy_model)

    # # 1. Pré-processamento
    print("🛠️ Pré-processando documentos...")
    processed_tokens = preprocess_with_spacy(df["text"], nlp)
    df["text_clean"] = [' '.join(tokens) for tokens in processed_tokens]

    print(df['maturity_score'].value_counts())

    build_pipeline(df)
    train_intent_classifier(df)
    
    print("| ### ✅ Finishing the process... ### |")