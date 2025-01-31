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

## โครงสร้างโปรเจกต์
/assignment
├── backend
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── services.py
│   ├── routers
│   │   └── sensor.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend
│   ├── src
│   │   ├── App.vue
│   │   ├── components
│   │   │   └── SensorChart.vue
│   │   └── main.ts
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml
└── sensor_data.csv