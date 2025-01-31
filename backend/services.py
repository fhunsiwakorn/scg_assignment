from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from pydantic import BaseModel
from models import SensorData
from schemas.schema_sensor import SchemaSensorIn
from datetime import datetime, timedelta, timezone
from typing import List
import numpy as np
# import pytz
# Get current UTC time
now_utc = datetime.now(timezone.utc)

# Bangkok is UTC+7
bangkok_offset = timedelta(hours=7)
now_bangkok = now_utc.astimezone(timezone(bangkok_offset))


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


async def add_sensor_data(data: SchemaSensorIn, db: Session):
    _content = SensorData(
        temperature=data.temperature,
        humidity=data.humidity,
        air_quality=data.air_quality
    )
    # เพิ่มข้อมูลลงในฐานข้อมูล
    db.add(_content)
    db.commit()
    db.refresh(_content)
    return _content


def get_aggregated_data(time_window: str, db: Session):
    # กำหนดช่วงเวลา
    now = now_bangkok
    if time_window == "10m":
        start_time = now - timedelta(minutes=10)
    elif time_window == "1h":
        start_time = now - timedelta(hours=1)
    elif time_window == "24h":
        start_time = now - timedelta(hours=24)
    elif time_window == "All":
        start_time = now
    else:
        raise HTTPException(status_code=400, detail="Invalid time window")

    # Query ข้อมูลในช่วงเวลาที่กำหนด
    data = db.query(
        SensorData.temperature,
        SensorData.humidity,
        SensorData.air_quality
    ).filter(
        SensorData.temperature.is_not(None),
        SensorData.humidity.is_not(None),
        SensorData.air_quality.is_not(None),
        SensorData.temperature > 0,
        SensorData.humidity > 0,
        SensorData.air_quality > 0
    )
    if time_window != "All":
        data = data.filter(SensorData.timestamp >= start_time)
    data = data.all()
    # ตรวจสอบว่ามีข้อมูลหรือไม่
    if not data:
        # raise HTTPException(status_code=404, detail="No data found for the given time window")
        return {
            "mean_temperature": 0.0,
            "median_temperature": 0.0,
            "min_temperature": 0.0,
            "max_temperature": 0.0,
            "mean_humidity": 0.0,
            "median_humidity": 0.0,
            "min_humidity": 0.0,
            "max_humidity": 0.0,
            "mean_air_quality": 0.0,
            "median_air_quality": 0.0,
            "min_air_quality": 0.0,
            "max_air_quality": 0.0,
        }

    # แยกข้อมูลออกเป็นลิสต์โดยไม่รวมค่า None
    temperatures = [d.temperature for d in data if d.temperature is not None]
    humidities = [d.humidity for d in data if d.humidity is not None]
    air_qualities = [d.air_quality for d in data if d.air_quality is not None]

    # ตรวจสอบว่ามีข้อมูลหลังจากกรองหรือไม่
    if not temperatures or not humidities or not air_qualities:
        raise HTTPException(
            status_code=404, detail="Not enough data for calculations")

    # คำนวณค่ากลาง (median) โดยใช้ฟังก์ชันใน Python
    def median(values):
        sorted_values = sorted(values)
        n = len(sorted_values)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_values[mid - 1] + sorted_values[mid]) / 2
        else:
            return sorted_values[mid]

    # คำนวณค่า mean, min, max และ median
    aggregated_data = {
        "mean_temperature": sum(temperatures) / len(temperatures),
        "median_temperature": median(temperatures),
        "min_temperature": min(temperatures),
        "max_temperature": max(temperatures),
        "mean_humidity": sum(humidities) / len(humidities),
        "median_humidity": median(humidities),
        "min_humidity": min(humidities),
        "max_humidity": max(humidities),
        "mean_air_quality": sum(air_qualities) / len(air_qualities),
        "median_air_quality": median(air_qualities),
        "min_air_quality": min(air_qualities),
        "max_air_quality": max(air_qualities),
    }

    # คืนค่าผลลัพธ์
    return AggregatedInsights(**aggregated_data)


def get_cleaned_data(time_window, db: Session):
    # กำหนดช่วงเวลา
    now = now_bangkok
    if time_window == "10m":
        start_time = now - timedelta(minutes=10)
    elif time_window == "1h":
        start_time = now - timedelta(hours=1)
    elif time_window == "24h":
        start_time = now - timedelta(hours=24)
    elif time_window == "All":
        start_time = now
    else:
        raise HTTPException(status_code=400, detail="Invalid time window")

    try:
        raw_data = db.query(SensorData).filter(SensorData.temperature.is_not(None),
                                               SensorData.humidity.is_not(
                                                   None),
                                               SensorData.air_quality.is_not(
                                                   None),
                                               SensorData.temperature > 0,
                                               SensorData.humidity > 0,
                                               SensorData.air_quality > 0)
        if time_window != "All":
            raw_data = raw_data.filter(
                SensorData.timestamp >= start_time)
            
        raw_data = raw_data.all()
        if not raw_data:
            return []

        cleaned_data = clean_data(raw_data)

        # กรองค่า None และ 0 ออกจาก temperatures, humidities, และ air_qualities
        temperatures = [
            record.temperature for record in cleaned_data if record.temperature is not None and record.temperature != 0]
        humidities = [
            record.humidity for record in cleaned_data if record.humidity is not None and record.humidity != 0]
        air_qualities = [
            record.air_quality for record in cleaned_data if record.air_quality is not None and record.air_quality != 0]

        if not temperatures:
            raise HTTPException(
                status_code=400, detail="No valid temperature data available")
        if not humidities:
            raise HTTPException(
                status_code=400, detail="No valid humidity data available")
        if not air_qualities:
            raise HTTPException(
                status_code=400, detail="No valid air quality data available")

        outliers_zscore = detect_outliers_zscore(temperatures)
        outliers_iqr = detect_outliers_iqr(temperatures)

        # เพิ่มฟิลด์ "is_anomaly" เพื่อ flag ค่าผิดปกติ
        for record in cleaned_data:
            record.is_anomaly_zscore = record.temperature in outliers_zscore
            record.is_anomaly_iqr = record.temperature in outliers_iqr

        return cleaned_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def compare_value(value):
    if value is None or value == 0:
        return 0
    else:
        return value


def clean_data(data: List[SensorData]):
    # ฟังก์ชันทำความสะอาดข้อมูล
    unique_data = {record.id: record for record in data}.values()
    cleaned_data = [
        record for record in unique_data
        if compare_value(record.temperature) > 0 and compare_value(record.humidity) > 0 and compare_value(record.air_quality) > 0
    ]
    return cleaned_data


def detect_outliers_zscore(data: List[float], threshold: float = 3.0):
    if len(data) == 0:
        return []
    mean = np.mean(data)
    std_dev = np.std(data)
    outliers = [value for value in data if abs(
        (value - mean) / std_dev) > threshold]
    return outliers


def detect_outliers_iqr(data: List[float]):
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = [value for value in data if value <
                lower_bound or value > upper_bound]
    return outliers
