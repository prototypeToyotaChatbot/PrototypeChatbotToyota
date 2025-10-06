from fastapi import FastAPI, HTTPException, Query, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Text, DateTime, func, Index, and_, JSON, DECIMAL, DATE, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
import os
import json
from typing import Optional, List, Dict, Any, Tuple
from decimal import Decimal
import uvicorn
from contextlib import contextmanager
import logging
import uuid
from datetime import date, datetime
from pytz import timezone as pytz_timezone
from fastapi_mcp import FastApiMCP
import httpx
import asyncio
from copy import deepcopy
from urllib.parse import urlencode

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration from environment variables
DATABASE_URL = os.getenv("DATABASE_URL_CAR", "postgresql://postgres:postgres@pgvector:5432/car_db")

# Chatbot Configuration
CHATBOT_CONFIG = {
    "n8n_webhook_url": os.getenv("N8N_CHATBOT_WEBHOOK_URL", ""),  # URL webhook N8N untuk chatbot
    "use_ai_processing": os.getenv("USE_AI_PROCESSING", "false").lower() == "true",
    "welcome_message": os.getenv("WELCOME_MESSAGE", 
        "Hello! I'm your car consultant assistant. I can help you find the perfect car, compare models, check promotions, and more. What can I help you with today?"),
    "fallback_message": os.getenv("FALLBACK_MESSAGE",
        "I'd be happy to help you with car-related questions! I can assist with finding cars, checking promotions, comparing models, and providing recommendations based on your needs."),
    "error_message": os.getenv("ERROR_MESSAGE",
        "I'm sorry, I'm experiencing some technical difficulties right now. Please try again or contact our sales team directly."),
    "webhook_timeout": int(os.getenv("WEBHOOK_TIMEOUT", "30"))  # timeout dalam detik
}

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# =================================================================
# SQLALCHEMY MODELS
# =================================================================

class Car(Base):
    __tablename__ = "cars"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_name = Column(String(100), nullable=False, unique=True)
    segment = Column(String(50))
    variants = relationship("CarVariant", back_populates="car")

class CarVariant(Base):
    __tablename__ = "car_variants"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    car_id = Column(UUID(as_uuid=True), ForeignKey("cars.id"))
    variant_name = Column(String(150), nullable=False)
    price = Column(DECIMAL(15, 2), nullable=False)
    image_url = Column(Text)
    engine_spec = Column(String(255))
    transmission = Column(String(50))
    seating_capacity = Column(Integer)
    fuel_type = Column(String(50))
    target_demographic = Column(String(50))
    use_case = Column(Text)
    benefits_summary = Column(Text)
    circumstances_summary = Column(Text)
    top_features = Column(JSON)
    
    car = relationship("Car", back_populates="variants")
    promotions = relationship("Promotion", back_populates="variant")
    stock = relationship("StockInventory", back_populates="variant")
    accessories = relationship("Accessory", secondary="variant_accessories", back_populates="variants")

class Accessory(Base):
    __tablename__ = "accessories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(12, 2), nullable=False)
    
    variants = relationship("CarVariant", secondary="variant_accessories", back_populates="accessories")

class VariantAccessory(Base):
    __tablename__ = "variant_accessories"
    variant_id = Column(UUID(as_uuid=True), ForeignKey("car_variants.id"), primary_key=True)
    accessory_id = Column(UUID(as_uuid=True), ForeignKey("accessories.id"), primary_key=True)

class Promotion(Base):
    __tablename__ = "promotions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    variant_id = Column(UUID(as_uuid=True), ForeignKey("car_variants.id"))
    promo_title = Column(String(255), nullable=False)
    discount_amount = Column(DECIMAL(15, 2))
    discount_percentage = Column(DECIMAL(5, 2))
    start_date = Column(DATE, nullable=False)
    end_date = Column(DATE, nullable=False)
    terms_conditions = Column(Text)
    
    variant = relationship("CarVariant", back_populates="promotions")

