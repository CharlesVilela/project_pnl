from nipype.interfaces.elastix.registration import AnalyzeWarpInputSpec
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from os.path import join
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
import re
from sentence_transformers import SentenceTransformer, util
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
from helpers.classification_score_intent import map_score_to_label

from pathlib import Path
base_path = Path(__file__).resolve().parents[2]

# Inicialize os pipelines (uma vez)
rephrase_pipe = pipeline("text2text-generation", model="Vamsi/T5_Paraphrase_Paws")

def create_directory_matrix(type_train, type_directory, base_name):
    root_image_path = Path(join(base_path, type_directory,type_train))
    # List only folders
    folders = [p for p in root_image_path.iterdir() if p.is_dir()]
    # Regular expression to extract numbers at the end of the folder name
    pattern = re.compile(f'{base_name}(\d+)$')
    # Extract the numbers from the existing folders
    numbers = []
    for folder in folders:
        match = pattern.match(folder.name)
        if match:
            numbers.append(int(match.group(1)))

    # Determine the next number
    next_num = max(numbers, default=0) + 1
    new_folder = root_image_path / f"{base_name}{next_num}"

    # Create the new folder
    new_folder.mkdir(exist_ok=True)
    print(f"Folder created: {new_folder}")

    return new_folder



def create_matriz_confusion(predictions, y_test, name_model, type_train, output_dir):
    cm = confusion_matrix(y_test, predictions)
    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel("Previsto")
    plt.ylabel("Real")
    plt.title(f"Matriz de Confusão: {name_model}")
    # plt.show()

    image_path = join(base_path, "image",type_train,output_dir)
    # Gerar nome do arquivo (sem espaços)
    filename = f"{name_model.replace(' ', '_').lower()}_confusion_matrix.png"
    filepath = join(image_path, filename)
    # Salvar a imagem
    plt.savefig(filepath, dpi=300, bbox_inches='tight')


def build_pipeline(df):

    df['maturity_label'] = df['maturity_score'].apply(map_score_to_label)

    # Divisão dos dados
    x = df['text_clean']
    y = df['maturity_label']

    # 2. Dividir treino/teste
    X_train, X_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y
    )
    
    # Modelos para testar
    models = [
        (MultinomialNB(), "Naive Bayes"),
        (LogisticRegression(max_iter=1000), "Logistic Regression"),
        (RandomForestClassifier(n_estimators=100), "Random Forest")
    ]

    type_train = "model_train_maturity_score"
    output_dir = create_directory_matrix(type_train, type_directory="image", base_name="matrices")
    version_directory = create_directory_matrix(type_train, type_directory="model_train", base_name="version")
    # Treino e avaliação
    for model, name in models:
       predictions = train_and_evaluate(model, name, X_train, X_test, y_train, y_test,type_train,version_directory)
       create_matriz_confusion(predictions, y_test, name, type_train,output_dir)
       print(f"| ### The Model: {name} ### |")
       print(classification_report(y_test, predictions, digits=3))

def train_intent_classifier(df):

    intent_counts = df['intent'].value_counts()
    valid_intents = intent_counts[intent_counts >= 2].index
    df_filtered = df[df['intent'].isin(valid_intents)]

    # Divisão dos dados
    x = df_filtered['text']
    y = df_filtered['intent']

    # 2. Dividir treino/teste
    X_train, X_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y
    )

    # Modelos para testar
    models = [
        (MultinomialNB(), "Naive Bayes"),
        (LogisticRegression(max_iter=1000), "Logistic Regression"),
        (RandomForestClassifier(n_estimators=100), "Random Forest")
    ]

    type_train = "model_train_intent"
    output_dir = create_directory_matrix(type_train, type_directory="image", base_name="matrices")
    version_directory = create_directory_matrix(type_train, type_directory="model_train", base_name="version")
    # Treino e avaliação
    for model, name in models:
        predictions = train_and_evaluate(model, name, X_train, X_test, y_train, y_test,type_train,version_directory)
        create_matriz_confusion(predictions, y_test, name, type_train,output_dir)
        print(f"| ### The Model: {name} ### |")
        print(classification_report(y_test, predictions, digits=3))
        save_classification_report(name, y_test, predictions)


