import sqlite3
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DB_NAME = "students.db"
TABLE_NAME = "student_performance"

NUMERIC_FEATURES = [
    "study_hours",
    "attendance_percentage",
    "previous_gpa",
]
CATEGORICAL_FEATURES = ["parental_education"]
TARGET = "passed_status"


def load_data():
    """Load raw data from SQLite using SQL."""
    query = f"""
        SELECT
            study_hours,
            attendance_percentage,
            previous_gpa,
            parental_education,
            passed_status
        FROM {TABLE_NAME}
    """

    with sqlite3.connect(DB_NAME) as connection:
        return pd.read_sql_query(query, connection)


def build_preprocessor():
    """Create preprocessing pipelines for numeric and categorical features."""
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, NUMERIC_FEATURES),
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )


def prepare_data():
    """Return raw X/y and the preprocessing transformer."""
    df = load_data()

    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES].copy()
    y = df[TARGET].astype(int).copy()

    preprocessor = build_preprocessor()
    return X, y, preprocessor


if __name__ == "__main__":
    data = load_data()
    print("Data loaded successfully from SQLite.")
    print(data.head())
    print("\nMissing values before preprocessing:")
    print(data.isnull().sum())
