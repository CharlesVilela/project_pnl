import fitz  # PyMuPDF
import pandas as pd
import re
from pathlib import Path
from os.path import join
from collections import Counter
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

from resource.key_world import keywords
from resource.intent_map import intent_map
from helpers.extract_text import extract_pdf_text, extract_relevant_phrases, extract_key_words
from helpers.generated_dataset import generate_dataset
from helpers.classification_score_intent import assign_intent_from_keyword

base_path = Path(__file__).resolve().parents[2]
# 4. Rodar tudo
def extract_data(article):

    input_path = join(base_path, 'input')
    output_path = join(base_path, 'output')
    path_pdf = join(input_path, article+".pdf")

    # === 2. Initialize the KeyBERT model ===
    kw_model = KeyBERT(model='all-MiniLM-L6-v2')
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print(f"| ### 📄 Starting PDF text extraction... ### |")
    text, metadata = extract_pdf_text(path_pdf)
    print(f"| ### 🧹 Limpando texto extraído... ### |")
    # cleaned_text = clean_texts_parallel(text)
    cleaned_text = text
    print(f"| ### ✨ Text ready/finalized after cleaning... ### |")
    print(f"| ### 📑 Finished PDF text extraction... ### |")

    print(f"| ### 🔍 Starting keyword extraction... ### |")
    key_words = extract_key_words(kw_model, cleaned_text)
    print(f"| ### 🔑 Keywords extracted... ### |")

    print(f"| ### 🧠 Extracting relevant phrases based on keywords... ### |")
    phrases = extract_relevant_phrases(cleaned_text, key_words, model)
    print(f"| ### 📌 Relevant phrases extracted... ### |")

    print(f"| ### 🛠️ Generating dataset from extracted data... ### |")
    generate_dataset(phrases, metadata, key_words, model)
    print(f"| ### 📁 Dataset generation complete... ### |")





