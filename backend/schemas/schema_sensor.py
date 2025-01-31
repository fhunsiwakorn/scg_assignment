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