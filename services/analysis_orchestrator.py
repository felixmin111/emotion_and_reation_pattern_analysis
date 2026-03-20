from services.life_area.predictor_service import predict_paragraph
from services.reaction_pattern.predictor_service import hybrid_predict

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

        rows.append({
            "life_area": chunk["primary"],
            "chunk_text": chunk["text"],
            "reaction_pattern": reaction_label,
            "percent": reaction_score,
            "emotion": "Neutral"
        })

    return rows