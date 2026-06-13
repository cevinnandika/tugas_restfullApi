from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from server import get_supabase_client, HEADERS

app = FastAPI(title="Backend Mahasiswa - Versi Aman JWT")

# Aktifkan CORS agar frontend bisa mengirim token tanpa diblokir browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_ENDPOINT = get_supabase_client()
security = HTTPBearer()

# Token rahasia tiruan untuk simulasi otentikasi
VALID_TOKEN = "rahasia-jwt-mahasiswa"

# Fungsi Pengecek Validitas Token JWT
def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != VALID_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau sudah kedaluwarsa!"
        )
    return token

# Skema Validasi Pydantic Data Mahasiswa
class MahasiswaSchema(BaseModel):
    nama: str
    nim: str
    jurusan: str

# Skema Validasi Pydantic Login Body
class LoginSchema(BaseModel):
    username: str
    password: str

# ----------------------------------------------------------------
# ENDPOINT LOGIN (OTENTIKASI)
# ----------------------------------------------------------------
@app.post("/login")
def login(payload: LoginSchema):
    # Validasi akun admin sederhana
    if payload.username == "admin" and payload.password == "admin123":
        return {"access_token": VALID_TOKEN, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Username atau password salah!")

# Endpoint untuk melayani halaman utama web
@app.get("/", response_class=FileResponse)
def read_index():
    path_to_html = os.path.join("templates", "index.html")
    if not os.path.exists(path_to_html):
        raise HTTPException(status_code=404, detail="File index.html tidak ditemukan")
    return path_to_html

# ================================================================
# ENDPOINT CRUD MAHASISWA (TERPROTEKSI JWT DEPENDENCY)
# ================================================================

# 1. GET ALL DATA
@app.get("/mahasiswa", status_code=200)
def get_all_mahasiswa(token: str = Depends(verify_jwt_token)):
    response = requests.get(SUPABASE_ENDPOINT, headers=HEADERS)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

# 2. CREATE (POST DATA)
@app.post("/mahasiswa", status_code=201)
def create_mahasiswa(mahasiswa: MahasiswaSchema, token: str = Depends(verify_jwt_token)):
    data_to_send = {k: v for k, v in mahasiswa.model_dump().items() if v is not None and v != ""}
    
    # Menambahkan header Prefer representation agar log bersih dari warning Supabase
    post_headers = HEADERS.copy()
    post_headers["Prefer"] = "return=representation"
    
    response = requests.post(SUPABASE_ENDPOINT, headers=post_headers, json=data_to_send)
    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

# 3. UPDATE (PUT DATA)
@app.put("/mahasiswa/{id}", status_code=200)
def update_mahasiswa(id: int, mahasiswa: MahasiswaSchema, token: str = Depends(verify_jwt_token)):
    url = f"{SUPABASE_ENDPOINT}?id=eq.{id}"
    data_to_send = {k: v for k, v in mahasiswa.model_dump().items() if v is not None and v != ""}
    
    update_headers = HEADERS.copy()
    update_headers["Prefer"] = "return=representation"
    
    response = requests.patch(url, headers=update_headers, json=data_to_send)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

# 4. DELETE DATA
@app.delete("/mahasiswa/{id}", status_code=200)
def delete_mahasiswa(id: int, token: str = Depends(verify_jwt_token)):
    url = f"{SUPABASE_ENDPOINT}?id=eq.{id}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return {"message": "Data mahasiswa berhasil dihapus"}