# Função de avaliação modificada para incluir métricas
def train_and_evaluate(model, model_name, x_train, x_test, y_train, y_test, type_train,version_directory):
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000)),
        ('clf', model)
    ])

    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)
    filename = model_name.replace(" ", "_").lower()


    path_model = join(base_path,"model_train",type_train,version_directory)
    joblib.dump(pipeline, join(path_model, f"{filename}_maturity_model.pkl"))
    return predictions

def save_classification_report(name, y_test, predictions):
    file_path=join(base_path,"log","classification_reports.txt")
    # Gera o relatório de classificação como string
    report = classification_report(y_test, predictions, digits=3)
    
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"| ### The Model: {name} ### |\n")
        f.write(report + "\n")
        f.write("=" * 60 + "\n")

def prepare_semantic_search(df):
    corpus = df["text_clean"].tolist()
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

    embed_model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = embed_model.encode(corpus, convert_to_tensor=True)

    return tfidf_vectorizer, tfidf_matrix, embed_model, embeddings

# TF-IDF Search
def tfidf_search(query, tfidf_vectorizer, tfidf_matrix, df, top_k=3):
    query_vec = tfidf_vectorizer.transform([query])
    similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = similarity.argsort()[-top_k:][::-1]
    return df.iloc[top_indices][["text", "maturity_score", "intent"]]

# Semantic Search com SentenceTransformer
# Ajustando o top_k de 3 para 1
def semantic_search(query, model, embeddings, df, top_k=1):
    query_emb = model.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(query_emb, embeddings, top_k=top_k)[0]
    return df.iloc[[hit['corpus_id'] for hit in hits]][["text", "maturity_score", "intent"]]

def improve_question(question):
    prompt = f"paraphrase: {question} </s>"
    result = rephrase_pipe(prompt, max_length=64, do_sample=True, top_k=50)[0]['generated_text']
    return result


# Carrega os modelos salvos
def load_models():
    intent_model_path = join(base_path, "model_train", "model_train_intent", "version1",
                             "regressão_logística_maturity_model.pkl")
    maturity_model_path = join(base_path, "model_train", "model_train_maturity_score", "version1",
                               "regressão_logística_maturity_model.pkl")

    intent_model = joblib.load(intent_model_path)
    maturity_model = joblib.load(maturity_model_path)

    return intent_model, maturity_model


# Função do chatbot
def chatbot_loop(df):
    tfidf_vectorizer, tfidf_matrix, embed_model, embeddings = prepare_semantic_search(df)

    intent_model, maturity_model = load_models()

    print("\n🔹 Chatbot sobre Transformação Digital (digite 'sair' para encerrar)\n")
    while True:
        user_input = input("Você: ")
        if user_input.lower() in ['sair', 'exit', 'quit']:
            print("👋 Encerrando o chatbot. Até mais!")
            break
        user_input = improve_question(user_input)

        predicted_intent = intent_model.predict([user_input])[0]
        predicted_maturity = maturity_model.predict([user_input])[0]

        print(f"\n🎯 Intenção Detectada: {predicted_intent}")
        print(f"📈 Nível de Maturidade: {predicted_maturity}")

        print("\n🔍 Resultados mais relevantes (semânticos):")
        results = semantic_search(user_input, embed_model, embeddings, df)
        for idx, row in results.iterrows():
            print(f"\n📝 Texto: {row['text'][:300]}...")
            print(f"📈 Maturity Score: {row['maturity_score']} | 🎯 Intent: {row['intent']}")

# ANOTAÇÕES
# MODELOS NER

# Whispers tiny (Para trancrever os textos em audios ou vise-versa)
# Idea de fluxo:
# [1] Inicio
# [2] Captura da Pergunta
# [3] Pré-processamento da linguagem
# [4] Classificação e Analyze
# [5] Busca da resposta
# [6] Resposta ao usuário
# [7] feedback
# [8] Aprendizado continuo
