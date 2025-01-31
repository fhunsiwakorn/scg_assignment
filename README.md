# IoT Data Processing Assignment

## วัตถุประสงค์
พัฒนาบริการ backend ที่ประมวลผลข้อมูล IoT แบบ time-series และให้ API สำหรับเรียกดูข้อมูลเชิงลึกที่สรุปไว้
## พัฒนาโดย
ศิวกร บรรลือทรัพย์
## เทคโนโลยีที่ใช้
- **Backend**: FastAPI
- **Frontend**: Vue.js
- **Database**: MySQL
- **Containerization**: Docker & Docker Compose
## เข้าถึงแอปพลิเคชัน
- **Backend: http://localhost:8000
- **Frontend: http://localhost

## API Endpoints
- **POST /sensor/data: รับข้อมูลเซนเซอร์ (อุณหภูมิ, ความชื้น, คุณภาพอากาศ)
- **GET /sensor/processed: ดึงข้อมูลที่ทำความสะอาดและตรวจจับค่าผิดปกติ
- **GET /sensor/aggregated: ดึงสถิติที่สรุปไว้ (ค่าเฉลี่ย, ค่ามัธยฐาน, ค่าสูงสุด/ต่ำสุด)

## การทำความสะอาดข้อมูลและการตรวจจับค่าผิดปกติ
ในขั้นตอนการประมวลผลข้อมูล เราได้ทำการ:
- **ลบค่าซ้ำ
- **จัดการข้อมูลที่หายไป
- **ตรวจจับค่าผิดปกติโดยใช้ Z-score หรือ IQR เพื่อทำการติดธงค่าที่ผิดปกติ

## การติดตั้ง Dependencies
สำหรับการติดตั้ง dependencies ของ backend ให้รันคำสั่ง:
- **pip install -r backend/requirements.txt