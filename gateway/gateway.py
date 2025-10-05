# gateway_service.py
from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import httpx
import json
from typing import Optional
import logging

app = FastAPI(
    title="Infinity Gateway", 
    description="Gateway untuk routing requests ke user service", 
    version="1.0"
)

logger = logging.getLogger(__name__)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base URLs for microservices
USER_SERVICE_URL = "http://toyota-user-service:8005"
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

# ========== CHAT ENDPOINTS ==========
@app.post("/chat", tags=["Chat"])
async def chat_with_assistant(request: Request):
    """Chat dengan assistant untuk konsultasi mobil"""
    try:
        body = await request.json()
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{CAR_SERVICE_URL}/chat", json=body)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process chat: {str(e)}")

@app.post("/api/chat", tags=["Chat"])
async def api_chat_with_assistant(request: Request):
    """API Chat endpoint untuk frontend PWA"""
    fallback_message = "I'm experiencing some technical difficulties. Please try again later."

    try:
        body = await request.json()
    except Exception as parse_error:
        error_message = str(parse_error) or parse_error.__class__.__name__
        logger.error("Failed to parse /api/chat request body: %s", error_message)
        return JSONResponse(
            status_code=400,
            content={
                "response": fallback_message,
                "status": "error",
                "error": "Invalid request payload"
            }
        )

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(f"{CAR_SERVICE_URL}/chat", json=body)
            response.raise_for_status()
    except httpx.HTTPStatusError as http_error:
        upstream_status = http_error.response.status_code if http_error.response else 502
        upstream_detail: Optional[str] = None
        if http_error.response:
            try:
                data = http_error.response.json()
                if isinstance(data, dict):
                    upstream_detail = (
                        data.get("detail")
                        or data.get("response")
                        or data.get("error")
                    )
            except Exception:
                upstream_detail = None

        error_message = upstream_detail or str(http_error) or http_error.__class__.__name__
        logger.error(
            "Car service /chat returned HTTP %s: %s",
            upstream_status,
            error_message
        )
        return JSONResponse(
            status_code=upstream_status,
            content={
                "response": fallback_message,
                "status": "error",
                "error": error_message
            }
        )
    except Exception as call_error:
        error_message = str(call_error) or call_error.__class__.__name__
        logger.exception("Failed to call car service /chat")
        return JSONResponse(
            status_code=502,
            content={
                "response": fallback_message,
                "status": "error",
                "error": error_message
            }
        )

    try:
        chat_response = response.json()
    except Exception as decode_error:
        error_message = str(decode_error) or decode_error.__class__.__name__
        logger.error("Failed to decode car service /chat response: %s", error_message)
        return JSONResponse(
            status_code=502,
            content={
                "response": fallback_message,
                "status": "error",
                "error": "Invalid response from car service"
            }
        )

    if not isinstance(chat_response, dict):
        chat_response = {"response": chat_response}

    response_text = (
        chat_response.get("response")
        or chat_response.get("message")
        or fallback_message
    )

    suggestions = chat_response.get("suggestions")
    if suggestions is None:
        suggestions = []
    elif isinstance(suggestions, str):
        suggestions = [suggestions]
    else:
        suggestions = list(suggestions)

    context_payload = chat_response.get("context") or {}
    if not isinstance(context_payload, dict):
        context_payload = {"value": context_payload}

    normalized_payload = {
        "response": response_text,
        "suggestions": suggestions,
        "context": context_payload,
        "status": "success"
    }

    session_id = chat_response.get("session_id")
    if not session_id and isinstance(context_payload, dict):
        session_id = context_payload.get("session_id")
    if session_id:
        normalized_payload["session_id"] = session_id

    for key, value in chat_response.items():
        if key in normalized_payload:
            continue
        normalized_payload[key] = value

    return JSONResponse(content=normalized_payload)

# ========== AUTH ENDPOINTS ==========
@app.post("/api/auth/login", tags=["Auth"])
async def login(request: Request):
    """Login endpoint untuk frontend PWA"""
    try:
        body = await request.json()
        # Simulasi autentikasi sederhana
        email = body.get("email")
        password = body.get("password")
        
        if email and password:
            # Di implementasi nyata, validasi dengan database
            return {
                "token": "dummy_jwt_token_for_demo",
                "user": {
                    "email": email,
                    "name": "Demo User"
                },
                "status": "success"
            }
        else:
            raise HTTPException(status_code=400, detail="Email and password required")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@app.post("/api/auth/register", tags=["Auth"])
async def register(request: Request):
    """Register endpoint untuk frontend PWA"""
    try:
        body = await request.json()
        name = body.get("name")
        email = body.get("email")
        password = body.get("password")
        
        if name and email and password:
            # Di implementasi nyata, simpan ke database
            return {
                "message": "Account created successfully",
                "status": "success"
            }
        else:
            raise HTTPException(status_code=400, detail="Name, email and password required")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.api_route("/mcp/cars", methods=["POST"])
async def proxy_cars(request: Request):
    """Proxy untuk MCP car_service"""
    return await forward(request, f"{CAR_SERVICE_URL}/mcp")
    
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
