import json
import os
import joblib
import numpy as np
from scipy.sparse import hstack

from services.emotion.preprocessing import preprocess
from services.emotion.training import (
    MODEL_PATH,
    WORD_VECTORIZER_PATH,
    CHAR_VECTORIZER_PATH,
    THRESHOLDS_PATH,
    EMOTION_NAMES_PATH,
    train_and_save_if_needed,
)

BASE_DIR = os.path.dirname(__file__)

_model = None
_word_vectorizer = None
_char_vectorizer = None
_thresholds = None
_emotion_names = None


def load_emotion_artifacts():
    global _model, _word_vectorizer, _char_vectorizer, _thresholds, _emotion_names

    if _model is not None:
        return

    train_and_save_if_needed()

    _model = joblib.load(MODEL_PATH)
    _word_vectorizer = joblib.load(WORD_VECTORIZER_PATH)
    _char_vectorizer = joblib.load(CHAR_VECTORIZER_PATH)
    _thresholds = np.load(THRESHOLDS_PATH)

    with open(EMOTION_NAMES_PATH, "r", encoding="utf-8") as f:
        _emotion_names = json.load(f)


def predict_emotions(text: str, top_k: int = 3):
    load_emotion_artifacts()

    clean_text = preprocess(text)
    word_vec = _word_vectorizer.transform([clean_text])
    char_vec = _char_vectorizer.transform([clean_text])
    features = hstack([word_vec, char_vec])

    probs = _model.predict_proba(features)[0]

    selected = []
    for i, prob in enumerate(probs):
        if prob >= _thresholds[i]:
            selected.append((_emotion_names[i], float(prob)))

    if not selected:
        neutral_idx = _emotion_names.index("neutral") if "neutral" in _emotion_names else int(np.argmax(probs))
        selected = [(_emotion_names[neutral_idx], float(probs[neutral_idx]))]

    selected = sorted(selected, key=lambda x: x[1], reverse=True)
    return selected[:top_k]


def predict_primary_emotion(text: str):
    preds = predict_emotions(text, top_k=1)
    if not preds:
        return None, None
    return preds[0][0], round(preds[0][1] * 100, 2)