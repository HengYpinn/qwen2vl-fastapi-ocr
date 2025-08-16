import os
import io
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
from pymongo import MongoClient
from qwen_infer import extract_info_from_image
from utils.image_quality import compute_blur_intensity, compute_glare_intensity
from utils.pdf_utils import convert_pdf_to_images
from utils.passport_utils import normalize_passport_number
from utils.ssm_utils import normalize_ssm_registration_numbers
from prompts import PROMPTS
app = FastAPI()

# --- Configuration ----------------------------------------------------------

# Where to store uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# MongoDB setup (uses MONGO_URI env var or defaults to localhost)
mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
mongo_client = MongoClient(mongo_uri)
db = mongo_client["document_ocr_db"]
collection = db["documents"]

# Supported file types
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}

# --- Core inference handler ------------------------------------------------

def handle_inference(contents: bytes, prompt_key: str):
    """
    Convert uploaded contents (image or PDF) into one or more PIL Images,
    run extract_info_from_image(...) on each with the appropriate prompt,
    and return a list of result dicts.
    """
    prompt = PROMPTS[prompt_key]

    # Determine images to process
    if contents[:4] == b"%PDF":
        try:
            images = convert_pdf_to_images(contents)
        except Exception as e:
            raise HTTPException(500, f"PDF conversion failed: {e}")
    else:
        # Single-image endpoint (IC or passport or image receipt)
        try:
            img = Image.open(io.BytesIO(contents)).convert("RGB")
            images = [img]
        except Exception as e:
            raise HTTPException(500, f"Image decoding failed: {e}")

    # Run inference on each image
    results = []
    for idx, img in enumerate(images):
        data = extract_info_from_image(img, prompt)
        blur = compute_blur_intensity(img)
        glare = compute_glare_intensity(img)
        data.update({"blurIntensity": blur, "glareIntensity": glare})
        
        # Apply post-processing for passport documents
        if prompt_key == "passport":
            # Apply passport number normalization (belt-and-suspenders sanitizer)
            # The Qwen2-VL model may return extra information in the passport number
            # field, so we normalize it according to ICAO standards
            if "passportNumber" in data:
                passport_num = data.get("passportNumber")
                if passport_num:  # Only normalize if not None/empty
                    data["passportNumber"] = normalize_passport_number(
                        str(passport_num), 
                        data.get("countryCode")
                    )
        
        # Apply post-processing for SSM Form D documents
        elif prompt_key == "ssm_form_d":
            # Apply SSM registration number normalization (belt-and-suspenders sanitizer)
            # The Qwen2-VL model may return combined registration numbers that need splitting
            # Example: "201934234321 (RT0069300-M)" should be split into separate fields
            data = normalize_ssm_registration_numbers(data)
        
        if len(images) > 1:
            results.append({"page": idx + 1, "data": data})
        else:
            results.append({"data": data})

    return results


# --- API Endpoints ----------------------------------------------------------

@app.post("/api/ic")
async def extract_ic(file: UploadFile = File(...)):
    """
    Detect Malaysian IC and extract its fields.
    """
    ext = os.path.splitext(file.filename.lower())[1]
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Unsupported file type.")
    contents = await file.read()

    # Save upload for history
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved_name = f"{timestamp}_{file.filename}"
    saved_path = os.path.join(UPLOAD_DIR, saved_name)
    with open(saved_path, "wb") as f:
        f.write(contents)

    # Run inference
    results = handle_inference(contents, "ic")

    # Record to MongoDB
    record = {
        "filename": saved_name,
        "file_path": saved_path,
        "content_type": file.content_type,
        "results": results,
        "upload_time": datetime.now(),
    }
    doc_id = collection.insert_one(record).inserted_id

    return JSONResponse({"status": "success", "document_id": str(doc_id), "results": results})


@app.post("/api/passport")
async def extract_passport(file: UploadFile = File(...)):
    """
    Detect an international passport and extract its fields.
    """
    ext = os.path.splitext(file.filename.lower())[1]
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Unsupported file type.")
    contents = await file.read()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved_name = f"{timestamp}_{file.filename}"
    saved_path = os.path.join(UPLOAD_DIR, saved_name)
    with open(saved_path, "wb") as f:
        f.write(contents)

    results = handle_inference(contents, "passport")

    record = {
        "filename": saved_name,
        "file_path": saved_path,
        "content_type": file.content_type,
        "results": results,
        "upload_time": datetime.now(),
    }
    doc_id = collection.insert_one(record).inserted_id

    return JSONResponse({"status": "success", "document_id": str(doc_id), "results": results})


