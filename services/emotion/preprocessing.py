import re

contrast_patterns = [
    r"\bon the other hand\b",
    r"\bin spite of\b",
    r"\beven though\b",
    r"\bin contrast\b",
    r"\bhowever\b",
    r"\bbut\b",
    r"\balthough\b",
    r"\byet\b"
]

contrast_patterns = sorted(contrast_patterns, key=len, reverse=True)
contrast_regex = re.compile("|".join(contrast_patterns), flags=re.IGNORECASE)

def preprocess(text: str) -> str:
    if not text:
        return ""

    text = text.lower()
    text = contrast_regex.sub(" contrast_token ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text