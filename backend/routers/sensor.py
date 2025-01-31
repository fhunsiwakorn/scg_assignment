from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from schemas.schema_sensor import SchemaSensorIn,SchemaSensorOut,SchemaSensorOut2
from services import add_sensor_data,get_aggregated_data,get_cleaned_data
routes_sensor = APIRouter()

@routes_sensor.post("/data", response_model=SchemaSensorOut2)  # ระบุ response model
async def ingest_sensor_data(data: SchemaSensorIn, db: Session = Depends(get_db)):
    try:
        result = await add_sensor_data(data, db=db)
        return result 
    except Exception as e:
        # จัดการข้อผิดพลาดและส่งคืนข้อความที่เหมาะสม
        raise HTTPException(status_code=500, detail=str(e))

@routes_sensor.get("/aggregated", description="time_window : 10m ,1h,24h,All")
async def fetch_aggregated_data(time_window: str  = "All", db: Session = Depends(get_db)):
    try:
        result = get_aggregated_data(time_window,db)
        return result 
    except Exception as e:
        # จัดการข้อผิดพลาดและส่งคืนข้อความที่เหมาะสม
        raise HTTPException(status_code=500, detail=str(e))
    

@routes_sensor.get("/processed", response_model=List[SchemaSensorOut] ,description="time_window : 10m ,1h,24h,All")
async def fetch_cleaned_data(time_window: str = "All",db: Session = Depends(get_db)):
    """
    Fetch cleaned and anomaly-detected sensor data.
    """
    # cleaned_data = get_cleaned_data(db)
    # return cleaned_data
    try:
        result =   get_cleaned_data(time_window,db)
        return result 
    except Exception as e:
        # จัดการข้อผิดพลาดและส่งคืนข้อความที่เหมาะสม
        raise HTTPException(status_code=500, detail=str(e))