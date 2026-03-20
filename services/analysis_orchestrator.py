from services.life_area.predictor_service import predict_paragraph
from services.reaction_pattern.predictor_service import hybrid_predict
from services.emotion.predictor_service import predict_primary_emotion


def analyze_journal(journal_text: str):
    life_chunks = predict_paragraph(journal_text)
    rows = []

    for chunk in life_chunks:
        reaction_results = hybrid_predict(chunk["text"], top_k=1, alpha=0.6)

        reaction_label = None
        reaction_score = None

        if reaction_results:
            reaction_label = reaction_results[0][0]
            reaction_score = round(reaction_results[0][1] * 100, 2)

        emotion_label, emotion_score = predict_primary_emotion(chunk["text"])

        rows.append({
            "life_area": chunk["primary"],
            "chunk_text": chunk["text"],
            "reaction_pattern": reaction_label,
            "percent": reaction_score,
            "emotion": emotion_label,
            "emotion_percent": emotion_score,
        })

    return rows