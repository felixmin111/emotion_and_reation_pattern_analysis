from flask import Flask, render_template, request
from services.predictor_service import hybrid_predict

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    journal_text = ""
    top_label = None
    top_score = None

    if request.method == "POST":
        journal_text = request.form.get("journal_text", "").strip()

        if journal_text:
            results = hybrid_predict(journal_text, top_k=1, alpha=0.6)
            if results:
                top_label = results[0][0]
                top_score = round(results[0][1] * 100, 2)

    return render_template(
        "index.html",
        journal_text=journal_text,
        top_label=top_label,
        top_score=top_score
    )

if __name__ == "__main__":
    app.run(debug=True)