import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import Flask, render_template
from src.inference import load_model, predict_spam
from web_app.email_fetcher import fetch_latest_email

app = Flask(__name__)
model, vectorizer = load_model()

# GANTI DENGAN EMAIL DAN APP PASSWORD ASLI
EMAIL_USER = "asepspakbor444@gmail.com"
EMAIL_PASS = "kelompok4indeksA"

@app.route('/')
def index():
    subject, body = fetch_latest_email(EMAIL_USER, EMAIL_PASS)
    label, prob = predict_spam(body, model, vectorizer)
    return render_template("index.html",
                           subject=subject,
                           body_preview=body[:300] + "...",
                           label=label,
                           confidence=round(prob, 2))

if __name__ == "__main__":
    app.run(debug=True)
