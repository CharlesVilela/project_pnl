from deep_translator import GoogleTranslator
from langid import langid


def translate_auto_to_en(text):
    if not text or len(text.strip()) < 2:
        return text
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        print(f"[⚠️ Tradução falhou]: '{text}' — {e}")
        return text

def translate_text(text, target_lang='en'):
    if not text or len(text.strip()) < 2:
        return text
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        print(f"[⚠️ Tradução falhou]: '{text}' — {e}")
        return text

def translate_pt_to_en(text):
    return GoogleTranslator(source='pt', target='en').translate(text)

def identify_language(text):
    lang, prob = langid.classify(text)
    return lang