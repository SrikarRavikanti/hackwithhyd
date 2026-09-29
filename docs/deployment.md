# Deployment Guide

## 1. Local Run
```bash
# 1. Install dependencies
python -m pip install -r requirements.txt

# 2. Start the unified service (Backend + Frontend)
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 2. Docker Deployment
Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
Build and run:
```bash
docker build -t feedback-memory-os .
docker run -p 8000:8000 -e HINDSIGHT_API_KEY=your_key feedback-memory-os
```

---

## 3. Production Cloud Deployment (Render / Railway / Fly.io)
1. Set environment variables:
   - `HINDSIGHT_API_URL=https://api.hindsight.vectorize.io`
   - `HINDSIGHT_API_KEY=<your-key>`
   - `HINDSIGHT_BANK_ID=workspace_nova_analytics`
2. Build command: `pip install -r requirements.txt`
3. Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
