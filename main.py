from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional

app = FastAPI(title="Hospital Queue System API")

# --- In-Memory Database ---
doctors = ["Dr. Smith (General)", "Dr. Adams (Cardiology)", "Dr. Lee (Pediatrics)"]

# Queue structure: { "Doctor Name": [ {"patient_id": 1, "name": "Alice", "status": "waiting"}, ... ] }
queues: Dict[str, List[dict]] = {doc: [] for doc in doctors}
patient_counter = 1


# --- Data Models ---
class PatientCreate(BaseModel):
    name: str
    doctor_name: str


class PatientResponse(BaseModel):
    patient_id: int
    name: str
    doctor_name: str
    status: str


# --- API Routes ---
@app.get("/doctors")
def get_doctors():
    """Get list of available doctors."""
    return {"doctors": doctors}


@app.post("/patients/enqueue", response_model=PatientResponse)
def add_patient_to_queue(patient: PatientCreate):
    """Receptionist endpoint: Add a patient to a doctor's queue."""
    global patient_counter
    if patient.doctor_name not in queues:
        raise HTTPException(status_code=404, detail="Doctor not found")

    new_patient = {
        "patient_id": patient_counter,
        "name": patient.name,
        "doctor_name": patient.doctor_name,
        "status": "waiting"
    }
    patient_counter += 1
    queues[patient.doctor_name].append(new_patient)
    return new_patient


@app.get("/queues/{doctor_name}")
def get_doctor_queue(doctor_name: str):
    """Get the full queue for a specific doctor."""
    if doctor_name not in queues:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {"doctor": doctor_name, "queue": queues[doctor_name]}


@app.post("/queues/{doctor_name}/next")
def call_next_patient(doctor_name: str):
    """Doctor endpoint: Complete current patient & call the next patient in line."""
    if doctor_name not in queues:
        raise HTTPException(status_code=404, detail="Doctor not found")

    doc_queue = queues[doctor_name]
    
    # Mark the currently consulting patient as completed (if any)
    for patient in doc_queue:
        if patient["status"] == "in_consultation":
            patient["status"] = "completed"
            break

    # Find the next waiting patient
    for patient in doc_queue:
        if patient["status"] == "waiting":
            patient["status"] = "in_consultation"
            return {"message": f"Now serving {patient['name']}", "current_patient": patient}

    return {"message": "No patients remaining in line", "current_patient": None}