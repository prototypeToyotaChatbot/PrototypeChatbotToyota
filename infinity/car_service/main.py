from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Text, DateTime, func, Index, and_, JSON, DECIMAL, DATE, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
import os
import json
from typing import Optional, List, Dict, Any
from decimal import Decimal
import uvicorn
from contextlib import contextmanager
import logging
import uuid
from datetime import date, datetime
from pytz import timezone as pytz_timezone
from fastapi_mcp import FastApiMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration from environment variables
DATABASE_URL = os.getenv("DATABASE_URL_CAR", "postgresql://postgres:postgres@pgvector:5432/car_db")

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

mcp = FastApiMCP(app, name="Car Service MCP",
    description="MCP untuk layanan data mobil, rekomendasi, dan promosi.",
    include_operations=[
        "list cars", "list car variants", "get car recommendations", 
        "compare variants", "list promotions", "get stock info"
    ]
)
mcp.mount(mount_path="/mcp", transport="sse")
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

if __name__ == "__main__":
    # Create tables if they don't exist (for local development)
    # In production, you might use Alembic for migrations
    Base.metadata.create_all(bind=engine)
    uvicorn.run("main:app", host="0.0.0.0", port=8007, reload=True)
    mcp.setup_server()