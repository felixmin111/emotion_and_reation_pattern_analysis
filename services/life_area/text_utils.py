import re
from typing import List


def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def split_sentences(paragraph: str) -> List[str]:
    paragraph = normalize_text(paragraph)
    if not paragraph:
        return []

    # Split on punctuation or newline boundaries
    parts = re.split(r'(?<=[.!?])\s+|\n+', paragraph)
    sentences = [p.strip() for p in parts if p and p.strip()]
    return sentences


def normalize_token_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s']", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def contains_phrase(text: str, phrase: str) -> bool:
    text = f" {normalize_token_text(text)} "
    phrase = f" {normalize_token_text(phrase)} "
    return phrase in text