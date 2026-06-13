# 🎓 Sistem Informasi Data Mahasiswa (FastAPI + Supabase + JWT Auth)

Aplikasi web manajemen data mahasiswa berbasis **Full-Stack** sederhana yang mengintegrasikan backend modern **FastAPI (Python)**, database cloud **Supabase (PostgreSQL)**, serta sistem proteksi keamanan menggunakan **JSON Web Token (JWT)**. Tampilan frontend menggunakan satu file HTML utuh berbasis **Bootstrap 5** agar responsif dan mudah dikembangkan.

---

## 🚀 Fitur Utama
* **Autentikasi Keamanan JWT**: Endpoint CRUD dikunci menggunakan satelit pengaman Token Bearer JWT.
* **Operasi CRUD Real-time**: Mengambil (GET), menambah (POST), mengubah (PUT), dan menghapus (DELETE) data langsung ke Supabase Cloud.
* **Manajemen RLS (Row Level Security)**: Konfigurasi bypass RLS database untuk fleksibilitas API pihak ketiga.
* **Dokumentasi Otomatis (Swagger UI)**: Pengujian endpoint langsung yang interaktif melalui `/docs`.
* **Desain Responsif**: Antarmuka berbasis komponen Card dan Table yang scannable menggunakan Bootstrap 5.

---

## 📁 Struktur Proyek
```text
PROJECT_PBW/
│
├── templates/
│   └── index.html      # Frontend (HTML, CSS internal, & JS Fetch API)
│
├── .env                # Variabel lingkungan rahasia (Supabase URL & API Key)
├── server.py           # Konfigurasi koneksi & header dasar Supabase
├── main.py             # Backend CRUD standar (Tanpa Keamanan)
├── main_jwt.py         # Backend CRUD utama dengan proteksi JWT Auth
└── venv/               # Virtual Environment Python
