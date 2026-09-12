import sqlite3
import numpy as np
import pandas as pd

DB_NAME = "students.db"
TABLE_NAME = "student_performance"
RANDOM_STATE = 42


def create_mock_data(n_students=500):
    """Create a reproducible mock student dataset."""
    rng = np.random.default_rng(RANDOM_STATE)

    study_hours = np.clip(rng.normal(4.5, 1.8, n_students), 0.5, 10)
    attendance = np.clip(rng.normal(82, 10, n_students), 45, 100)
    previous_gpa = np.clip(rng.normal(7.2, 1.2, n_students), 4.0, 10.0)

    parental_education = rng.choice(
    ["High School", "Diploma", "Bachelor", "Master"],
    size=n_students,
    p=[0.30, 0.20, 0.35, 0.15],
      ).astype(object)

    # Higher risk score means greater dropout risk.
    risk_score = (
        2.2
        - 0.48 * study_hours
        - 0.055 * (attendance - 75)
        - 0.90 * (previous_gpa - 6.5)
        + rng.normal(0, 1.2, n_students)
    )

    education_effect = {
        "High School": 0.35,
        "Diploma": 0.10,
        "Bachelor": -0.15,
        "Master": -0.30,
    }
    risk_score += pd.Series(parental_education).map(education_effect).to_numpy()

    # passed_status = 1 -> Safe, 0 -> At Risk.
    passed_status = (risk_score < 0.5).astype(int)

    # Add a few missing values so preprocessing demonstrates imputation.
    missing_count = max(1, int(n_students * 0.02))
    for column in ["study_hours", "attendance_percentage", "previous_gpa", "parental_education"]:
        indices = rng.choice(n_students, size=missing_count, replace=False)
        # Leave target column complete.
        if column == "parental_education":
            parental_education[indices] = np.nan
        elif column == "study_hours":
            study_hours[indices] = np.nan
        elif column == "attendance_percentage":
            attendance[indices] = np.nan
        elif column == "previous_gpa":
            previous_gpa[indices] = np.nan

    return pd.DataFrame(
        {
            "study_hours": study_hours,
            "attendance_percentage": attendance,
            "previous_gpa": previous_gpa,
            "parental_education": parental_education,
            "passed_status": passed_status,
        }
    )


def setup_database():
    df = create_mock_data()

    with sqlite3.connect(DB_NAME) as connection:
        df.to_sql(TABLE_NAME, connection, if_exists="replace", index=False)

    print(f"Database created: {DB_NAME}")
    print(f"Table created: {TABLE_NAME}")
    print(f"Rows inserted: {len(df)}")
    print("\nTarget distribution:")
    print(df["passed_status"].map({1: "Safe", 0: "At Risk"}).value_counts())


if __name__ == "__main__":
    setup_database()
