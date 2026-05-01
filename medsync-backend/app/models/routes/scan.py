import os
from fastapi import APIRouter, UploadFile, File
from app.services.scanner_service import analyze_prescription

# Create the router object
router = APIRouter()

@router.post("/scan")
async def scan_prescription(file: UploadFile = File(...)):
    # 1. Define where to save the uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    
    # 2. Write the uploaded bytes to that temp file
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())
    
    try:
        # 3. Call the logic from our Service file
        results = analyze_prescription(temp_path)
        return {"status": "success", "data": results}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
    finally:
        # 4. ALWAYS delete the temp file so your server doesn't get cluttered
        if os.path.exists(temp_path):
            os.remove(temp_path)