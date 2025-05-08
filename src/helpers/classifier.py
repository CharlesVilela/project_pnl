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

from pathlib import Path
base_path = Path(__file__).resolve().parents[2]

def create_directory_matrix():
    root_image_path = Path(join(base_path, 'image'))
    # List only folders
    folders = [p for p in root_image_path.iterdir() if p.is_dir()]
    # Regular expression to extract numbers at the end of the folder name
    pattern = re.compile(r'matrices(\d+)$')
    # Extract the numbers from the existing folders
    numbers = []
    for folder in folders:
        match = pattern.match(folder.name)
        if match:
            numbers.append(int(match.group(1)))

    # Determine the next number
    next_num = max(numbers, default=0) + 1
    new_folder = root_image_path / f"matrices{next_num}"

    # Create the new folder
    new_folder.mkdir(exist_ok=True)
    print(f"Folder created: {new_folder}")

    return new_folder



def create_matriz_confusion(predictions, y_test, name_model):
    cm = confusion_matrix(y_test, predictions)
    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel("Previsto")
    plt.ylabel("Real")
    plt.title(f"Matriz de Confusão: {name_model}")
    # plt.show()

    root_image_path = join(base_path,'image')
    output_dir = create_directory_matrix()
    image_path = join(root_image_path, output_dir)

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