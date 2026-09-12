from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "best_model.joblib"

app = FastAPI(
    title="Student Dropout Risk Prediction",
    description="ML-based student academic performance and dropout risk prediction",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@app.post("/predict")
async def predict_student(data: dict):

    if not MODEL_PATH.exists():
        return {
            "success": False,
            "error": "Trained model not found. Run python main.py first.",
        }

    try:
        study_hours = float(data["study_hours"])
        attendance = float(data["attendance_percentage"])
        previous_gpa = float(data["previous_gpa"])
        parental_education = data["parental_education"]

        if study_hours < 0 or study_hours > 24:
            return {
                "success": False,
                "error": "Study hours must be between 0 and 24.",
            }

        if attendance < 0 or attendance > 100:
            return {
                "success": False,
                "error": "Attendance must be between 0 and 100.",
            }

        if previous_gpa < 0 or previous_gpa > 10:
            return {
                "success": False,
                "error": "GPA must be between 0 and 10.",
            }

        valid_education = [
            "High School",
            "Diploma",
            "Bachelor",
            "Master",
        ]

        if parental_education not in valid_education:
            return {
                "success": False,
                "error": "Invalid parental education.",
            }

        model = joblib.load(MODEL_PATH)

        student = pd.DataFrame(
            {
                "study_hours": [study_hours],
                "attendance_percentage": [attendance],
                "previous_gpa": [previous_gpa],
                "parental_education": [parental_education],
            }
        )

        prediction = int(model.predict(student)[0])

        probabilities = model.predict_proba(student)[0]

        classes = list(model.classes_)
        at_risk_index = classes.index(0)

        at_risk_probability = float(
            probabilities[at_risk_index]
        )

        if prediction == 0:
            result = "AT RISK"
            recommendation = (
                "The student may require additional academic "
                "support and monitoring."
            )
        else:
            result = "SAFE"
            recommendation = (
                "The student's current academic indicators "
                "appear relatively safe."
            )

        return {
            "success": True,
            "prediction": result,
            "risk_probability": round(
                at_risk_probability * 100,
                2,
            ),
            "recommendation": recommendation,
        }

    except (KeyError, ValueError, TypeError):
        return {
            "success": False,
            "error": "Please provide valid student information.",
        }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_available": MODEL_PATH.exists(),
    }