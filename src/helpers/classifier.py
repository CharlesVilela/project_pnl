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



def create_matriz_confusion(predictions, y_test, name_model, output_dir="matrizes3"):
    cm = confusion_matrix(y_test, predictions)
    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel("Previsto")
    plt.ylabel("Real")
    plt.title(f"Matriz de Confusão: {name_model}")
    # plt.show()

    base_path = "C:\Projetos\chatbot_with_pln\image"
    image_path = join(base_path, output_dir)
    # Criar diretório se não existir
    os.makedirs(image_path, exist_ok=True)

    # Gerar nome do arquivo (sem espaços)
    filename = f"{name_model.replace(' ', '_').lower()}_confusion_matrix.png"
    filepath = join(image_path, filename)

    # Salvar a imagem
    plt.savefig(filepath, dpi=300, bbox_inches='tight')


def build_pipeline(df):
    # Divisão dos dados
    x = df['text_clean']
    y = df['maturity_score']

    # 2. Dividir treino/teste
    X_train, X_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y
    )
    
    # Modelos para testar
    models = [
        (MultinomialNB(), "Naive Bayes"),
        (LogisticRegression(max_iter=1000), "Regressão Logística"),
        (RandomForestClassifier(n_estimators=100), "Random Forest")
    ]
    
    # Treino e avaliação
    for model, name in models:
       predictions = train_and_evaluate(model, name, X_train, X_test, y_train, y_test)
       create_matriz_confusion(predictions, y_test, name)
       print(f"| ### The Model: {name} ### |")
       print(classification_report(y_test, predictions, digits=3))


# Função de avaliação modificada para incluir métricas
def train_and_evaluate(model, model_name, X_train, X_test, y_train, y_test):
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000)),
        ('clf', model)
    ])
    
    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)

    filename = model_name.replace(" ", "_").lower()
    joblib.dump(pipeline, f"{filename}_maturity_model.pkl")


    return predictions