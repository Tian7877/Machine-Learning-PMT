import sys
import os
from pathlib import Path
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import Flask, render_template, request, redirect, url_for, flash
from main import run_training 
from src.inference import load_model, predict_spam
from web_app.email_fetcher import fetch_emails

app = Flask(__name__)
app.secret_key = "kelompok_4_spam_filter"
# Load model and vectorizer 
model, vectorizer = load_model()

# Konfigurasi email
EMAIL_USER = "asepspakbor444@gmail.com"
EMAIL_PASS = "kmwy hbwb tpyg yusk"
PER_PAGE = 10


@app.route('/')
def index():
    page = int(request.args.get("page", 1))
    filter_val = request.args.get("filter", "all")
    offset = (page - 1) * PER_PAGE

    raw_emails = fetch_emails(EMAIL_USER, EMAIL_PASS, limit=PER_PAGE * 2, offset=offset)  # ambil ekstra utk filter
    processed_emails = []
    for email_data in raw_emails:
        label, prob = predict_spam(email_data["body"], model, vectorizer)
        processed_emails.append({
            "subject": email_data["subject"],
            "preview": email_data["preview"],
            "label": label,
            "confidence": round(prob, 2)
        })

    # Filter
    if filter_val == "spam":
        processed_emails = [e for e in processed_emails if e["label"] == "SPAM"]
    elif filter_val == "ham":
        processed_emails = [e for e in processed_emails if e["label"] == "HAM"]

    # Pagination logic
    displayed_emails = processed_emails[:PER_PAGE]
    has_next = len(processed_emails) > PER_PAGE

    return render_template("index.html",
                           emails=enumerate(displayed_emails),
                           page=page,
                           per_page=PER_PAGE,
                           has_next=has_next,
                           filter=filter_val)

@app.route("/feedback", methods=["POST"])
def feedback():
    message = request.form.get("message")
    predicted_label = request.form.get("predicted_label")  # 'SPAM' atau 'HAM'
    feedback = request.form.get("feedback")  # 'correct' atau 'incorrect'

    if not message or not predicted_label or not feedback:
        flash("❌ Feedback tidak valid.")
        return redirect(url_for("index"))

    # Tentukan label yang disimpan berdasarkan feedback
    if predicted_label == "SPAM":
        label = "spam" if feedback == "correct" else "ham"
    else:  # predicted HAM
        label = "ham" if feedback == "correct" else "spam"

    # Simpan ke CSV
    base_dir = Path(__file__).resolve().parent.parent  # menggunakan __file__
    csv_path = base_dir / "data/email_spam_indo.csv"
    try:
        df_new = pd.DataFrame([{"Pesan": message, "Kategori": label.strip()}])
        df_new.to_csv(csv_path, mode='a', header=False, index=False, )
        print(f"✅ Feedback disimpan: label={label} | message='{message[:40]}...'")
        run_training()
        flash("✔️ Feedback disimpan & model diperbarui.")
    except Exception as e:
        print(f"❌ Error menyimpan feedback: {e}")
        flash("❌ Gagal menyimpan feedback.")

    return redirect(url_for("index"))
if __name__ == "__main__":
    app.run(debug=True)
