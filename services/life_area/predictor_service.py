import os
from typing import Any, Dict, List

from services.life_area.chunking import chunk_by_weak_life_area, keyword_scores
from services.life_area.config_data import (
    DEFAULT_ALPHA,
    DEFAULT_TOP_K,
    MODEL_STORE_DIRNAME,
    PROTOTYPE_CACHE_FILENAME,
    PROTOTYPES,
)
from services.life_area.ml_engine import load_or_build_prototype_embeddings
from services.life_area.text_utils import split_sentences


BASE_DIR = os.path.dirname(__file__)
MODEL_STORE_DIR = os.path.join(BASE_DIR, MODEL_STORE_DIRNAME)
PROTOTYPE_CACHE_PATH = os.path.join(MODEL_STORE_DIR, PROTOTYPE_CACHE_FILENAME)

PROTOTYPE_EMBEDDINGS = load_or_build_prototype_embeddings(
    prototypes=PROTOTYPES,
    cache_path=PROTOTYPE_CACHE_PATH
)


def predict_paragraph(
    paragraph: str,
    top_k: int = DEFAULT_TOP_K,
    alpha: float = DEFAULT_ALPHA
) -> List[Dict[str, Any]]:
    sentences = split_sentences(paragraph)
    if not sentences:
        return []

    chunks = chunk_by_weak_life_area(sentences)
    results: List[Dict[str, Any]] = []

    for idx, chunk in enumerate(chunks, start=1):
        kw_scores = keyword_scores(chunk.text)

        from services.life_area.ml_engine import predict_multilabel  # local import is okay here

        pred = predict_multilabel(
            text=chunk.text,
            prototype_embeddings=PROTOTYPE_EMBEDDINGS,
            keyword_scores_map=kw_scores,
            alpha=alpha,
            top_k=top_k,
        )

        results.append({
            "chunk_index": idx,
            "text": chunk.text,
            "sentences": chunk.sentences,
            "span": chunk.span,
            "weak": chunk.weak_labels,
            "primary": pred["primary"],
            "multi": pred["multi"],
            "ranked": pred["ranked"],
            "semantic_scores": pred["semantic_scores"],
            "keyword_scores": pred["keyword_scores"],
        })

    return results