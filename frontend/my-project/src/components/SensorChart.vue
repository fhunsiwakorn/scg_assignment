<template>
  <div class="chart-container">
    <div align="center">
      <h1>IoT Data Processing Assignment</h1>
    </div>
    <div align="right">
      <select v-model="selectedTimeWindow" @change="updateData" style="width: 100px;height: 45px;">
      <option value="All">All</option>  
      <option value="10m">10 minutes</option>  
      <option value="1h">1 hour</option>  
      <option value="24h">24 hours</option> 
    </select>
    </div>


    <Line v-if="data.labels.length > 0" :data="data" :options="options" />

       <!-- Progress Bar -->
    <div v-if="loading" class="progress-bar">
      <div class="progress-bar-fill"></div>
    </div>

    <table v-if="averageData" class="average-table">
      <thead>
        <tr>
          <th>Type</th>
          <th>Mean</th>
          <th>Median</th>
          <th>Minimum</th>
          <th>Maximum</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Temperature</td>
          <td>{{ averageData.mean_temperature.toFixed(2) }}</td>
          <td>{{ averageData.median_temperature.toFixed(2) }}</td>
          <td>{{ averageData.min_temperature.toFixed(2) }}</td>
          <td>{{ averageData.max_temperature.toFixed(2) }}</td>
        </tr>
        <tr>
          <td>Humidity</td>
          <td>{{ averageData.mean_humidity.toFixed(2) }}</td>
          <td>{{ averageData.median_humidity.toFixed(2) }}</td>
          <td>{{ averageData.min_humidity.toFixed(2) }}</td>
          <td>{{ averageData.max_humidity.toFixed(2) }}</td>
        </tr>
        <tr>
          <td>Air Quality</td>
          <td>{{ averageData.mean_air_quality.toFixed(2) }}</td>
          <td>{{ averageData.median_air_quality.toFixed(2) }}</td>
          <td>{{ averageData.min_air_quality.toFixed(2) }}</td>
          <td>{{ averageData.max_air_quality.toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "vue-chartjs";
import * as chartConfig from "./chartConfig.js";
import axios from "axios";
const apiUrl = "http://127.0.0.1:8000";
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default {
  name: "App",
  components: {
    Line,
  },
  data() {
    return {
      ...chartConfig,
      intervalId: 0,
      averageData: null,
      selectedTimeWindow: "All",
      loading: false, // ตัวแปรสำหรับควบคุมการแสดง progress bar
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            title: {
              display: true,
              text: "Timestamp",
            },
          },
          y: {
            title: {
              display: true,
              text: "Values",
            },
          },
        },
        plugins: {
          legend: {
            display: true,
            position: "top",
          },
          tooltip: {
            enabled: true,
          },
        },
      },
    };
  },
  mounted() {
    this.loading = true; // เริ่มแสดง progress bar
    this.fetchData2();
    this.fetchAverageData();
    this.intervalId = setInterval(() => {
      this.fetchData2();
      this.fetchAverageData();
    }, 10000);
  },
  beforeDestroy() {
    clearInterval(this.intervalId);
  },
  methods: {
    async updateData() {
      this.loading = true; // เริ่มแสดง progress bar
      await this.fetchAverageData();
      await this.fetchData2();
      this.loading = false; // ซ่อน progress bar
    },

    async fetchData2() {
      try {
        const response = await axios.get(
          `${apiUrl}/sensor/processed?time_window=${this.selectedTimeWindow}`
        );
        const sensorData = response.data;
        // console.log(JSON.stringify(sensorData));

        // Update chart data
        this.data.labels = sensorData.map(
          (item) => item.timestamp
        );
        this.data.datasets[0].data = sensorData.map(
          (item) => item.temperature
        );
        this.data.datasets[1].data = sensorData.map(
          (item) => item.humidity
        );
        this.data.datasets[2].data = sensorData.map(
          (item) => item.air_quality
        );
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        this.loading = false; // ซ่อน progress bar
      }
    },

    async fetchAverageData() {
      try {
        const response = await axios.get(
          `${apiUrl}/sensor/aggregated?time_window=${this.selectedTimeWindow}`
        );
        this.averageData = response.data;
      } catch (error) {
        console.error("Error fetching average data:", error);
      } finally {
        this.loading = false; // ซ่อน progress bar
      }
    },
  },
};
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  height: 60vh;
}

.average-table {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
}

.average-table th,
.average-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

.average-table th {
  background-color: #f2f2f2;
}

.progress-bar {
  width: 100%;
  height: 5px;
  background-color: #f3f3f3;
  border-radius: 5px;
  overflow: hidden;
  margin-top: 10px;
}

.progress-bar-fill {
  height: 100%;
  width: 100%; /* เปลี่ยนเป็น 0% เพื่อแสดงความก้าวหน้า */
  background-color: #4caf50; /* สีของ progress bar */
  animation: loading 2s infinite; /* เพิ่ม animation */
}

@keyframes loading {
  0% { width: 0%; }
  50% { width: 50%; }
  100% { width: 100%; }
}
</style>
