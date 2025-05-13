# 🖥️ Process Monitoring App

A Python-based system process monitoring tool with a live dashboard, REST API, and full Docker support.

---

## 🚀 Features

- 🔍 Monitor system processes: PID, CPU%, memory%
- 🧠 Anomaly detection for CPU/MEM spikes
- 📊 Filter and sort results dynamically
- 🌐 JSON REST API via FastAPI
- 🖼️ Web UI built with Streamlit
- 🐳 Docker + Docker Compose support

---

## 📦 Tech Stack

- Python 3.10
- FastAPI + Uvicorn
- Streamlit
- Docker & Docker Compose
- psutil

---

## ⚙️ How to Run

### 🔧 Requirements

- [Docker](https://www.docker.com/)
- (Optional) Python 3.10 + `pip install -r requirements.txt` for local testing

### 🐳 Run with Docker Compose

```bash
docker-compose up --build
