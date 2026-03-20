from services.nlp_loader import nlp
from services.config_data import NEG_WORDS

def lemmatize_phrase(phrase: str) -> str:
    doc = nlp(phrase.lower())
    return " ".join(token.lemma_ for token in doc)

def normalize_patterns_inplace(patterns: dict):
    for label, items in patterns.items():
        items["single"] = sorted(set(lemmatize_phrase(w) for w in items.get("single", [])))
        items["phrase"] = sorted(set(lemmatize_phrase(p) for p in items.get("phrase", [])))

def preprocess_lemmas(text: str):
    doc = nlp(text.lower())
    lemmas = [token.lemma_ for token in doc]
    lemma_text = " ".join(lemmas)
    return doc, lemma_text

def is_in_neg_scope(doc, i, window=4):
    start = max(0, i - window)
    return any(doc[j].lower_ in NEG_WORDS for j in range(start, i + 1))