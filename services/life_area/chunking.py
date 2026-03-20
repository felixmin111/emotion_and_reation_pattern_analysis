from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

from services.life_area.config_data import KEYWORDS
from services.life_area.text_utils import normalize_token_text, contains_phrase


@dataclass
class Chunk:
    text: str
    sentences: List[str]
    span: Tuple[int, int]
    weak_labels: List[str]


def keyword_scores(text: str) -> Dict[str, float]:
    normalized = normalize_token_text(text)
    tokens = set(normalized.split())
    scores: Dict[str, float] = {}

    for label, bucket in KEYWORDS.items():
        score = 0.0

        for kw in bucket.get("strong", set()):
            if " " in kw:
                if contains_phrase(normalized, kw):
                    score += 3.0
            elif kw in tokens:
                score += 3.0

        for kw in bucket.get("weak", set()):
            if " " in kw:
                if contains_phrase(normalized, kw):
                    score += 1.0
            elif kw in tokens:
                score += 1.0

        if score > 0:
            scores[label] = score

    return scores


def weak_multilabel_guess(sentence: str) -> List[str]:
    scores = keyword_scores(sentence)
    if not scores:
        return []

    max_score = max(scores.values())
    labels = [label for label, score in scores.items() if score >= max(1.0, max_score * 0.5)]
    return labels


def overlap(a: Set[str], b: Set[str]) -> bool:
    return len(a.intersection(b)) > 0


def chunk_by_weak_life_area(sentences: List[str]) -> List[Chunk]:
    if not sentences:
        return []

    guessed = [weak_multilabel_guess(s) for s in sentences]

    chunks: List[Chunk] = []
    current_sentences: List[str] = [sentences[0]]
    current_labels: Set[str] = set(guessed[0])
    start_idx = 0

    for i in range(1, len(sentences)):
        sent = sentences[i]
        labels = set(guessed[i])

        should_merge = False

        if not current_labels and not labels:
            should_merge = True
        elif current_labels and labels and overlap(current_labels, labels):
            should_merge = True
        elif not labels and current_labels:
            should_merge = True
        elif labels and not current_labels:
            should_merge = True

        if should_merge:
            current_sentences.append(sent)
            current_labels = current_labels.union(labels)
        else:
            chunk_text = " ".join(current_sentences).strip()
            chunks.append(
                Chunk(
                    text=chunk_text,
                    sentences=current_sentences[:],
                    span=(start_idx, i - 1),
                    weak_labels=sorted(current_labels),
                )
            )
            current_sentences = [sent]
            current_labels = set(labels)
            start_idx = i

    chunk_text = " ".join(current_sentences).strip()
    chunks.append(
        Chunk(
            text=chunk_text,
            sentences=current_sentences[:],
            span=(start_idx, len(sentences) - 1),
            weak_labels=sorted(current_labels),
        )
    )

    return chunks