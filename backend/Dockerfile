# ใช้ Python เป็นฐาน
FROM python:3.9

# ตั้งค่าตำแหน่งทำงาน
WORKDIR /usr/src/app

# คัดลอกไฟล์ requirements.txt
COPY requirements.txt ./

# ติดตั้ง dependencies
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์ทั้งหมด
COPY . .

# เปิดพอร์ตที่ FastAPI จะทำงาน
EXPOSE 8000

# รัน FastAPI ด้วย Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
