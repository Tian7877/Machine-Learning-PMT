import sys
import os
import pandas as pd
import csv
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

    raw_emails = fetch_emails(EMAIL_USER, EMAIL_PASS, limit=PER_PAGE * 2, offset=offset)
    processed_emails = []
    for email_data in raw_emails:
        label, prob = predict_spam(email_data["body"], model, vectorizer)
        processed_emails.append({
            "subject": email_data["subject"],
            "preview": email_data["preview"],
            "body": email_data["body"],
            "label": label,
            "confidence": round(prob, 2)
        })

    if filter_val == "spam":
        processed_emails = [e for e in processed_emails if e["label"] == "SPAM"]
    elif filter_val == "ham":
        processed_emails = [e for e in processed_emails if e["label"] == "HAM"]

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
    predicted_label = request.form.get("predicted_label")
    feedback = request.form.get("feedback")

    print("📨 FEEDBACK POST RECEIVED:")
    print("message:", message[:50] if message else "[EMPTY]")
    print("predicted_label:", predicted_label)
    print("feedback:", feedback)

    if not message or not predicted_label or not feedback:
        flash("❌ Feedback tidak valid.")
        return redirect(url_for("index"))

    predicted_label = predicted_label.strip().upper()
    feedback = feedback.strip().lower()

    if predicted_label == "SPAM":
        label = "spam" if feedback == "correct" else "ham"
    elif predicted_label == "HAM":
        label = "ham" if feedback == "correct" else "spam"
    else:
        flash("❌ Label tidak dikenali.")
        return redirect(url_for("index"))

    csv_path = os.path.abspath("data/email_spam_indo.csv")
    try:
        message = message.replace('\r', ' ').replace('\n', ' ').strip()
        
        with open(csv_path, 'a', newline='', encoding='utf-8') as f:
            # Custom formatting:
            if any([c in message for c in [',', '"', '\n', '\r']]):
                message = message.replace('"', '""')  # Escape quotes
                f.write(f'{label},"{message}"\n')  # Hanya message yang dikutip
            else:
                f.write(f'{label},{message}\n')  # Tanpa quotes

        print(f"✅ Feedback disimpan: label={label} | message='{message[:40]}...'")
        
        try:
            run_training()
            flash("✔️ Feedback disimpan & model diperbarui.")
        except Exception as e:
            print(f"❌ Error saat training: {e}")
            flash("⚠️ Feedback disimpan tapi gagal update model")

    except Exception as e:
        print(f"❌ Error menyimpan feedback: {e}")
        flash("❌ Gagal menyimpan feedback.")

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
