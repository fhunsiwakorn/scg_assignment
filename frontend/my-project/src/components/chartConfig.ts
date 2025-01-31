import axios from 'axios';

// ข้อมูลเริ่มต้น
export const data = {
  labels: [],
  datasets: [
    {
      label: 'Temperature',
      backgroundColor: '#f87979',
      data: [],
    },
    {
      label: 'Humidity',
      backgroundColor: '#7acbff',
      data: [],
    },
    {
      label: 'Air Quality',
      backgroundColor: '#ffcc00',
      data: [],
    },
  ],
};

// ตัวเลือกสำหรับกราฟ
export const options = {
  responsive: true,
  maintainAspectRatio: false,
};


// ฟังก์ชันในการดึงข้อมูลจาก API
export const fetchData = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/sensor/processed');
    const sensorData = response.data;
  
    
    // กำหนด labels และ datasets
    data.labels = sensorData.map((item: { timestamp: any; }) => item.timestamp); // สมมติว่า timestamp เป็นฟิลด์ที่มีอยู่
    data.datasets[0].data = sensorData.map((item: { temperature: any; }) => item.temperature);
    data.datasets[1].data = sensorData.map((item: { humidity: any; }) => item.humidity);
    data.datasets[2].data = sensorData.map((item: { air_quality: any; }) => item.air_quality);
    console.log(JSON.stringify(data));
    
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};
// export const intervalFetchData = () =>  {
//     setInterval(() => {
//         fetchData();
//     }, 3000);
//   };
// // เรียกใช้ฟังก์ชันเมื่อเริ่มต้น
// intervalFetchData();
