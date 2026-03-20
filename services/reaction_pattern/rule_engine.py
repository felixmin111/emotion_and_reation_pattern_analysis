import re
from services.reaction_pattern.config_data import REACTION_PATTERNS, LABEL_WEIGHTS
from services.reaction_pattern.text_utils import preprocess_lemmas, is_in_neg_scope

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