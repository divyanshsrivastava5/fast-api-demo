from fastapi import FastAPI
import json
from pathlib import Path

app = FastAPI()

PATIENT_FILE_PATH = Path(__file__).parent / "patients.json"

def load_data():
    with open(PATIENT_FILE_PATH, "r") as f:
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional API to manage your patient records"}

@app.get("/patients")
def get_patients():
    data = load_data()
    return data