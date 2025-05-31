import joblib
from pathlib import Path
from src.preprocessing import clean_text

def load_model():
    # Menggunakan __file__ untuk mendapatkan path absolut file ini
    base_dir = Path(__file__).resolve().parent.parent  # ini akan mengarah ke project root
    model_path = base_dir / "model/spam_model.pkl"
    vec_path = base_dir / "model/tfidf_vectorizer.pkl"      
    """
    Memuat model dan TF-IDF vectorizer dari file .pkl.
    """
    model = joblib.load(model_path)
    vectorizer = joblib.load(vec_path)
    return model, vectorizer

def predict_spam(text, model, vectorizer):
    """
    Memprediksi apakah teks termasuk spam atau bukan.
    """
    cleaned = clean_text(text)
    vect_text = vectorizer.transform([cleaned])
    prediction = model.predict(vect_text)[0]
    prob = model.predict_proba(vect_text)[0][prediction]
    label = "SPAM" if prediction == 1 else "HAM"
    return label, prob

# Contoh penggunaan langsung
if __name__ == "__main__":
    model, vectorizer = load_model()
    while True:
        user_input = input("\nMasukkan email/text: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        label, confidence = predict_spam(user_input, model, vectorizer)
        print(f"Prediksi: {label} (Confidence: {confidence:.2f})")
