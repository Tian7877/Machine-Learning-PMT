import sys
import os
import pandas as pd
import csv
from flask import Flask, request, jsonify
from flask_cors import CORS

# Tambahkan path agar modul bisa diimpor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import modul
from main import run_training
from src.inference import load_model, predict_spam
from web_app.email_fetcher import fetch_emails

app = Flask(__name__)
CORS(app)  # Aktifkan CORS untuk semua route

# Konfigurasi email
EMAIL_USER = "[email_user]@gmail.com"  # Ganti dengan email Anda
EMAIL_PASS = "[email_pass]"  # Ganti dengan app password Anda
PER_PAGE = 10


@app.route('/emails', methods=["GET"])
def get_emails():
    try:
        model, vectorizer = load_model()
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

        return jsonify({
            "success": True,
            "emails": displayed_emails,
            "page": page,
            "per_page": PER_PAGE,
            "has_next": has_next,
            "filter": filter_val
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json()

    message = data.get("message")
    predicted_label = data.get("predicted_label")
    feedback = data.get("feedback")

    if not message or not predicted_label or not feedback:
        return jsonify({"success": False, "message": "❌ Feedback tidak valid."}), 400

    predicted_label = predicted_label.strip().upper()
    feedback = feedback.strip().lower()

    if predicted_label == "SPAM":
        label = "spam" if feedback == "correct" else "ham"
    elif predicted_label == "HAM":
        label = "ham" if feedback == "correct" else "spam"
    else:
        return jsonify({"success": False, "message": "❌ Label tidak dikenali."}), 400

    csv_path = os.path.abspath("data/email_spam_indo.csv")

    try:
        # Normalisasi message
        message = message.replace('\r', ' ').replace('\n', ' ').strip()

        # Cek apakah newline dibutuhkan
        with open(csv_path, 'rb+') as f:
            f.seek(0, os.SEEK_END)
            if f.tell() == 0:
                need_newline = False
            else:
                f.seek(-1, os.SEEK_END)
                last_char = f.read(1)
                need_newline = last_char != b'\n'

            if need_newline:
                f.write(b'\n')

        # Tulis ke CSV
        with open(csv_path, 'a', newline='', encoding='utf-8') as f:
            if '"' in message or ',' in message:
                message_escaped = message.replace('"', '""')
                f.write(f'{label},"{message_escaped}"\n')
            else:
                f.write(f'{label},{message}\n')

        # Lakukan retraining
        try:
            run_training(iteration='2')
            return jsonify({"success": True, "message": "✔️ Feedback disimpan & model diperbarui."}), 200
        except Exception as e:
            return jsonify({"success": True, "message": "⚠️ Feedback disimpan tapi gagal update model", "error": str(e)}), 200

    except Exception as e:
        return jsonify({"success": False, "message": "❌ Gagal menyimpan feedback.", "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
