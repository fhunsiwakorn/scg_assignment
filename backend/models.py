from sqlalchemy import Column, Integer, Float, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class SensorData(Base):
    __tablename__ = 'sensor_data'
    id = Column(Integer, primary_key=True)
    temperature = Column(Float, default=0)
    humidity = Column(Float, default=0)
    air_quality =  Column(Float, default=0)
    timestamp = Column(DateTime , default=func.now())