class StockInventory(Base):
    __tablename__ = "stock_inventory"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    variant_id = Column(UUID(as_uuid=True), ForeignKey("car_variants.id"))
    city = Column(String(100), nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    indent_estimate_weeks = Column(Integer)
    
    variant = relationship("CarVariant", back_populates="stock")

class Workshop(Base):
    __tablename__ = "workshops"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(Text)
    specialization = Column(Text)

class Community(Base):
    __tablename__ = "communities"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    base_city = Column(String(100), nullable=False)
    focus_model = Column(String(100))
    contact_person = Column(String(100))

class DressCode(Base):
    __tablename__ = "dress_codes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(100), nullable=False)
    day_of_week = Column(String(20), nullable=False)
    attire_description = Column(Text, nullable=False)

# =================================================================
# PYDANTIC SCHEMAS
# =================================================================

class CarSchema(BaseModel):
    id: uuid.UUID
    model_name: str
    segment: Optional[str]
    variant_count: int

    class Config:
        from_attributes = True

class AccessorySchema(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    price: Decimal

    class Config:
        from_attributes = True

class CarVariantSchema(BaseModel):
    id: uuid.UUID
    car_id: uuid.UUID
    variant_name: str
    price: Decimal
    image_url: Optional[str]
    engine_spec: Optional[str]
    transmission: Optional[str]
    seating_capacity: Optional[int]
    fuel_type: Optional[str]
    target_demographic: Optional[str]
    use_case: Optional[str]
    benefits_summary: Optional[str]
    circumstances_summary: Optional[str]
    top_features: Optional[Dict[str, Any]]
    model_name: str

    class Config:
        from_attributes = True

class CarVariantDetailSchema(CarVariantSchema):
    segment: str

class PromotionSchema(BaseModel):
    id: uuid.UUID
    variant_id: uuid.UUID
    promo_title: str
    discount_amount: Optional[Decimal]
    discount_percentage: Optional[Decimal]
    start_date: date
    end_date: date
    terms_conditions: Optional[str]
    variant_name: str
    model_name: str
    original_price: Decimal
    discounted_price: Decimal

    class Config:
        from_attributes = True

class StockInventorySchema(BaseModel):
    id: uuid.UUID
    variant_id: uuid.UUID
    city: str
    stock_quantity: int
    indent_estimate_weeks: Optional[int]
    variant_name: str
    model_name: str

    class Config:
        from_attributes = True

class WorkshopSchema(BaseModel):
    id: uuid.UUID
    name: str
    city: str
    address: Optional[str]
    specialization: Optional[str]

    class Config:
        from_attributes = True

class CommunitySchema(BaseModel):
    id: uuid.UUID
    name: str
    base_city: str
    focus_model: Optional[str]
    contact_person: Optional[str]

    class Config:
        from_attributes = True

class DressCodeSchema(BaseModel):
    id: int
    role: str
    day_of_week: str
    attire_description: str

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    session_id: str = Field(alias="session-id", validation_alias="session-id", serialization_alias="session-id")
    output: str

    model_config = ConfigDict(populate_by_name=True)


def prepare_chat_context(raw_context: Optional[Dict[str, Any]]) -> Tuple[Dict[str, Any], str]:
    """Normalize incoming chat context and guarantee a session identifier."""
    base_context = deepcopy(raw_context) if isinstance(raw_context, dict) else {}
    session_id = (
        base_context.get("session_id")
        or base_context.get("session-id")
        or f"session-{uuid.uuid4()}"
    )
    base_context.pop("user_id", None)
    base_context.setdefault("session_id", session_id)
    return base_context, session_id


# =================================================================
# APP & MIDDLEWARE
# =================================================================

app = FastAPI(
    title="Car Service API",
    description="API untuk manajemen data mobil, varian, aksesoris, dan rekomendasi",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

jakarta_tz = pytz_timezone('Asia/Jakarta')

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    logger.info("Car service starting up...")
    # The database engine is created on module load.
    # No need to initialize a separate pool.
    try:
        for route in app.routes:
            methods = getattr(route, "methods", None)
            path = getattr(route, "path", getattr(route, "path_format", ""))
            logger.info(f"Route registered: path={path} methods={methods}")
    except Exception as e:
        logger.warning(f"Failed to enumerate routes: {e}")

@app.get("/debug/routes")
async def list_routes():
    routes = []
    for route in app.routes:
        routes.append({
            "path": getattr(route, "path", getattr(route, "path_format", "")),
            "methods": list(getattr(route, "methods", [])),
            "name": getattr(route, "name", None)
        })
    return {"routes": routes}

@app.post("/mcp")
async def mcp_post_bridge(request: Request) -> Response:
    """
    Bridge endpoint to support POST /mcp by forwarding to MCP message endpoint.
    Some MCP clients POST to the base mount path. This forwards the request
    to the underlying message endpoint so those clients continue to work.
    """
    try:
        raw_body = await request.body()
        headers = {
            "content-type": request.headers.get("content-type", "application/json")
        }
        query_params = dict(request.query_params)

        def normalize_session(value: Optional[str]) -> Optional[str]:
            if not value:
                return None
            try:
                return uuid.UUID(str(value)).hex
            except Exception:
                return None

        session_id = normalize_session(query_params.get("session_id"))

        try:
            decoded_body = raw_body.decode("utf-8") if raw_body else ""
            payload = json.loads(decoded_body) if decoded_body else {}

            if not isinstance(payload, dict):
                logger.debug("MCP POST payload is not a JSON object; wrapping into dict")
                payload = {"messages": payload}

            body_session = (
                payload.get("session_id")
                or payload.get("sessionId")
                or payload.get("session")
            )

            if not session_id and body_session:
                session_id = normalize_session(body_session)

            if not session_id:
                session_id = uuid.uuid4().hex
                logger.info(
                    "POST /mcp missing session identifier. Generated new session: %s",
                    session_id,
                )

            payload["session_id"] = session_id
            payload["sessionId"] = session_id
            raw_body = json.dumps(payload).encode("utf-8")
        except Exception as parse_error:
            logger.warning(
                f"Failed to process MCP POST body for session normalization: {parse_error}"
            )
            if not session_id:
                session_id = uuid.uuid4().hex
                logger.info(
                    "POST /mcp had unreadable body. Injecting default session %s",
                    session_id,
                )
            fallback_payload = {"session_id": session_id, "sessionId": session_id, "messages": []}
            raw_body = json.dumps(fallback_payload).encode("utf-8")

        query_params["session_id"] = session_id
        target_url = "http://localhost:8007/mcp/messages/"
        if query_params:
            target_url = f"{target_url}?{urlencode(query_params)}"

        logger.info(f"Bridging POST /mcp request to {target_url}")

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(target_url, content=raw_body, headers=headers)

        # Return the response from the message endpoint directly to the original caller (N8N)
        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=dict(resp.headers),
        )

    except Exception as e:
        logger.error(f"Failed to bridge POST /mcp request: {e}")
        return Response(
            content=json.dumps({"error": "mcp_bridge_failed"}),
            status_code=502,
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "car_service"}

# =================================================================
# CARS & VARIANTS ENDPOINTS
# =================================================================

@app.get("/cars", response_model=Dict[str, Any], operation_id="list cars")
async def get_all_cars(db: Session = Depends(get_db)):
    """Mendapatkan semua model mobil"""
    try:
        cars_with_counts = db.query(
            Car.id,
            Car.model_name,
            Car.segment,
            func.count(CarVariant.id).label("variant_count")
        ).outerjoin(CarVariant, Car.id == CarVariant.car_id)\
         .group_by(Car.id)\
         .order_by(Car.model_name)\
         .all()
        
        return {
            "status": "success",
            "data": [CarSchema.model_validate(c) for c in cars_with_counts]
        }
    except Exception as e:
        logger.error(f"Error getting cars: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cars/{car_id}/variants", response_model=Dict[str, Any], operation_id="list car variants")
async def get_car_variants(car_id: uuid.UUID, db: Session = Depends(get_db)):
    """Mendapatkan semua varian dari model mobil tertentu"""
    try:
        variants = db.query(CarVariant)\
            .join(Car)\
            .filter(CarVariant.car_id == car_id)\
            .order_by(CarVariant.price)\
            .all()
        
        # Manually add model_name to each variant object for schema validation
        result = []
        for v in variants:
            v.model_name = v.car.model_name
            result.append(CarVariantSchema.model_validate(v))

        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        logger.error(f"Error getting car variants: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/variants/{variant_id}", response_model=Dict[str, Any])
async def get_variant_detail(variant_id: uuid.UUID, db: Session = Depends(get_db)):
    """Mendapatkan detail lengkap varian mobil"""
    try:
        variant = db.query(CarVariant).filter(CarVariant.id == variant_id).first()
        
        if not variant:
            raise HTTPException(status_code=404, detail="Variant not found")
        
        # Manually add model_name and segment for schema validation
        variant.model_name = variant.car.model_name
        variant.segment = variant.car.segment
        
        return {
            "status": "success",
            "data": CarVariantDetailSchema.model_validate(variant)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting variant detail: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =================================================================
# RECOMMENDATION ENDPOINTS
# =================================================================

@app.get("/recommendations", response_model=Dict[str, Any], operation_id="get car recommendations")
async def get_car_recommendations(
    budget_min: Optional[float] = Query(None, description="Budget minimum"),
    budget_max: Optional[float] = Query(None, description="Budget maximum"),
    use_case: Optional[str] = Query(None, description="Kegunaan mobil (daily, travel, business, off-road)"),
    target_demographic: Optional[str] = Query(None, description="Target demografi (Gen Z, Millennial, Family, Executive)"),
    seating_capacity: Optional[int] = Query(None, description="Kapasitas tempat duduk minimum"),
    fuel_type: Optional[str] = Query(None, description="Jenis bahan bakar"),
    transmission: Optional[str] = Query(None, description="Jenis transmisi"),
    db: Session = Depends(get_db)
):
    """Mendapatkan rekomendasi mobil berdasarkan kriteria"""
    try:
        query = db.query(CarVariant).join(Car)
        
        if budget_min is not None:
            query = query.filter(CarVariant.price >= Decimal(budget_min))
        
        if budget_max is not None:
            query = query.filter(CarVariant.price <= Decimal(budget_max))
        
        if use_case:
            query = query.filter(CarVariant.use_case.ilike(f"%{use_case}%"))
        
        if target_demographic:
            query = query.filter(CarVariant.target_demographic.ilike(f"%{target_demographic}%"))
        
        if seating_capacity:
            query = query.filter(CarVariant.seating_capacity >= seating_capacity)
        
        if fuel_type:
            query = query.filter(CarVariant.fuel_type.ilike(f"%{fuel_type}%"))
        
        if transmission:
            query = query.filter(CarVariant.transmission.ilike(f"%{transmission}%"))
        
        recommendations = query.order_by(CarVariant.price).limit(10).all()
        
        result = []
        for r in recommendations:
            r.model_name = r.car.model_name
            r.segment = r.car.segment
            result.append(CarVariantDetailSchema.model_validate(r))
        
        return {
            "status": "success",
            "data": result,
            "total": len(result)
        }
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =================================================================
# COMPARISON ENDPOINTS
# =================================================================

@app.get("/compare", response_model=Dict[str, Any], operation_id="compare variants")
async def compare_variants(
    variant_ids: str = Query(..., description="Comma-separated variant IDs"),
    db: Session = Depends(get_db)
):
    """Membandingkan beberapa varian mobil"""
    try:
        try:
            variant_id_list = [uuid.UUID(id.strip()) for id in variant_ids.split(',')]
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid UUID format in variant_ids")

        if len(variant_id_list) > 4:
            raise HTTPException(status_code=400, detail="Maximum 4 variants can be compared")
        
        variants = db.query(CarVariant)\
            .filter(CarVariant.id.in_(variant_id_list))\
            .order_by(CarVariant.price)\
            .all()
        
        if len(variants) != len(variant_id_list):
            found_ids = {v.id for v in variants}
            missing_ids = [str(vid) for vid in variant_id_list if vid not in found_ids]
            raise HTTPException(status_code=404, detail=f"Variants not found: {', '.join(missing_ids)}")
        
        result = []
        for v in variants:
            v.model_name = v.car.model_name
            v.segment = v.car.segment
            result.append(CarVariantDetailSchema.model_validate(v))
        
        return {
            "status": "success",
            "data": result
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error comparing variants: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =================================================================
# ACCESSORIES ENDPOINTS
# =================================================================

@app.get("/variants/{variant_id}/accessories", response_model=Dict[str, Any])
async def get_variant_accessories(variant_id: uuid.UUID, db: Session = Depends(get_db)):
    """Mendapatkan aksesoris yang tersedia untuk varian tertentu"""
    try:
        variant = db.query(CarVariant).filter(CarVariant.id == variant_id).first()
        if not variant:
            raise HTTPException(status_code=404, detail="Variant not found")
            
        accessories = variant.accessories
        
        return {
            "status": "success",
            "data": [AccessorySchema.model_validate(acc) for acc in accessories]
        }
    except Exception as e:
        logger.error(f"Error getting variant accessories: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/accessories", response_model=Dict[str, Any])
async def get_all_accessories(db: Session = Depends(get_db)):
    """Mendapatkan semua aksesoris"""
    try:
        accessories = db.query(Accessory).order_by(Accessory.name).all()
        return {
            "status": "success",
            "data": [AccessorySchema.model_validate(acc) for acc in accessories]
        }
    except Exception as e:
        logger.error(f"Error getting accessories: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =================================================================
# PROMOTIONS ENDPOINTS
# =================================================================

@app.get("/promotions", response_model=Dict[str, Any], operation_id="list promotions")
async def get_active_promotions(db: Session = Depends(get_db)):
    """Mendapatkan semua promosi yang aktif"""
    try:
        today = date.today()
        promotions = db.query(Promotion)\
            .join(CarVariant)\
            .filter(Promotion.start_date <= today, Promotion.end_date >= today)\
            .all()

        result = []
        for p in promotions:
            original_price = p.variant.price
            if p.discount_percentage and p.discount_percentage > 0:
                discounted_price = original_price * (Decimal(1) - p.discount_percentage / Decimal(100))
            elif p.discount_amount and p.discount_amount > 0:
                discounted_price = original_price - p.discount_amount
            else:
                discounted_price = original_price

            promo_data = {
                **p.__dict__,
                "variant_name": p.variant.variant_name,
                "model_name": p.variant.car.model_name,
                "original_price": original_price,
                "discounted_price": discounted_price.quantize(Decimal('0.01'))
            }
            result.append(PromotionSchema.model_validate(promo_data))
        
        # Sort by discount percentage equivalent
        result.sort(key=lambda p: (p.original_price - p.discounted_price) / p.original_price, reverse=True)

        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        logger.error(f"Error getting promotions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =================================================================
# STOCK & INVENTORY ENDPOINTS
# =================================================================

@app.get("/stock", response_model=Dict[str, Any], operation_id="get stock info")
async def get_stock_info(
    city: Optional[str] = Query(None, description="Nama kota"),
    variant_id: Optional[uuid.UUID] = Query(None, description="ID varian"),
    db: Session = Depends(get_db)
):
    """Mendapatkan informasi stok dan inden"""
    try:
        query = db.query(StockInventory).join(CarVariant).join(Car)
        
        if city:
            query = query.filter(StockInventory.city.ilike(f"%{city}%"))
        
        if variant_id:
            query = query.filter(StockInventory.variant_id == variant_id)
            
        stock_info = query.order_by(StockInventory.city, Car.model_name, CarVariant.variant_name).all()
        
        result = []
        for s in stock_info:
            stock_data = {
                **s.__dict__,
                "variant_name": s.variant.variant_name,
                "model_name": s.variant.car.model_name
            }
            result.append(StockInventorySchema.model_validate(stock_data))

        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        logger.error(f"Error getting stock info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =================================================================
# SUPPORT ENDPOINTS
# =================================================================

@app.get("/workshops", response_model=Dict[str, Any])
async def get_workshops(
    city: Optional[str] = Query(None, description="Nama kota"),
    db: Session = Depends(get_db)
):
    """Mendapatkan daftar bengkel modifikasi"""
    try:
        query = db.query(Workshop)
        if city:
            query = query.filter(Workshop.city.ilike(f"%{city}%"))
        
        workshops = query.order_by(Workshop.city, Workshop.name).all()
        
        return {
            "status": "success",
            "data": [WorkshopSchema.model_validate(w) for w in workshops]
        }
    except Exception as e:
        logger.error(f"Error getting workshops: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/communities", response_model=Dict[str, Any])
async def get_communities(
    city: Optional[str] = Query(None, description="Nama kota"),
    db: Session = Depends(get_db)
):
    """Mendapatkan daftar komunitas mobil"""
    try:
        query = db.query(Community)
        if city:
            query = query.filter(Community.base_city.ilike(f"%{city}%"))
            
        communities = query.order_by(Community.base_city, Community.name).all()
        
        return {
            "status": "success",
            "data": [CommunitySchema.model_validate(c) for c in communities]
        }
    except Exception as e:
        logger.error(f"Error getting communities: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dress-codes", response_model=Dict[str, Any])
async def get_dress_codes(db: Session = Depends(get_db)):
    """Mendapatkan panduan dress code untuk staf"""
    try:
        dress_codes = db.query(DressCode).order_by(DressCode.role, DressCode.day_of_week).all()
        return {
            "status": "success",
            "data": [DressCodeSchema.model_validate(dc) for dc in dress_codes]
        }
    except Exception as e:
        logger.error(f"Error getting dress codes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def call_n8n_webhook(message: str, context: dict = None) -> dict:
    """Memanggil N8N webhook untuk AI processing"""
    try:
        webhook_url = CHATBOT_CONFIG["n8n_webhook_url"]
        if not webhook_url:
            logger.warning("N8N webhook URL tidak dikonfigurasi")
            return None

        context_data = deepcopy(context) if context else {}
        session_id = (
            context_data.get("session_id")
            or context_data.get("session-id")
            or f"session-{uuid.uuid4()}"
        )
        context_data.pop("user_id", None)
        context_data.setdefault("session_id", session_id)

        payload = {
            "message": message,
            "context": context_data,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }

        timeout = CHATBOT_CONFIG["webhook_timeout"]
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(webhook_url, json=payload)
            response.raise_for_status()

            result = response.json()
            if not isinstance(result, dict):
                result = {"output": result}

            output_candidate = (
                result.get("output")
                or result.get("response")
                or result.get("message")
            )
            result_session_id = (
                result.get("session_id")
                or result.get("session-id")
            )

            if isinstance(output_candidate, list):
                first_entry = next(
                    (item for item in output_candidate if isinstance(item, dict)),
                    None,
                )
                if first_entry:
                    output_candidate = (
                        first_entry.get("output")
                        or first_entry.get("response")
                        or first_entry.get("message")
                    )
                    if not result_session_id:
                        result_session_id = (
                            first_entry.get("session_id")
                            or first_entry.get("session-id")
                            or (first_entry.get("context") or {}).get("session_id")
                        )
                elif output_candidate:
                    output_candidate = output_candidate[0]

            if isinstance(output_candidate, dict):
                output_candidate = (
                    output_candidate.get("output")
                    or output_candidate.get("response")
                    or output_candidate.get("message")
                    or json.dumps(output_candidate)
                )

            context_payload = result.get("context")
            if isinstance(context_payload, dict) and not result_session_id:
                result_session_id = context_payload.get("session_id") or context_payload.get("session-id")

            if not isinstance(output_candidate, str):
                try:
                    output_candidate = json.dumps(output_candidate)
                except (TypeError, ValueError):
                    output_candidate = str(output_candidate)

            result_payload = {
                "output": output_candidate or CHATBOT_CONFIG["fallback_message"],
                "session_id": result_session_id or session_id,
            }
            logger.info(f"N8N webhook response: {result_payload}")
            return result_payload

    except httpx.TimeoutException:
        logger.error(f"N8N webhook timeout after {timeout}s")
        return None
    except Exception as e:
        logger.error(f"Error calling N8N webhook: {e}")
        return None


def get_welcome_response(session_id: str) -> ChatResponse:
    """Mendapatkan respons selamat datang"""
    return ChatResponse(
        session_id=session_id,
        output=CHATBOT_CONFIG["welcome_message"]
    )

async def get_fallback_response(message: str, db: Session, session_id: str) -> ChatResponse:
    """Mendapatkan respons fallback dengan informasi dasar"""
    try:
        # Berikan beberapa informasi berguna berdasarkan kata kunci
        message_lower = message.lower()

        if any(word in message_lower for word in ["car", "mobil", "model", "available"]):
            cars = db.query(Car).limit(5).all()
            car_list = [f"- {car.model_name} ({car.segment})" for car in cars]
            response_text = f"Here are some of our popular car models:\n\n" + "\n".join(car_list)
        elif any(word in message_lower for word in ["promo", "promotion", "discount"]):
            promotions = db.query(Promotion).filter(
                Promotion.end_date >= func.current_date()
            ).limit(3).all()
            if promotions:
                response_text = f"We have {len(promotions)} active promotions! Would you like to see the details?"
            else:
                response_text = "We always offer competitive prices! Let me know what car you're looking for."
        else:
            response_text = CHATBOT_CONFIG["fallback_message"]

        return ChatResponse(
            session_id=session_id,
            output=response_text
        )
    except Exception as e:
        logger.error(f"Error in fallback response: {e}")
        return ChatResponse(
            session_id=session_id,
            output=CHATBOT_CONFIG["error_message"]
        )


@app.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(request: ChatRequest, db: Session = Depends(get_db)):
    """Chat dengan assistant untuk konsultasi mobil"""
    session_id: str = f"session-{uuid.uuid4()}"
    try:
        message = request.message.strip()
        context_data, session_id = prepare_chat_context(request.context)

        if any(word in message.lower() for word in ["hello", "hi", "halo", "hai", "start"]):
            return get_welcome_response(session_id)

        if CHATBOT_CONFIG["use_ai_processing"] and CHATBOT_CONFIG["n8n_webhook_url"]:
            logger.info(f"Sending message to N8N webhook: {message}")
            ai_response = await call_n8n_webhook(message, context_data)

            if ai_response:
                response_session_id = ai_response.get("session_id") or session_id
                output_text = (
                    ai_response.get("output")
                    or ai_response.get("response")
                    or ai_response.get("message")
                    or CHATBOT_CONFIG["fallback_message"]
                )
                return ChatResponse(
                    session_id=response_session_id,
                    output=output_text
                )

            logger.warning("N8N webhook failed, using fallback response")
            return await get_fallback_response(message, db, session_id)

        logger.info(f"AI processing disabled or webhook missing, using fallback for: {message}")
        return await get_fallback_response(message, db, session_id)

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return ChatResponse(
            session_id=session_id,
            output=CHATBOT_CONFIG["error_message"],
        )


mcp = FastApiMCP(app, name="Car Service MCP",
    description="MCP untuk layanan data mobil, rekomendasi, dan promosi.",
    include_operations=[
        "list cars", "list car variants", "get car recommendations",
        "compare variants", "list promotions", "get stock info"
    ]
)
mcp.mount(mount_path="/mcp", transport="sse")

if __name__ == "__main__":
    # Create tables if they don't exist (for local development)
    # In production, you might use Alembic for migrations
    Base.metadata.create_all(bind=engine)
    # Ensure MCP routes are registered before serving
    mcp.setup_server()
    # Running without reloader for Docker healthcheck stability
    uvicorn.run(app, host="0.0.0.0", port=8007)

