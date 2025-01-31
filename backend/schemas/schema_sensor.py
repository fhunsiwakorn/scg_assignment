from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SchemaSensorIn(BaseModel):
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    air_quality: Optional[float] = None

    class Config:
        from_attributes  = True


class SchemaSensorOut(BaseModel):
    id: int
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    air_quality: Optional[float] = None
    timestamp: Optional[datetime] = None
    is_anomaly_zscore: bool
    is_anomaly_iqr: bool

    class Config:
        from_attributes  = True

class SchemaSensorOut2(BaseModel):
    id: int
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    air_quality: Optional[float] = None
    timestamp: Optional[datetime] = None
    class Config:
        from_attributes  = True
        

class AggregatedInsights(BaseModel):
    mean_temperature: float
    median_temperature: float
    min_temperature: float
    max_temperature: float
    mean_humidity: float
    median_humidity: float
    min_humidity: float
    max_humidity: float
    mean_air_quality: float
    median_air_quality: float
    min_air_quality: float
    max_air_quality: float