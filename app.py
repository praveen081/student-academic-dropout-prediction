from pathlib import Path

import joblib
import pandas as pd
import sqlite3
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "best_model.joblib"
DB_PATH = BASE_DIR / "students.db"

app = FastAPI(
    title="Student Academic Risk Analytics & Early-Warning System",
    description="ML-based student academic risk prediction and early-warning system",
    version="2.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


# ---------------------------------------------------------
# RISK LEVEL
# ---------------------------------------------------------

def get_risk_level(probability):
    if probability < 30:
        return "LOW"
    elif probability < 60:
        return "MEDIUM"
    else:
        return "HIGH"


# ---------------------------------------------------------
# EXPLANATION
# ---------------------------------------------------------

def generate_explanation(
    study_hours,
    attendance,
    previous_gpa
):
    factors = []

    if attendance < 60:
        factors.append(
            "Very low attendance is increasing the student's risk."
        )
    elif attendance < 75:
        factors.append(
            "Attendance is below the recommended level."
        )

    if previous_gpa < 5:
        factors.append(
            "Previous GPA is low and is an important academic risk factor."
        )
    elif previous_gpa < 7:
        factors.append(
            "Previous GPA indicates moderate academic risk."
        )

    if study_hours < 2:
        factors.append(
            "Low daily study time may contribute to academic difficulty."
        )
    elif study_hours < 4:
        factors.append(
            "Daily study time could be improved."
        )

    if not factors:
        factors.append(
            "The student's current academic indicators do not show major warning signs."
        )

    return factors


# ---------------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------------

def generate_recommendations(
    study_hours,
    attendance,
    previous_gpa,
    risk_level
):
    recommendations = []

    if attendance < 75:
        recommendations.append(
            "Improve attendance and maintain regular class participation."
        )

    if study_hours < 3:
        recommendations.append(
            "Increase focused study time to at least 3 hours per day."
        )

    if previous_gpa < 6:
        recommendations.append(
            "Provide academic mentoring and focus on weak subjects."
        )

    if risk_level == "HIGH":
        recommendations.append(
            "Consider early academic intervention and regular progress monitoring."
        )
    elif risk_level == "MEDIUM":
        recommendations.append(
            "Monitor academic progress regularly and provide additional support when required."
        )
    else:
        recommendations.append(
            "Continue the current academic routine and maintain consistent performance."
        )

    return recommendations

# ---------------------------------------------------------
# DASHBOARD PAGE
# ---------------------------------------------------------

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"request": request},
    )


# ---------------------------------------------------------
# PREDICTION API
# ---------------------------------------------------------

@app.post("/predict")
async def predict_student(data: dict):

    if not MODEL_PATH.exists():
        return {
            "success": False,
            "error": "Trained model not found. Run python main.py first.",
        }

    try:
        # ---------------------------------------------
        # Read input
        # ---------------------------------------------

        study_hours = float(data["study_hours"])
        attendance = float(data["attendance_percentage"])
        previous_gpa = float(data["previous_gpa"])
        parental_education = data["parental_education"]

        # ---------------------------------------------
        # Validate input
        # ---------------------------------------------

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

        # ---------------------------------------------
        # Load model
        # ---------------------------------------------

        model = joblib.load(MODEL_PATH)

        # ---------------------------------------------
        # Create student DataFrame
        # ---------------------------------------------

        student = pd.DataFrame(
            {
                "study_hours": [study_hours],
                "attendance_percentage": [attendance],
                "previous_gpa": [previous_gpa],
                "parental_education": [parental_education],
            }
        )

        # ---------------------------------------------
        # Prediction
        # ---------------------------------------------

        prediction = int(model.predict(student)[0])

        probabilities = model.predict_proba(student)[0]

        classes = list(model.classes_)

        at_risk_index = classes.index(0)

        at_risk_probability = float(
            probabilities[at_risk_index]
        )

        risk_percentage = round(
            at_risk_probability * 100,
            2
        )

        # ---------------------------------------------
        # Risk level
        # ---------------------------------------------

        risk_level = get_risk_level(
            risk_percentage
        )

        # ---------------------------------------------
        # Prediction result
        # ---------------------------------------------

        if prediction == 0:
            result = "AT RISK"
        else:
            result = "SAFE"

        # ---------------------------------------------
        # Explanation
        # ---------------------------------------------

        explanation = generate_explanation(
            study_hours,
            attendance,
            previous_gpa
        )

        # ---------------------------------------------
        # Recommendations
        # ---------------------------------------------

        recommendations = generate_recommendations(
            study_hours,
            attendance,
            previous_gpa,
            risk_level
        )

        # ---------------------------------------------
        # API response
        # ---------------------------------------------

        return {
            "success": True,

            "prediction": result,

            "risk_probability": risk_percentage,

            "risk_level": risk_level,

            "student_profile": {
                "study_hours": study_hours,
                "attendance": attendance,
                "previous_gpa": previous_gpa,
                "parental_education": parental_education,
            },

            "risk_factors": explanation,

            "recommendations": recommendations,
        }

    except (KeyError, ValueError, TypeError):

        return {
            "success": False,
            "error": "Please provide valid student information.",
        }


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model_available": MODEL_PATH.exists(),
        "version": "2.0.0",
    }
    # ---------------------------------------------------------
