# gateway_service.py
from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import httpx
import json
from typing import Optional

app = FastAPI(
    title="Infinity Gateway", 
    description="Gateway untuk routing requests ke user service", 
    version="1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base URLs for microservices
USER_SERVICE_URL = "http://user_service:8005"
CAR_SERVICE_URL = "http://car_service:8007"

@app.get("/health", tags=["Gateway"])
def health_check():
    return {"status": "ok", "gateway": "Infinity Gateway"}

# ========== USER ENDPOINTS ==========
@app.get("/users", tags=["User"])
async def get_users():
    """Ambil daftar semua user"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{USER_SERVICE_URL}/users")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {str(e)}")

@app.post("/users", tags=["User"])
async def create_user(request: Request):
    """Buat user baru"""
    try:
        body = await request.json()
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{USER_SERVICE_URL}/users", json=body)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

# ========== CAR ENDPOINTS ==========
@app.get("/cars", tags=["Car"])
async def get_cars():
    """Ambil semua model mobil"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{CAR_SERVICE_URL}/cars")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch cars: {str(e)}")

@app.get("/cars/{car_id}/variants", tags=["Car"])
async def get_car_variants(car_id: str):
    """Ambil varian mobil berdasarkan model"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{CAR_SERVICE_URL}/cars/{car_id}/variants")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch car variants: {str(e)}")

@app.get("/variants/{variant_id}", tags=["Car"])
async def get_variant_detail(variant_id: str):
    """Ambil detail varian mobil"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{CAR_SERVICE_URL}/variants/{variant_id}")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch variant detail: {str(e)}")

@app.get("/recommendations", tags=["Car"])
async def get_car_recommendations(request: Request):
    """Ambil rekomendasi mobil berdasarkan kriteria"""
    try:
        async with httpx.AsyncClient() as client:
            params = dict(request.query_params)
            response = await client.get(f"{CAR_SERVICE_URL}/recommendations", params=params)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch recommendations: {str(e)}")

@app.get("/compare", tags=["Car"])
async def compare_variants(request: Request):
    """Bandingkan varian mobil"""
    try:
        async with httpx.AsyncClient() as client:
            params = dict(request.query_params)
            response = await client.get(f"{CAR_SERVICE_URL}/compare", params=params)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to compare variants: {str(e)}")

@app.get("/variants/{variant_id}/accessories", tags=["Car"])
async def get_variant_accessories(variant_id: str):
    """Ambil aksesoris untuk varian tertentu"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{CAR_SERVICE_URL}/variants/{variant_id}/accessories")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch variant accessories: {str(e)}")

@app.get("/accessories", tags=["Car"])
async def get_accessories():
    """Ambil semua aksesoris"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{CAR_SERVICE_URL}/accessories")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch accessories: {str(e)}")

@app.get("/promotions", tags=["Car"])
async def get_promotions():
    """Ambil promosi yang sedang aktif"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{CAR_SERVICE_URL}/promotions")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch promotions: {str(e)}")

@app.get("/stock", tags=["Car"])
async def get_stock(request: Request):
    """Ambil informasi stok dan inden"""
    try:
        async with httpx.AsyncClient() as client:
            params = dict(request.query_params)
            response = await client.get(f"{CAR_SERVICE_URL}/stock", params=params)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stock: {str(e)}")

@app.get("/workshops", tags=["Car"])
async def get_workshops(request: Request):
    """Ambil daftar bengkel modifikasi"""
    try:
        async with httpx.AsyncClient() as client:
            params = dict(request.query_params)
            response = await client.get(f"{CAR_SERVICE_URL}/workshops", params=params)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch workshops: {str(e)}")

@app.get("/communities", tags=["Car"])
async def get_communities(request: Request):
    """Ambil daftar komunitas mobil"""
    try:
        async with httpx.AsyncClient() as client:
            params = dict(request.query_params)
            response = await client.get(f"{CAR_SERVICE_URL}/communities", params=params)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch communities: {str(e)}")

@app.get("/dress-codes", tags=["Car"])
async def get_dress_codes():
    """Ambil panduan dress code untuk staf"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{CAR_SERVICE_URL}/dress-codes")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch dress codes: {str(e)}")

# Util fungsi forwarding request
async def forward(request: Request, target_url: str):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=target_url,
            headers=dict(request.headers),
            content=await request.body()
        )
        return response.json()
