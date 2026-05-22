# 🧠 EmpathAI - Teman Curhat Psikologi

EmpathAI adalah aplikasi chatbot interaktif berbasis AI yang dirancang untuk menjadi pendengar yang empatik, suportif, dan hangat. Aplikasi ini menggunakan prinsip-prinsip dasar psikologi seperti *Active Listening* dan *Validation* untuk menemani pengguna bercerita tentang perasaan mereka.

Aplikasi ini dibangun menggunakan **Streamlit** untuk antarmuka pengguna, **Google Gemini API** sebagai otak utama AI, dan **LangChain + ChromaDB** untuk mengintegrasikan basis pengetahuan psikologi (RAG - *Retrieval-Augmented Generation*).

---

## ✨ Fitur Utama

- **💬 Obrolan Empatik:** Mengobrol dengan AI yang disesuaikan untuk merespons dengan gaya bahasa yang natural, hangat, dan suportif.
- **🛡️ Keamanan & Krisis (Safety Guard):** Mendeteksi indikasi krisis (seperti melukai diri sendiri atau depresi berat) dan secara otomatis mengarahkan pengguna ke layanan darurat profesional. AI juga dilatih untuk menolak memberikan diagnosis medis.
- **🧠 Knowledge Base (RAG):** AI dapat merespons berdasarkan dokumen teks terkait psikologi yang diunggah ke dalam sistem, memberikan konteks yang lebih akurat.
- **📝 Ringkasan Otomatis (Memory):** Menggunakan fitur memori yang akan meringkas percakapan secara otomatis saat obrolan menjadi terlalu panjang untuk menghemat token API.
- **💾 Manajemen Obrolan:** Kemampuan untuk menyimpan obrolan, memuat riwayat obrolan sebelumnya, atau mengekspor percakapan ke file `.txt`.

---

## 🛠️ Teknologi yang Digunakan

- **Bahasa Pemrograman:** Python 3.11+
- **Frontend:** Streamlit
- **LLM (Large Language Model):** Google GenAI (Gemini)
- **RAG & Vectorstore:** LangChain & Chroma
- **Environment & Config:** `pydantic-settings`, `python-dotenv`
- **Deployment:** Docker & Docker Compose

---

## 🚀 Cara Instalasi

### 1. Prasyarat
- Python versi 3.11 atau lebih baru.
- Akun Google untuk mendapatkan Gemini API Key.

### 2. Kloning Repositori
```bash
git clone <url-repositori-anda>
cd psikolog-ai
```

### 3. Instalasi Dependensi
Proyek ini menggunakan `pyproject.toml`. Anda bisa menginstal dependensi menggunakan `uv`, `pip`, atau virtual environment standar.

Menggunakan `uv` (Direkomendasikan):
```bash
uv sync
```

Menggunakan `pip` standar:
```bash
pip install .
```

### 4. Konfigurasi Environment
Buat sebuah file bernama `.env` di direktori utama (root) proyek dan tambahkan API Key Gemini Anda:
```dotenv
GEMINI_API_KEY=API_KEY_ANDA_DI_SINI
```

---

## 📖 Cara Penggunaan

### Menjalankan Aplikasi Secara Lokal
Gunakan perintah berikut di terminal Anda untuk menjalankan server Streamlit:
```bash
streamlit run src/main.py
```
Aplikasi akan terbuka secara otomatis di browser web Anda pada `http://localhost:8501`.

### Menjalankan Menggunakan Docker
Jika Anda lebih suka menggunakan Docker, jalankan perintah berikut:
```bash
docker-compose up --build -d
```

### Menambahkan Pengetahuan Psikologi (RAG)
Untuk membuat AI lebih pintar dengan materi psikologi referensi Anda sendiri:
1. Tambahkan file `.txt` yang berisi materi psikologi ke dalam folder `data/knowledge/`.
2. Jalankan skrip inisialisasi basis pengetahuan (melalui file `knowledge_base.py`) untuk membuat *embeddings* di ChromaDB.
3. AI akan secara otomatis menarik informasi (Retrieve) dari dokumen-dokumen tersebut untuk merespons pertanyaan yang relevan.

---

## ⚠️ Disclaimer (Peringatan Penting)

**EmpathAI BUKAN pengganti psikolog, psikiater, atau terapis profesional.** 
Aplikasi ini tidak dirancang untuk memberikan diagnosis klinis atau terapi medis. Jika Anda atau seseorang yang Anda kenal sedang mengalami masa krisis, depresi berat, atau memiliki pikiran untuk mengakhiri hidup, **segera hubungi profesional kesehatan mental atau layanan darurat terdekat di daerah Anda.**

---

**Dibuat dengan ❤️ untuk mendukung kesehatan mental.**