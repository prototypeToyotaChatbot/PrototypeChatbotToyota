# gateway_service.py
from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
from typing import Optional, Dict, Any
import logging

app = FastAPI(
    title="Infinity Gateway", 
    description="Gateway untuk routing requests ke layanan internal", 
    version="1.0"
)

logger = logging.getLogger(__name__)



def _to_optional_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    try:
        return str(value)
    except Exception:
        return None



def build_chat_envelope(context: Any, message: str) -> Dict[str, Optional[str]]:
    session_id: Optional[str] = None

    if isinstance(context, dict):
        session_candidate = context.get('session_id') or context.get('session-id')
        session_id = _to_optional_str(session_candidate)

    return {
        'session-id': session_id,
        'output': message,
    }


def normalize_chat_response(
    payload: Any,
    fallback: Dict[str, Optional[str]],
    default_output: str
) -> Dict[str, Optional[str]]:
    normalized: Dict[str, Optional[str]] = {
        'session-id': fallback.get('session-id'),
        'output': default_output,
    }

    if isinstance(payload, dict):
        session_candidate = _to_optional_str(payload.get('session_id') or payload.get('session-id'))
        if session_candidate:
            normalized['session-id'] = session_candidate

        output_candidate: Any = (
            payload.get('output')
            or payload.get('response')
            or payload.get('message')
        )

        if isinstance(output_candidate, list):
            first_entry = next(
                (item for item in output_candidate if isinstance(item, dict)),
                None,
            )
            if first_entry:
                output_candidate = (
                    first_entry.get('output')
                    or first_entry.get('response')
                    or first_entry.get('message')
                )
                if not normalized['session-id']:
                    normalized['session-id'] = _to_optional_str(
                        first_entry.get('session_id')
                        or first_entry.get('session-id')
                        or (first_entry.get('context') or {}).get('session_id')
                    )
            elif output_candidate:
                output_candidate = output_candidate[0]

        if isinstance(output_candidate, dict):
            output_candidate = (
                output_candidate.get('output')
                or output_candidate.get('response')
                or output_candidate.get('message')
            )

        context_payload = payload.get('context')
        if isinstance(context_payload, dict) and not normalized['session-id']:
            normalized['session-id'] = _to_optional_str(
                context_payload.get('session_id')
                or context_payload.get('session-id')
            )

        if isinstance(output_candidate, str):
            normalized['output'] = output_candidate
        elif output_candidate is not None:
            normalized['output'] = _to_optional_str(output_candidate) or default_output
        else:
            normalized['output'] = default_output

    elif payload is not None:
        normalized['output'] = _to_optional_str(payload) or default_output

    if not normalized['output'] or not normalized['output'].strip():
        normalized['output'] = default_output

    if normalized['session-id'] is None:
        normalized['session-id'] = fallback.get('session-id')

    return normalized


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base URLs for microservices
CAR_SERVICE_URL = "http://car_service:8007"

@app.get("/health", tags=["Gateway"])
def health_check():
    return {"status": "ok", "gateway": "Infinity Gateway"}

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

    fallback_envelope = build_chat_envelope({}, fallback_message)

    try:
        body = await request.json()
    except Exception as parse_error:
        error_message = str(parse_error) or parse_error.__class__.__name__
        logger.error("Failed to parse /api/chat request body: %s", error_message)
        return JSONResponse(status_code=400, content=fallback_envelope)

    context = {}
    if isinstance(body, dict):
        context = body.get("context")

    fallback_envelope = build_chat_envelope(context, fallback_message)

    car_service_payload: Any = None

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(f"{CAR_SERVICE_URL}/chat", json=body)
            response.raise_for_status()
            try:
                car_service_payload = response.json()
            except Exception as decode_error:
                error_message = str(decode_error) or decode_error.__class__.__name__
                logger.error(
                    "Failed to decode car service /chat response: %s",
                    error_message
                )
                return JSONResponse(status_code=502, content=fallback_envelope)
    except httpx.HTTPStatusError as http_error:
        upstream_status = http_error.response.status_code if http_error.response else 502
        error_message: Optional[str] = None
        if http_error.response:
            try:
                data = http_error.response.json()
                if isinstance(data, dict):
                    error_message = (
                        data.get("detail")
                        or data.get("output")
                        or data.get("response")
                        or data.get("error")
                    )
            except Exception:
                error_message = None

        error_message = error_message or str(http_error) or http_error.__class__.__name__
        logger.error(
            "Car service /chat returned HTTP %s: %s",
            upstream_status,
            error_message
        )
        return JSONResponse(
            status_code=upstream_status,
            content={**fallback_envelope, "output": fallback_message}
        )
    except Exception as call_error:
        error_message = str(call_error) or call_error.__class__.__name__
        logger.exception("Failed to call car service /chat")
        return JSONResponse(
            status_code=502,
            content={**fallback_envelope, "output": fallback_message}
        )

    normalized_payload = normalize_chat_response(
        car_service_payload,
        fallback_envelope,
        fallback_message
    )

    return JSONResponse(content=normalized_payload)
