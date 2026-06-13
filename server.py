import os
import requests
from dotenv import load_dotenv
from fastapi import HTTPException, Header

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE_NAME = os.getenv("TABLE_NAME", "mahasiswa")

# Headers standar untuk berkomunikasi dengan REST API Supabase
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def get_supabase_client():
    """Helper untuk memastikan konfigurasi Supabase sudah terisi"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("Kredensial Supabase belum dikonfigurasi di file .env")
    return f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}"

def verify_jwt_token(authorization: str = Header(None)):
    """Simulasi verifikasi token JWT untuk main_jwt.py"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Token otentikasi tidak ditemukan")
    
    try:
        token_type, token = authorization.split(" ")
        if token_type.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Tipe token harus Bearer")
        
        # Contoh simulasi: token sukses jika isinya 'rahasia-jwt-mahasiswa'
        if token != "rahasia-jwt-mahasiswa":
            raise HTTPException(status_code=401, detail="Token tidak valid atau kedaluwarsa")
            
        return {"user": "admin", "role": "authenticated"}
    except ValueError:
        raise HTTPException(status_code=401, detail="Format header Authorization tidak valid")