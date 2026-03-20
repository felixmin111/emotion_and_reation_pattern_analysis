import json
import os
import joblib
import numpy as np

from datasets import load_dataset
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.multiclass import OneVsRestClassifier

from services.emotion.preprocessing import preprocess

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "model_store")

MODEL_PATH = os.path.join(MODEL_DIR, "emotion_model.joblib")
WORD_VECTORIZER_PATH = os.path.join(MODEL_DIR, "word_vectorizer.joblib")
CHAR_VECTORIZER_PATH = os.path.join(MODEL_DIR, "char_vectorizer.joblib")
THRESHOLDS_PATH = os.path.join(MODEL_DIR, "thresholds.npy")
EMOTION_NAMES_PATH = os.path.join(MODEL_DIR, "emotion_names.json")


def multi_hot_encode(labels, num_classes):
    multi_hot = np.zeros((len(labels), num_classes))
    for i, label_list in enumerate(labels):
        for label in label_list:
            multi_hot[i, label] = 1
    return multi_hot


def all_artifacts_exist():
    return all([
        os.path.exists(MODEL_PATH),
        os.path.exists(WORD_VECTORIZER_PATH),
        os.path.exists(CHAR_VECTORIZER_PATH),
        os.path.exists(THRESHOLDS_PATH),
        os.path.exists(EMOTION_NAMES_PATH),
    ])


def train_and_save_if_needed():
    os.makedirs(MODEL_DIR, exist_ok=True)

    if all_artifacts_exist():
        print("Emotion model artifacts already exist. Skipping training.")
        return

    print("Training emotion model...")

    ds = load_dataset("go_emotions")

    X_train = [preprocess(t) for t in ds["train"]["text"]]
    X_val = [preprocess(t) for t in ds["validation"]["text"]]

    y_train_raw = ds["train"]["labels"]
    y_val_raw = ds["validation"]["labels"]

    emotion_names = ds["train"].features["labels"].feature.names
    num_labels = len(emotion_names)

    y_train = multi_hot_encode(y_train_raw, num_labels)
    y_val = multi_hot_encode(y_val_raw, num_labels)

    word_vectorizer = TfidfVectorizer(
        max_features=50000,
        ngram_range=(1, 3),
        stop_words="english",
        sublinear_tf=True
    )

    char_vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        max_features=30000,
        sublinear_tf=True
    )

    X_train_word = word_vectorizer.fit_transform(X_train)
    X_val_word = word_vectorizer.transform(X_val)

    X_train_char = char_vectorizer.fit_transform(X_train)
    X_val_char = char_vectorizer.transform(X_val)

    X_train_tfidf = hstack([X_train_word, X_train_char])
    X_val_tfidf = hstack([X_val_word, X_val_char])

    best_f1 = 0
    best_C = 1.0

    for c in [0.1, 0.5, 1, 2, 5]:
        model = OneVsRestClassifier(
            LogisticRegression(
                C=c,
                max_iter=1000,
                class_weight="balanced",
                solver="liblinear"
            )
        )
        model.fit(X_train_tfidf, y_train)
        y_val_probs = model.predict_proba(X_val_tfidf)

        y_val_pred = (y_val_probs >= 0.5).astype(int)
        macro_f1 = f1_score(y_val, y_val_pred, average="macro", zero_division=0)

        if macro_f1 > best_f1:
            best_f1 = macro_f1
            best_C = c

    final_model = OneVsRestClassifier(
        LogisticRegression(
            C=best_C,
            max_iter=1000,
            class_weight="balanced",
            solver="liblinear"
        )
    )
    final_model.fit(X_train_tfidf, y_train)

    y_val_probs = final_model.predict_proba(X_val_tfidf)

    best_thresholds = []
    for i in range(num_labels):
        best_f1_label = 0
        best_t = 0.5

        for t in np.arange(0.1, 0.9, 0.05):
            y_pred_label = (y_val_probs[:, i] >= t).astype(int)
            f1 = f1_score(y_val[:, i], y_pred_label, zero_division=0)
            if f1 > best_f1_label:
                best_f1_label = f1
                best_t = t

        best_thresholds.append(best_t)

    joblib.dump(final_model, MODEL_PATH)
    joblib.dump(word_vectorizer, WORD_VECTORIZER_PATH)
    joblib.dump(char_vectorizer, CHAR_VECTORIZER_PATH)
    np.save(THRESHOLDS_PATH, np.array(best_thresholds))

    with open(EMOTION_NAMES_PATH, "w", encoding="utf-8") as f:
        json.dump(emotion_names, f, ensure_ascii=False, indent=2)

    print("Emotion model training complete. Artifacts saved.")