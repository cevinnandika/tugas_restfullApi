from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from server import get_supabase_client, HEADERS

app = FastAPI(title="Backend Mahasiswa Supabase - Fixed CRUD")

# Aktifkan CORS agar browser tidak memblokir komunikasi frontend-backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_ENDPOINT = get_supabase_client()

# Model validasi data Pydantic
class MahasiswaSchema(BaseModel):
    nama: str
    nim: str
    jurusan: str

# ----------------------------------------------------------------
# 1. ENDPOINT FRONTEND: Menampilkan halaman utama web
# ----------------------------------------------------------------
@app.get("/", response_class=FileResponse)
def read_index():
    path_to_html = os.path.join("templates", "index.html")
    if not os.path.exists(path_to_html):
        raise HTTPException(status_code=404, detail="File index.html tidak ditemukan di folder templates")
    return path_to_html

# ----------------------------------------------------------------
# 2. ENDPOINT API CRUD MAHASISWA (Urutan Rapi & Bebas Error 405/401)
# ----------------------------------------------------------------

# GET ALL: Mengambil seluruh data dari Supabase
@app.get("/mahasiswa", status_code=200)
def get_all_mahasiswa():
    response = requests.get(SUPABASE_ENDPOINT, headers=HEADERS)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

# POST: Menambah data mahasiswa baru ke Supabase
@app.post("/mahasiswa", status_code=201)
def create_mahasiswa(mahasiswa: MahasiswaSchema):
    # Buang data ID atau kolom kosong agar diisi otomatis oleh identity Supabase
    data_to_send = {k: v for k, v in mahasiswa.model_dump().items() if v is not None and v != ""}
    
    # Tambahkan preferensi header agar Supabase mengembalikan data objek & log bersih
    post_headers = HEADERS.copy()
    post_headers["Prefer"] = "return=representation"
    
    response = requests.post(SUPABASE_ENDPOINT, headers=post_headers, json=data_to_send)
    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

# PUT: Mengubah data mahasiswa berdasarkan ID di Supabase
@app.put("/mahasiswa/{id}", status_code=200)
def update_mahasiswa(id: int, mahasiswa: MahasiswaSchema):
    url = f"{SUPABASE_ENDPOINT}?id=eq.{id}"
    data_to_send = {k: v for k, v in mahasiswa.model_dump().items() if v is not None and v != ""}
    
    update_headers = HEADERS.copy()
    update_headers["Prefer"] = "return=representation"
    
    response = requests.patch(url, headers=update_headers, json=data_to_send)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

# DELETE: Menghapus data mahasiswa berdasarkan ID di Supabase
@app.delete("/mahasiswa/{id}", status_code=200)
def delete_mahasiswa(id: int):
    url = f"{SUPABASE_ENDPOINT}?id=eq.{id}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return {"message": "Data mahasiswa berhasil dihapus"}