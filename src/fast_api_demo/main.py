from fastapi import FastAPI, Path, HTTPException, Query, Depends
import json
from pathlib import Path as FilePath
from typing import Annotated

app = FastAPI()

PATIENT_FILE_PATH = FilePath(__file__).parent / "patients.json"

def load_data():
    with open(PATIENT_FILE_PATH, "r") as f:
        data = json.load(f)
    return data

PatientData = Annotated[dict, Depends(load_data)]

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional API to manage your patient records"}

@app.get("/patients")
def get_patients(data: PatientData):
    return data

@app.get("/patient/{patient_id}")
def get_patient(data: PatientData, patient_id: str = Path(..., description="ID of the patient in the DB", example="P001")):
    if patient_id in data:
        return data.get(patient_id)
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(data: PatientData, sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi"), order: str = Query("asc", description="sort in asc or desc order")):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field select from {valid_fields}")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail=f"Invalid field select from {valid_fields}")

    sort_order = True if order == "desc" else False

    return sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)


    