import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

from src.preprocessing import clean_text  # pastikan struktur folder

def load_and_prepare_data(csv_path: str):
    df = pd.read_csv(csv_path)
    df = df.rename(columns={'Kategori': 'label', 'Pesan': 'message'})

    # Validasi kolom
    if 'message' not in df.columns or 'label' not in df.columns:
        raise ValueError("Dataset harus memiliki kolom 'message' dan 'label'.")

    df['label'] = df['label'].map({'ham': 0, 'spam': 1})
    df['clean_text'] = df['message'].apply(clean_text)

    return df

def train_model(df: pd.DataFrame):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['clean_text'])
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = MultinomialNB()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    return model, vectorizer

def save_model(model, vectorizer, model_path="model/spam_model.pkl", vec_path="model/tfidf_vectorizer.pkl"):
    os.makedirs("model", exist_ok=True)
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vec_path)
    print(f"Model saved to {model_path}")
    print(f"Vectorizer saved to {vec_path}")

if __name__ == "__main__":
    df = load_and_prepare_data("data/email_spam_indo.csv")
    model, vectorizer = train_model(df)
    save_model(model, vectorizer)
