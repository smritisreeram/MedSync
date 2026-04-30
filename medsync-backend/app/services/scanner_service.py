from fastapi import APIRouter, UploadFile, File
from app.services.scanner_service import analyze_prescription

router = APIRouter()

@router.post("/scan-prescription")
async def scan_prescription(file: UploadFile = File(...)):
    # 1. Save the uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # 2. Call your Gemini logic
    results = analyze_prescription(temp_path)
    
    # 3. Clean up and return
    os.remove(temp_path)
    return {"status": "success", "data": results}   