# 📄 Qwen2-VL FastAPI OCR Extraction API

## 📦 Features
- Upload `.jpg`, `.png`, `.pdf` of Malaysian ICs or receipts
- Uses Qwen2-VL-2B-Instruct to extract structured data (e.g. name, IC number)
- Saves original files and extracted text into MongoDB

## 🧰 Requirements
- Docker
- Docker Compose
- NVIDIA GPU with CUDA drivers installed

## 🚀 Quick Start (Using Docker Compose)

### 1. Clone the repository

```bash
git clone https://github.com/HengYpinn/qwen2vl-fastapi-ocr.git
cd qwen2vl-fastapi-ocr
```
### 2. Build and start the services

```bash
docker-compose up --build
```

### 3. Test the API

```bash
curl -X POST -F "file=@example_ic.jpg" http://localhost:8000/api/documents
```
## 📂 MongoDB Output
- `filename`
- `content_typ`
- `file_data`
- `extracted_text`
- `upload_time`