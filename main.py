from src.train import load_and_prepare_data, train_model, save_model
from src.inference import load_model, predict_spam

def run_training():
    print("=== TRAINING MODE ===")
    df = load_and_prepare_data("data/email_spam_indo.csv")
    model, vectorizer = train_model(df)
    save_model(model, vectorizer)

def run_inference():
    print("=== INFERENCE MODE ===")
    model, vectorizer = load_model()
    while True:
        text = input("\nMasukkan teks/email (atau ketik 'exit'): ")
        if text.lower() in ["exit", "quit"]:
            break
        label, prob = predict_spam(text, model, vectorizer)
        print(f"Prediksi: {label} (Confidence: {prob:.2f})")

if __name__ == "__main__":
    print("Spam Detection CLI")
    print("===================")
    print("1. Training model")
    print("2. Inference (uji prediksi)")
    choice = input("Pilih opsi (1/2): ")

    if choice == "1":
        run_training()
    elif choice == "2":
        run_inference()
    else:
        print("Pilihan tidak valid.")
