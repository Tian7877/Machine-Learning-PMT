from src.train import load_and_prepare_data, train_model, save_model
from src.inference import load_model, predict_spam
import subprocess
import sys
import os

def run_training(iteration):
    print("=== TRAINING MODE ===")
    df = load_and_prepare_data("data/email_spam_indo.csv")
    model, vectorizer = train_model(df, choice=iteration)
    save_model(model, vectorizer)


def run_web_app():
    print("=== MENJALANKAN WEB APP ===")
    print("Aplikasi web akan dijalankan di http://localhost:5000")
    print("Tekan Ctrl+C untuk menghentikan server")
    
    # Dapatkan path ke app.py
    web_app_dir = os.path.join(os.path.dirname(__file__), "web_app")
    app_path = os.path.join(web_app_dir, "app.py")
    
    # Jalankan Flask app menggunakan subprocess
    try:
        subprocess.run([sys.executable, app_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error menjalankan web app: {e}")
    except KeyboardInterrupt:
        print("\nServer dihentikan")

if __name__ == "__main__":
    while True:
        print("Spam Detection System")
        print("=====================")
        print("1. Training model")
        print("2. Jalankan Web App")
        choice = input("Pilih opsi (1/2): ")

        if choice == "1":
            run_training(choice)
            break
        elif choice == "2":
            run_web_app()
            break
        else:
            print("Pilihan tidak valid. Masukan angka 1 atau 2 untuk memilih")
            print()
