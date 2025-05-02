def atribuir_score(frase):
    frase_lower = frase.lower()
    
    if any(p in frase_lower for p in ["omnichannel", "open finance", "gen ai", "dlt", "tokenization"]):
        return 5
    elif any(p in frase_lower for p in ["cloud", "rpa", "automation", "personalization"]):
        return 4
    elif any(p in frase_lower for p in ["customer experience", "onboarding", "financial literacy", "efficiency"]):
        return 3
    elif any(p in frase_lower for p in ["digital identity", "kyc", "compliance", "risk management"]):
        return 2
    else:
        return 1

def atribuir_intent(frase):
    frase_lower = frase.lower()

    if any(p in frase_lower for p in ["cloud", "cloud-native", "digital platforms"]):
        return "infraestrutura_digital"
    elif any(p in frase_lower for p in ["customer experience", "omnichannel", "cx", "personalization"]):
        return "experiencia_cliente"
    elif any(p in frase_lower for p in ["ai", "gen ai", "intelligent automation", "rpa"]):
        return "inteligencia_artificial"
    elif any(p in frase_lower for p in ["regtech", "compliance", "risk management", "dora"]):
        return "governanca_riscos"
    elif any(p in frase_lower for p in ["open finance", "embedded finance", "financial inclusion"]):
        return "modelo_negocio"
    elif any(p in frase_lower for p in ["green finance", "sustainability", "esg", "net zero"]):
        return "sustentabilidade"
    else:
        return "outros"