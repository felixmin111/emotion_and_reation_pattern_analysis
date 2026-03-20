import re
import numpy as np
import spacy
from sentence_transformers import SentenceTransformer, util

nlp = spacy.load("en_core_web_sm")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

LABEL_TEMPLATES = {
    "achievement_mastery": [
        "I worked hard and achieved my goal",
        "I finished something successfully",
        "I improved my skill and felt proud"
    ],
    "avoidance_withdrawal": [
        "I avoided the problem",
        "I stayed away from people",
        "I ignored the situation"
    ],
    "rumination_worry": [
        "I kept worrying about it",
        "I overthought everything",
        "I could not stop thinking about it"
    ]
}

REACTION_PATTERNS = {
    "achievement_mastery": {
        "single": ["achieve", "finish", "improve", "success", "master", "goal"],
        "phrase": ["worked hard", "reached my goal", "did my best"]
    },
    "avoidance_withdrawal": {
        "single": ["avoid", "ignore", "withdraw", "hide"],
        "phrase": ["stayed away", "ran away", "did not face"]
    },
    "rumination_worry": {
        "single": ["worry", "overthink", "anxious"],
        "phrase": ["kept thinking", "could not stop thinking"]
    }
}

LABEL_WEIGHTS = {
    "achievement_mastery": 1.3,
    "avoidance_withdrawal": 1.2,
    "rumination_worry": 1.2
}

NEG_WORDS = {"not", "never", "no", "n't"}

def lemmatize_phrase(phrase: str) -> str:
    doc = nlp(phrase.lower())
    return " ".join(token.lemma_ for token in doc)

def normalize_patterns_inplace(patterns: dict):
    for label, items in patterns.items():
        items["single"] = sorted(set(lemmatize_phrase(w) for w in items.get("single", [])))
        items["phrase"] = sorted(set(lemmatize_phrase(p) for p in items.get("phrase", [])))

normalize_patterns_inplace(REACTION_PATTERNS)

TEMPLATE_EMB = {
    label: embedder.encode(sentences, convert_to_tensor=True)
    for label, sentences in LABEL_TEMPLATES.items()
}

def preprocess_lemmas(text: str):
    doc = nlp(text.lower())
    lemmas = [token.lemma_ for token in doc]
    lemma_text = " ".join(lemmas)
    return doc, lemma_text

def is_in_neg_scope(doc, i, window=4):
    start = max(0, i - window)
    return any(doc[j].lower_ in NEG_WORDS for j in range(start, i + 1))

def count_matches_phrase_aware(doc, lemma_text: str, label_dict: dict) -> int:
    count = 0

    for phrase in label_dict.get("phrase", []):
        if re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", lemma_text):
            count += 1

    for i, tok in enumerate(doc):
        if tok.lemma_ in label_dict.get("single", []):
            if not is_in_neg_scope(doc, i):
                count += 1

    return count

def rule_scores(text: str):
    doc, lemma_text = preprocess_lemmas(text)
    raw_scores = {}

    for label, label_dict in REACTION_PATTERNS.items():
        count = count_matches_phrase_aware(doc, lemma_text, label_dict)
        if count > 0:
            raw_scores[label] = count * LABEL_WEIGHTS.get(label, 1.0)

    if not raw_scores:
        return {}

    total = sum(raw_scores.values())
    return {k: v / total for k, v in raw_scores.items()}

def ml_scores(text: str):
    x = embedder.encode([text], convert_to_tensor=True)
    scores = {}

    for label, emb in TEMPLATE_EMB.items():
        sim = util.cos_sim(x, emb).max().item()
        scores[label] = sim

    return scores

def hybrid_predict(text: str, top_k=1, alpha=0.6):
    rule = rule_scores(text)
    ml = ml_scores(text)

    ml_vals = np.array(list(ml.values()))
    ml_min, ml_max = ml_vals.min(), ml_vals.max()
    ml_norm = {k: (v - ml_min) / (ml_max - ml_min + 1e-9) for k, v in ml.items()}
    ml_total = sum(ml_norm.values()) + 1e-9
    ml_norm = {k: v / ml_total for k, v in ml_norm.items()}

    labels = set(rule.keys()) | set(ml_norm.keys())
    combined = {}

    for label in labels:
        combined[label] = alpha * rule.get(label, 0.0) + (1 - alpha) * ml_norm.get(label, 0.0)

    return sorted(combined.items(), key=lambda x: x[1], reverse=True)[:top_k]