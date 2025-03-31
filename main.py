from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from qwen_infer import extract_info_from_image
from utils.pdf_utils import convert_pdf_to_images
from PIL import Image
from pymongo import MongoClient
from datetime import datetime
import io
import os
import numpy as np

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load MongoDB connection string from environment variable, fallback to localhost
mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
mongo_client = MongoClient(mongo_uri)
db = mongo_client["document_ocr_db"]
collection = db["documents"]

@app.post("/api/documents")
async def upload_file(file: UploadFile = File(...)):
    allowed_extensions = [".jpg", ".jpeg", ".png", ".pdf"]
    filename = file.filename.lower()

    if not any(filename.endswith(ext) for ext in allowed_extensions):
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved_filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, saved_filename)

    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    extracted_text = ""
    results = []

    if filename.endswith(".pdf"):
        try:
            images = convert_pdf_to_images(contents)
            for idx, image in enumerate(images):
                text = extract_info_from_image(image)
                results.append({"page": idx + 1, "extracted": text})
                extracted_text += text + "\n"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PDF processing failed: {e}")

    else:
        try:
            image = Image.open(io.BytesIO(contents)).convert("RGB")
            text = extract_info_from_image(image)
            extracted_text = text
            results.append({"extracted": text})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image processing failed: {e}")

    doc_record = {
        "filename": saved_filename,
        "file_path": file_path,
        "file_data": contents,
        "content_type": file.content_type,
        "extracted_text": extracted_text,
        "upload_time": datetime.now(),
    }
    result = collection.insert_one(doc_record)

    return {
        "status": "success",
        "document_id": str(result.inserted_id),
        "results": results,
    }

@app.get("/api/documents")
def get_documents():
    docs = collection.find({})
    results = []
    for d in docs:
        results.append({
            "document_id": str(d["_id"]),
            "filename": d["filename"],
            "upload_time": d["upload_time"],
            "extracted_text_preview": d["extracted_text"][:100],
        })
    return results
