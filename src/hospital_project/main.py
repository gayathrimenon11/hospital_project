from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from . import models

# Automatically create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Queue System API")

# --- Pydantic Models ---
class PatientCreate(BaseModel):
    name: str
    doctor_name: str

class PatientResponse(BaseModel):
    patient_id: int
    name: str
    doctor_name: str
    status: str

    class Config:
        from_attributes = True


# --- Helper to Seed Default Doctors if Empty ---
def get_or_create_default_doctors(db: Session):
    count = db.query(models.Doctor).count()
    if count == 0:
        default_docs = [
            models.Doctor(name="Dr. Smith", specialization="General"),
            models.Doctor(name="Dr. Adams", specialization="Cardiology"),
            models.Doctor(name="Dr. Lee", specialization="Pediatrics"),
        ]
        db.add_all(default_docs)
        db.commit()


# --- API Routes ---
@app.get("/doctors")
def get_doctors(db: Session = Depends(get_db)):
    """Get list of available doctors from the database."""
    get_or_create_default_doctors(db)
    doctors = db.query(models.Doctor).all()
    return {"doctors": [f"{doc.name} ({doc.specialization})" for doc in doctors]}


@app.post("/patients/enqueue", response_model=PatientResponse)
def add_patient_to_queue(patient: PatientCreate, db: Session = Depends(get_db)):
    """Receptionist endpoint: Add a patient to a doctor's queue in the database."""
    # Extract doctor name (e.g., "Dr. Smith" from "Dr. Smith (General)")
    doc_name_key = patient.doctor_name.split(" (")[0].strip()
    
    doctor = db.query(models.Doctor).filter(models.Doctor.name.ilike(f"%{doc_name_key}%")).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    new_patient = models.Patient(
        name=patient.name,
        doctor_id=doctor.id,
        status="waiting"
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return {
        "patient_id": new_patient.id,
        "name": new_patient.name,
        "doctor_name": f"{doctor.name} ({doctor.specialization})",
        "status": new_patient.status
    }


@app.get("/queues/{doctor_name}")
def get_doctor_queue(doctor_name: str, db: Session = Depends(get_db)):
    """Get the full queue for a specific doctor from the database."""
    doc_name_key = doctor_name.split(" (")[0].strip()
    doctor = db.query(models.Doctor).filter(models.Doctor.name.ilike(f"%{doc_name_key}%")).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    patients = db.query(models.Patient).filter(models.Patient.doctor_id == doctor.id).all()
    
    queue_list = [
        {
            "patient_id": p.id,
            "name": p.name,
            "doctor_name": f"{doctor.name} ({doctor.specialization})",
            "status": p.status
        }
        for p in patients
    ]
    return {"doctor": doctor_name, "queue": queue_list}


@app.post("/queues/{doctor_name}/next")
def call_next_patient(doctor_name: str, db: Session = Depends(get_db)):
    """Doctor endpoint: Complete current patient & call the next patient in line."""
    doc_name_key = doctor_name.split(" (")[0].strip()
    doctor = db.query(models.Doctor).filter(models.Doctor.name.ilike(f"%{doc_name_key}%")).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Mark the currently consulting patient as completed
    current_patient = db.query(models.Patient).filter(
        models.Patient.doctor_id == doctor.id,
        models.Patient.status == "in_consultation"
    ).first()
    
    if current_patient:
        current_patient.status = "completed"

    # Find the next waiting patient (FIFO order by ID)
    next_patient = db.query(models.Patient).filter(
        models.Patient.doctor_id == doctor.id,
        models.Patient.status == "waiting"
    ).order_by(models.Patient.id.asc()).first()

    if next_patient:
        next_patient.status = "in_consultation"
        db.commit()
        return {
            "message": f"Now serving {next_patient.name}",
            "current_patient": {
                "patient_id": next_patient.id,
                "name": next_patient.name,
                "doctor_name": doctor_name,
                "status": next_patient.status
            }
        }

    db.commit()
    return {"message": "No patients remaining in line", "current_patient": None}