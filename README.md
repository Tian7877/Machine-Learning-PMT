# 📧 Spam Filter Website

Aplikasi web untuk mendeteksi dan memfilter email spam secara otomatis menggunakan Machine Learning. Proyek ini terdiri dari dua bagian utama: **Backend (Python Flask)** sebagai API dan model prediksi, serta **Frontend (React.js)** sebagai antarmuka pengguna.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-Backend-black)
![React](https://img.shields.io/badge/React.js-Frontend-61DAFB)

---

## ✨ Fitur

- Deteksi email spam secara otomatis
- Integrasi langsung dengan akun Gmail pengguna
- Antarmuka sederhana dan responsif

---

## 🔧 Prasyarat

Pastikan Anda telah menginstal:
- **Python 3.10**
- **Node.js** dan **npm**

---

## 🚀 Cara Menjalankan Proyek

### 1. Sesuaikan Username Email dan App Password
1. Buka file `app.py`
2. Ubah variabel `EMAIL_USER` dan `EMAIL_PASS` menjadi username email dan app password dari email Anda
3. Untuk Gmail, tata cara mengatur app password dapat dilihat pada [Google Support](https://support.google.com/mail/answer/185833?hl=en)

### 2. Menjalankan Backend
```bash
# Arahkan ke direktori proyek (tempat file requirement.txt berada)
pip install -r requirement.txt
python -m web_app.app
```

### 3. Menjalankan Frontend
```bash
cd web_app/templates/spam-filter-frontend
npm install
npm run dev
```

> **Catatan:** Jalankan backend terlebih dahulu agar frontend dapat terhubung dengan API dengan benar.

---

## 🌐 Akses Website

| Layanan | URL |
|---|---|
| Frontend | [http://localhost:3000](http://localhost:3000) |
| Backend (API Flask) | [http://localhost:5000](http://localhost:5000) |

---

## 📁 Struktur Proyek (Singkat)
