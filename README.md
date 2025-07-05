# Spam Filter Website

Proyek ini terdiri dari dua bagian utama: **Backend (Python Flask)** dan **Frontend (React.js)**. Pastikan mengikuti langkah-langkah di bawah ini untuk menjalankan aplikasi dengan benar.

---

## 🔧 Prasyarat

Pastikan Anda telah menginstal:

- **Python 3.10**
- **Node.js** dan **npm**

---

## 🚀 Cara Menjalankan Proyek

### 1. Sesuaikan Username email dan app password
1. Buka kode app.py
2. Ubah variabel EMAIL_USER dan EMAIL_PASS menjadi username email dan app password dari email anda
3. Untuk GMail, tata cara mengatur app password dapat dilihat pada link berikut [Google Support](https://support.google.com/mail/answer/185833?hl=en)

### 2. Menjalankan Backend

1. Buka terminal dan arahkan ke direktori proyek (tempat file `requirement.txt` berada).
2. Install semua dependensi Python:

   ```bash
   pip install -r requirement.txt
   ```

3. Jalankan backend Flask:

   ```bash
   python -m web_app.app
   ```

---

### 3. Menjalankan Frontend

1. Arahkan terminal ke folder frontend:

   ```bash
   cd web_app/templates/spam-filter-frontend
   ```

2. Install semua dependensi React:

   ```bash
   npm install
   ```

3. Jalankan server development:

   ```bash
   npm run dev
   ```

---

## 🌐 Akses Website

- Frontend tersedia di: [http://localhost:3000](http://localhost:3000)
- Backend (API Flask) tersedia di: [http://localhost:5000](http://localhost:5000)

> **Catatan:** Jalankan backend terlebih dahulu agar frontend dapat terhubung dengan API dengan benar.

---

## 📁 Struktur Proyek (Singkat)

```
...
web_app/
├── app.py
└── templates/
    └── spam-filter-frontend/
        ├── package.json
        └── ...
```

---


