from sentence_transformers import util
from services.reaction_pattern.nlp_loader import embedder

def build_template_embeddings(label_templates: dict):
    return {
        label: embedder.encode(sentences, convert_to_tensor=True)
        for label, sentences in label_templates.items()
    }

def ml_scores(text: str, template_embeddings: dict):
    x = embedder.encode([text], convert_to_tensor=True)
    scores = {}

    for label, emb in template_embeddings.items():
        sim = util.cos_sim(x, emb).max().item()
        scores[label] = sim

    return scores