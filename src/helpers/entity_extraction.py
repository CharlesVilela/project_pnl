
def add_custom_entities(nlp):
    ruler = nlp.add_pipe("entity_ruler", last=True)
    patterns = [
        {"label": "TECNOLOGIA", "pattern": "nuvem"},
        {"label": "TECNOLOGIA", "pattern": "cloud computing"},
        {"label": "TECNOLOGIA", "pattern": "inteligência artificial"},
        {"label": "PROCESSO", "pattern": "metodologias ágeis"},
        {"label": "PROCESSO", "pattern": "automação"},
        {"label": "ESTRATÉGIA", "pattern": "roadmap"},
        {"label": "CULTURA", "pattern": "resistência à mudança"},
        {"label": "DADOS", "pattern": "governança de dados"}
    ]
    ruler.add_patterns(patterns)

    return ruler

def extract_entities(text, nlp):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        # Filtre todas as categorias relevantes (incluindo "CULTURA" e "DADOS")
        if ent.label_ in ["TECNOLOGIA", "PROCESSO", "ESTRATÉGIA", "CULTURA", "DADOS"]:
            entities.append((ent.text, ent.label_))
    return entities