@app.post("/api/cash-deposit")
async def extract_cash_deposit(file: UploadFile = File(...)):
    """
    Extract fields from a cash deposit receipt.
    """
    ext = os.path.splitext(file.filename.lower())[1]
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Unsupported file type.")
    contents = await file.read()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved_name = f"{timestamp}_{file.filename}"
    saved_path = os.path.join(UPLOAD_DIR, saved_name)
    with open(saved_path, "wb") as f:
        f.write(contents)

    results = handle_inference(contents, "cash_deposit")

    record = {
        "filename": saved_name,
        "file_path": saved_path,
        "content_type": file.content_type,
        "results": results,
        "upload_time": datetime.now(),
    }
    doc_id = collection.insert_one(record).inserted_id

    return JSONResponse({"status": "success", "document_id": str(doc_id), "results": results})

@app.post("/api/bank-transfer")
async def extract_bank_transfer(file: UploadFile = File(...)):
    """
    Extract fields from bank transfer receipt.
    """
    ext = os.path.splitext(file.filename.lower())[1]
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Unsupported file type.")
    contents = await file.read()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved_name = f"{timestamp}_{file.filename}"
    saved_path = os.path.join(UPLOAD_DIR, saved_name)
    with open(saved_path, "wb") as f:
        f.write(contents)

    results = handle_inference(contents, "bank_transfer")

    record = {
        "filename": saved_name,
        "file_path": saved_path,
        "content_type": file.content_type,
        "results": results,
        "upload_time": datetime.now(),
    }
    doc_id = collection.insert_one(record).inserted_id

    return JSONResponse({"status": "success", "document_id": str(doc_id), "results": results})

@app.post("/api/ssm-form-d")
async def extract_ssm_form_d(file: UploadFile = File(...)):
    """
    Extract fields from SSM Form D (Malaysia company registration).
    """
    ext = os.path.splitext(file.filename.lower())[1]
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Unsupported file type.")
    contents = await file.read()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved_name = f"{timestamp}_{file.filename}"
    saved_path = os.path.join(UPLOAD_DIR, saved_name)
    with open(saved_path, "wb") as f:
        f.write(contents)

    results = handle_inference(contents, "ssm_form_d")

    record = {
        "filename": saved_name,
        "file_path": saved_path,
        "content_type": file.content_type,
        "results": results,
        "upload_time": datetime.now(),
    }
    doc_id = collection.insert_one(record).inserted_id

    return JSONResponse({"status": "success", "document_id": str(doc_id), "results": results})

@app.post("/api/utility-bill")
async def extract_utility_bill(file: UploadFile = File(...)):
    """
    Extract fields from Malaysia utility bills (Water Bill, Indah Water, Broadband Internet).
    """
    ext = os.path.splitext(file.filename.lower())[1]
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Unsupported file type.")
    contents = await file.read()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved_name = f"{timestamp}_{file.filename}"
    saved_path = os.path.join(UPLOAD_DIR, saved_name)
    with open(saved_path, "wb") as f:
        f.write(contents)

    results = handle_inference(contents, "utility_bill")

    record = {
        "filename": saved_name,
        "file_path": saved_path,
        "content_type": file.content_type,
        "results": results,
        "upload_time": datetime.now(),
    }
    doc_id = collection.insert_one(record).inserted_id

    return JSONResponse({"status": "success", "document_id": str(doc_id), "results": results})

@app.get("/api/documents")
def list_documents():
    """
    List all processed documents with previews.
    """
    docs = collection.find().sort("upload_time", -1)
    out = []
    for d in docs:
        out.append({
            "document_id": str(d["_id"]),
            "filename": d["filename"],
            "upload_time": d["upload_time"],
            "preview": d.get("results", [])[:1]  # show first entry only, or empty list if missing
        })
    return out


# --- Run with: uvicorn main:app --host 0.0.0.0 --port 8000 ------------------
