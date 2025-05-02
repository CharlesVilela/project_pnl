import spacy

def load_spacy_model():
    # nlp = spacy.load("en_core_web_sm")
    # spacy.load('pt_core_news_lg')
    return spacy.load('en_core_web_sm')

# Função de pré-processamento mantida igual
def preprocess_with_spacy(texts, nlp):
    processed_texts = []
    for doc in texts:
        spacy_doc = nlp(doc.lower())
        tokens = [
            token.lemma_
            for token in spacy_doc
            if not token.is_stop and not token.is_punct
        ]
        processed_texts.append(tokens)
    return processed_texts