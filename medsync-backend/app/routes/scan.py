import os
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.services.scanner_service import analyze_prescription
from app.database import get_db
from app.models.medication import Medication
from app.utils.scheduler import get_reminder_times, calculate_next_dose 

router = APIRouter()

@router.post("/scan")
async def scan_prescription(file: UploadFile = File(...), db: Session = Depends(get_db)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())
    
    try:
        results = analyze_prescription(temp_path)
        
        saved_meds = []
        for med_data in results:
            new_med = Medication(
                name=med_data["medication_name"],
                dosage=med_data["dosage"],
                schedule=med_data["schedule"]
            )
            db.add(new_med)
            saved_meds.append(new_med)
        
        db.commit() 
        
        return {"status": "success", "data": results}
    
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)



@router.get("/medications")
def get_all_medications(db: Session = Depends(get_db)):
    meds = db.query(Medication).all()
    results = []
    
    for med in meds:
        reminder_times = get_reminder_times(med.schedule)
        
        if not reminder_times:
            next_dose_str = "As Needed (SOS)"
            slots = []
        else:
            next_dose = calculate_next_dose(reminder_times)
            next_dose_str = next_dose.strftime("%H:%M")
            slots = [t.strftime("%H:%M") for t in reminder_times]
            
        results.append({
            "id": med.id,
            "name": med.name,
            "dosage": med.dosage,
            "original_schedule": med.schedule,
            "reminder_slots": slots,
            "next_dose_at": next_dose_str
        })
        
    return {"status": "success", "data": results}