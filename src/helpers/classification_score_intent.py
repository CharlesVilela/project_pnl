from helpers.preprocess import load_spacy_model, preprocess_with_spacy
from helpers.entity_extraction import extract_entities, add_custom_entities, load_nlp_with_patterns
from resource.atribute_score import grupos
from resource.key_world import palavras_chave
from os.path import join
import re
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from sklearn.cluster import KMeans

from pathlib import Path
base_path = Path(__file__).resolve().parents[2]

def load_nlp():
    spacy_model = load_spacy_model()
    # Criar um Entity Ruler personalizado
    nlp = load_nlp_with_patterns(spacy_model)
    return nlp

def atribuir_entities(frase):
    nlp = load_nlp()
    return extract_entities(frase, nlp)

def atribuir_score(frase, score_map):
    frase_lower = frase.lower()
    scores_encontrados = []

    for termo, score in score_map.items():
        if termo in frase_lower:
            scores_encontrados.append(score)

    return max(scores_encontrados) if scores_encontrados else 1  # 1 = irrelevante por padrão


def atribuir_intent(frase, intent_map):
    frase_lower = frase.lower()
    intents_encontrados = []
    for termo, intent in intent_map.items():
        # Regex com bordas de palavra para evitar falsos positivos como "ai" dentro de "said"
        pattern = r'\b' + re.escape(termo) + r'\b'
        if re.search(pattern, frase_lower):
            intents_encontrados.append(intent)

    return max(set(intents_encontrados), key=intents_encontrados.count) if intents_encontrados else "others"

def atribuir_intent_from_keyword(palavra_chave, intent_map):
    palavra_lower = palavra_chave.lower()
    for intent, termos in intent_map.items():
        if any(t in palavra_lower for t in termos):
            return intent
    return "others"

def extract_new_intent(phrases, new_key_words, model, df_scores_intents):
    df_intent = df_scores_intents[["palavra_chave", "intent"]]
    existing_terms = [term[0] for term in df_intent]
    only_keywords = [kw[0] for kw in new_key_words]

    emb_existing = model.encode(existing_terms, convert_to_tensor=True)
    emb_news = model.encode(only_keywords, convert_to_tensor=True)

    # === 5. Filter new words that are not similar to existing ones (score < 0.6) ===
    suggested_terms = []
    for i, term in enumerate(only_keywords):
        score_max = util.cos_sim(emb_news[i], emb_existing).max().item()
        if score_max < 0.6:  # New enough word
            suggested_terms.append((term, score_max))

    # === 6. Cluster new terms to suggest intent groups ===
    new_terms = [termo for termo, _ in suggested_terms]
    emb_sugeridos = model.encode(new_terms)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(emb_sugeridos)

    # === 7. Organize terms by cluster ===
    clusters = {}
    for idx, label in enumerate(kmeans.labels_):
        clusters.setdefault(label, []).append(new_terms[idx])

    # === 8. Display suggested results ===
    print("\nNew potentially relevant keywords (not similar to existing ones):")
    for term, score in suggested_terms:
        print(f"- {term} (maximum similarity: {score:.2f})")

    print("\nGrouping suggestion for possible new intent:")
    for label, terms in clusters.items():
        print(f"\nSuggested Intent {label}:")
        for term in terms:
            print(f"  - {term}")

    # Agrupar por cluster
    new_clusters = {}
    labels = kmeans.labels_
    for termo, label in zip(only_keywords, labels):
        new_clusters.setdefault(label, []).append(termo)

    # Gerar nomes de cluster
    clusters_names = {label: gerar_nome_cluster(termos, model) for label, termos in new_clusters.items()}

    term_reference = df_intent.iloc[0,0]

    scores = [
        round(util.cos_sim(model.encode([term])[0], model.encode(term_reference)).item(), 2)
        for term, _ in suggested_terms
    ]

    return prepare_file_new_intent(suggested_terms, scores, labels, clusters_names, df_scores_intents)


def prepare_file_new_intent(suggested_terms, scores, labels, clusters_names, df_scores_intents):
    # === 7. Preparar dados para salvar ===
    df_final = pd.DataFrame({
        "palavra_chave": [term for term, _ in suggested_terms],
        "score": scores,
        "intent": [clusters_names[label] for label in labels]
    })

    # === 8. Salvar em CSV ===
    df_novos = pd.DataFrame(df_final)
    new_df = pd.concat([df_novos, df_scores_intents])
    data_path = join(base_path, 'data')
    new_df.to_csv(join(data_path, "palavras_chave_com_scores_e_intents.csv"))

    return new_df


# Gerar descrição semântica por cluster (automático via palavras mais centrais)
def gerar_nome_cluster(termos, modelo):
    emb_termos = modelo.encode(termos)
    centroide = emb_termos.mean(axis=0)

    # Calcular similaridade do centroide com cada termo
    sims = [(termo, util.cos_sim(modelo.encode([termo])[0], centroide).item()) for termo in termos]
    termo_mais_representativo = sorted(sims, key=lambda x: -x[1])[0][0]

    # Alternativa: juntar as 2 mais representativas
    return termo_mais_representativo.title()


def map_score_to_label(score):
    if score <= 0.33:
        return 'low'
    elif score <= 0.66:
        return 'average'
    else:
        return 'high'