# ANALYTICS DASHBOARD API
# ---------------------------------------------------------

@app.get("/api/dashboard")
def dashboard():

    if not DB_PATH.exists():
        return {
            "success": False,
            "error": "Database not found."
        }

    try:

        with sqlite3.connect(DB_PATH) as connection:

            query = """
                SELECT
                    study_hours,
                    attendance_percentage,
                    previous_gpa,
                    parental_education,
                    passed_status
                FROM student_performance
            """

            df = pd.read_sql_query(
                query,
                connection
            )

        # ---------------------------------------------
        # Basic statistics
        # ---------------------------------------------

        total_students = len(df)

        at_risk_students = int(
            (df["passed_status"] == 0).sum()
        )

        safe_students = int(
            (df["passed_status"] == 1).sum()
        )

        average_gpa = round(
            df["previous_gpa"].mean(),
            2
        )

        average_attendance = round(
            df["attendance_percentage"].mean(),
            2
        )

        average_study_hours = round(
            df["study_hours"].mean(),
            2
        )

        # ---------------------------------------------
        # Risk percentage
        # ---------------------------------------------

        at_risk_percentage = round(
            (at_risk_students / total_students) * 100,
            2
        )

        safe_percentage = round(
            (safe_students / total_students) * 100,
            2
        )

        # ---------------------------------------------
        # Parental education distribution
        # ---------------------------------------------

        education_distribution = (
            df["parental_education"]
            .fillna("Unknown")
            .value_counts()
            .to_dict()
        )

        # ---------------------------------------------
        # Risk distribution
        # ---------------------------------------------

        risk_distribution = {
            "At Risk": at_risk_students,
            "Safe": safe_students
        }

        # ---------------------------------------------
        # Academic averages by status
        # ---------------------------------------------

        grouped = (
            df.groupby("passed_status")
            .agg(
                average_gpa=("previous_gpa", "mean"),
                average_attendance=(
                    "attendance_percentage",
                    "mean"
                ),
                average_study_hours=(
                    "study_hours",
                    "mean"
                )
            )
            .round(2)
        )

        academic_comparison = {
            "at_risk": {
                "average_gpa": float(
                    grouped.loc[0, "average_gpa"]
                ) if 0 in grouped.index else 0,

                "average_attendance": float(
                    grouped.loc[
                        0,
                        "average_attendance"
                    ]
                ) if 0 in grouped.index else 0,

                "average_study_hours": float(
                    grouped.loc[
                        0,
                        "average_study_hours"
                    ]
                ) if 0 in grouped.index else 0
            },

            "safe": {
                "average_gpa": float(
                    grouped.loc[1, "average_gpa"]
                ) if 1 in grouped.index else 0,

                "average_attendance": float(
                    grouped.loc[
                        1,
                        "average_attendance"
                    ]
                ) if 1 in grouped.index else 0,

                "average_study_hours": float(
                    grouped.loc[
                        1,
                        "average_study_hours"
                    ]
                ) if 1 in grouped.index else 0
            }
        }

        return {

            "success": True,

            "summary": {

                "total_students":
                    total_students,

                "at_risk_students":
                    at_risk_students,

                "safe_students":
                    safe_students,

                "at_risk_percentage":
                    at_risk_percentage,

                "safe_percentage":
                    safe_percentage,

                "average_gpa":
                    average_gpa,

                "average_attendance":
                    average_attendance,

                "average_study_hours":
                    average_study_hours
            },

            "risk_distribution":
                risk_distribution,

            "education_distribution":
                education_distribution,

            "academic_comparison":
                academic_comparison
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }
