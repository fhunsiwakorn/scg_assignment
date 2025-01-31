# ใช้ Node.js เป็นฐาน
FROM node:14

# ตั้งค่าตำแหน่งทำงาน
WORKDIR /usr/src/app

# คัดลอก package.json และ package-lock.json
COPY package*.json ./

# ติดตั้ง dependencies
RUN npm install

# คัดลอกไฟล์ทั้งหมด
COPY . .

# สร้างแอปพลิเคชัน
RUN npm run build

# ใช้ Nginx เพื่อเสิร์ฟไฟล์ static
FROM nginx:alpine

# คัดลอกไฟล์จาก build ไปยัง Nginx
COPY --from=0 /usr/src/app/dist /usr/share/nginx/html

# เปิดพอร์ตที่ Nginx จะทำงาน
EXPOSE 80

# รัน Nginx
CMD ["nginx", "-g", "daemon off;"]