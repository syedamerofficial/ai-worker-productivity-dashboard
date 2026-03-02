# AI Worker Productivity Dashboard

## 🚀 Overview

This project simulates an AI-powered factory monitoring system where computer vision events from CCTV cameras are ingested, stored, and converted into actionable productivity metrics.

The system demonstrates an end-to-end ML Ops style pipeline:

Edge (CV events) → Backend API → Database → Metrics Engine → Dashboard

---

## 🏗 Architecture

AI Cameras → FastAPI Backend → SQLite → Metrics Engine → React Dashboard

### Components

- FastAPI backend — event ingestion and metrics APIs  
- SQLite database — persistent storage  
- Metrics engine — computes worker productivity  
- React frontend — visualization dashboard  
- Docker — containerized backend  
- Render + Vercel — cloud deployment  

---

## 📊 Database Schema

### Workers

- worker_id (PK)  
- name  

### Workstations

- station_id (PK)  
- name  

### Events

- id (PK, deduplicated via hash)  
- timestamp  
- worker_id  
- workstation_id  
- event_type  
- confidence  
- count  

---

## 📈 Metric Definitions

### Worker Level

- Active Time — duration between working events  
- Idle Time — duration between idle events  
- Utilization % — active / (active + idle)  
- Units Produced — sum of product_count events  
- Units/hour — units normalized by active time  

---

## ⚙️ Assumptions

- Events are time-ordered per worker  
- Missing future event closes previous state  
- product_count is independent of time windows  
- SQLite used for simplicity (can be replaced with Postgres)  

---

## 🛡 Handling Edge Cases

### Intermittent Connectivity

- Events are idempotent via hashed event IDs  
- Duplicate ingestion safely ignored  

### Duplicate Events

- MD5 hash generated from event payload  
- Primary key constraint prevents duplicates  

### Out-of-Order Events

- Metrics computed after ordering by timestamp  
- Ensures deterministic calculations  

---

## 🤖 Model Versioning (Proposed)

In production:

- Add model_version column to events  
- Store model metadata in separate table  
- Enable A/B comparison across versions  

---

## 📉 Model Drift Detection (Proposed)

Would implement:

- distribution monitoring of event frequencies  
- confidence score tracking  
- statistical drift tests (KS test / PSI)  
- alerting via monitoring pipeline  

---

## 🔁 Retraining Strategy (Proposed)

Trigger retraining when:

- drift threshold exceeded  
- sustained accuracy drop  
- periodic scheduled retraining  

Pipeline:

Data → Validation → Training → Evaluation → Deployment → Monitoring

---

## 📦 Scalability Plan

### From 5 → 100+ Cameras

- Introduce message queue (Kafka/RabbitMQ)  
- Batch event ingestion  
- Partition by worker/site  

### Multi-Site Expansion

- Add site_id dimension  
- Use Postgres/warehouse  
- Deploy regional API gateways  

---

## 🐳 Running Locally

```bash
docker-compose up --build
```

Backend: http://localhost:8000  
Frontend: http://localhost:3000  

---

## 🌐 Live Demo

Frontend: https://ai-worker-productivity-dashboard-lilac.vercel.app  
Backend: https://ai-worker-dashboard-b6tl.onrender.com 

---

## 👨‍💻 Author

Syed Amer 
