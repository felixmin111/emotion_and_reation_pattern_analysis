import numpy as np
from services.config_data import LABEL_TEMPLATES, REACTION_PATTERNS
from services.text_utils import normalize_patterns_inplace
from services.rule_engine import rule_scores
from services.ml_engine import ml_scores, build_template_embeddings

normalize_patterns_inplace(REACTION_PATTERNS)
TEMPLATE_EMB = build_template_embeddings(LABEL_TEMPLATES)

def hybrid_predict(text: str, top_k=1, alpha=0.6):
    rule = rule_scores(text)
    ml = ml_scores(text, TEMPLATE_EMB)

    ml_vals = np.array(list(ml.values()))
    ml_min, ml_max = ml_vals.min(), ml_vals.max()

    ml_norm = {
        k: (v - ml_min) / (ml_max - ml_min + 1e-9)
        for k, v in ml.items()
    }

    ml_total = sum(ml_norm.values()) + 1e-9
    ml_norm = {k: v / ml_total for k, v in ml_norm.items()}

    labels = set(rule.keys()) | set(ml_norm.keys())
    combined = {}

    for label in labels:
        combined[label] = alpha * rule.get(label, 0.0) + (1 - alpha) * ml_norm.get(label, 0.0)

    return sorted(combined.items(), key=lambda x: x[1], reverse=True)[:top_k]