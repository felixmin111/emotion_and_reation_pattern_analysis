import os
import pickle
from typing import Dict, List

import numpy as np
from sentence_transformers import SentenceTransformer

from services.life_area.config_data import MODEL_NAME


_embedder = None


def get_embedder() -> SentenceTransformer:
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(MODEL_NAME)
    return _embedder


def _cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    denom = (np.linalg.norm(vec_a) * np.linalg.norm(vec_b)) + 1e-12
    return float(np.dot(vec_a, vec_b) / denom)


def build_prototype_embeddings(prototypes: Dict[str, List[str]]) -> Dict[str, np.ndarray]:
    embedder = get_embedder()
    result: Dict[str, np.ndarray] = {}

    for label, examples in prototypes.items():
        emb = embedder.encode(examples, convert_to_numpy=True, normalize_embeddings=True)
        centroid = np.mean(emb, axis=0)
        centroid = centroid / (np.linalg.norm(centroid) + 1e-12)
        result[label] = centroid.astype(np.float32)

    return result


def load_or_build_prototype_embeddings(
    prototypes: Dict[str, List[str]],
    cache_path: str
) -> Dict[str, np.ndarray]:
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)

    if os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            return pickle.load(f)

    proto_embs = build_prototype_embeddings(prototypes)

    with open(cache_path, "wb") as f:
        pickle.dump(proto_embs, f)

    return proto_embs


def predict_multilabel(
    text: str,
    prototype_embeddings: Dict[str, np.ndarray],
    keyword_scores_map: Dict[str, float],
    alpha: float = 0.65,
    top_k: int = 3
):
    embedder = get_embedder()
    query_vec = embedder.encode([text], convert_to_numpy=True, normalize_embeddings=True)[0]

    semantic_scores = {
        label: _cosine_similarity(query_vec, proto_vec)
        for label, proto_vec in prototype_embeddings.items()
    }

    # Normalize semantic scores to 0..1
    sem_values = np.array(list(semantic_scores.values()), dtype=np.float32)
    sem_min = float(sem_values.min())
    sem_max = float(sem_values.max())

    if abs(sem_max - sem_min) < 1e-12:
        semantic_norm = {k: 1.0 for k in semantic_scores.keys()}
    else:
        semantic_norm = {
            k: (v - sem_min) / (sem_max - sem_min + 1e-12)
            for k, v in semantic_scores.items()
        }

    # Normalize keyword scores to 0..1
    if keyword_scores_map:
        kw_max = max(keyword_scores_map.values())
        keyword_norm = {
            label: keyword_scores_map.get(label, 0.0) / (kw_max + 1e-12)
            for label in prototype_embeddings.keys()
        }
    else:
        keyword_norm = {label: 0.0 for label in prototype_embeddings.keys()}

    combined = {
        label: alpha * semantic_norm.get(label, 0.0) + (1 - alpha) * keyword_norm.get(label, 0.0)
        for label in prototype_embeddings.keys()
    }

    ranked = sorted(combined.items(), key=lambda x: x[1], reverse=True)
    top_items = ranked[:top_k]

    primary = top_items[0][0] if top_items else None

    # multi-label selection rule
    if top_items:
        best_score = top_items[0][1]
        multi = [label for label, score in ranked if score >= best_score * 0.75]
    else:
        multi = []

    return {
        "primary": primary,
        "multi": multi,
        "ranked": top_items,
        "semantic_scores": semantic_scores,
        "keyword_scores": keyword_scores_map,
    }