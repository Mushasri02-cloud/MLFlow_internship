from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import mlflow.pyfunc

app = FastAPI(
    title="🧬 Clinical Inference REST Engine",
    description="Production-grade API layer serving registered MLflow models.",
    version="1.0.0"
)

# Set up central MLflow tracking target
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Define the incoming data validation structure using Pydantic
class PatientVitals(BaseModel):
    Pregnancies: int
    Glucose: float
    BloodPressure: float
    SkinThickness: float
    Insulin: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int

@app.get("/")
def read_root():
    return {"status": "online", "engine": "FastAPI Deployment Subsystem"}

@app.post("/predict/{model_name}")
def predict_risk(model_name: str, vitals: PatientVitals):
    # Validate requested model type
    if model_name not in ["Random_Forest", "Logistic_Regression"]:
        raise HTTPException(status_code=400, detail="Invalid model architecture target requested.")
        
    try:
        # Pull the latest deployment binary from the registry dynamically
        model_uri = f"models:/{model_name}/latest"
        model = mlflow.pyfunc.load_model(model_uri)
        
        # Convert incoming JSON payload to structural Pandas DataFrame
        input_data = pd.DataFrame([vitals.model_dump()])
        
        # Run inference computation
        prediction = int(model.predict(input_data)[0])
        
        return {
            "requested_architecture": model_name,
            "diabetic_risk_flag": prediction,
            "clinical_status": "High Risk Profile Detected" if prediction == 1 else "Normal Profile Confirmed"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference execution engine failure: {str(e)}")