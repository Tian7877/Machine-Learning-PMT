import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import Flask, render_template, request
from src.inference import load_model, predict_spam
from web_app.email_fetcher import fetch_emails

app = Flask(__name__)
model, vectorizer = load_model()

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


if __name__ == "__main__":
    app.run(debug=True)
