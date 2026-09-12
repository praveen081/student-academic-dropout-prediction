from pathlib import Path

import joblib
import pandas as pd


MODEL_PATH = Path("models/best_model.joblib")


def predict_student():
    if not MODEL_PATH.exists():
        print("ERROR: Trained model not found.")
        print("Please run 'python main.py' first.")
        return

    model = joblib.load(MODEL_PATH)

    print("=" * 50)
    print("STUDENT DROPOUT RISK PREDICTION")
    print("=" * 50)

    try:
        study_hours = float(input("Study hours per day: "))
        attendance = float(input("Attendance percentage: "))
        previous_gpa = float(input("Previous GPA: "))

        print("\nParental Education:")
        print("1. High School")
        print("2. Diploma")
        print("3. Bachelor")
        print("4. Master")

        education_choice = input("Choose (1-4): ")

        education_map = {
            "1": "High School",
            "2": "Diploma",
            "3": "Bachelor",
            "4": "Master",
        }

        if education_choice not in education_map:
            print("Invalid parental education choice.")
            return

        parental_education = education_map[education_choice]

        # Validate inputs
        if study_hours < 0 or study_hours > 24:
            print("Study hours must be between 0 and 24.")
            return

        if attendance < 0 or attendance > 100:
            print("Attendance must be between 0 and 100.")
            return

        if previous_gpa < 0 or previous_gpa > 10:
            print("GPA must be between 0 and 10.")
            return

        # Create input DataFrame
        student = pd.DataFrame(
            {
                "study_hours": [study_hours],
                "attendance_percentage": [attendance],
                "previous_gpa": [previous_gpa],
                "parental_education": [parental_education],
            }
        )

        # Make prediction
        prediction = model.predict(student)[0]

        # Get prediction probabilities
        probabilities = model.predict_proba(student)[0]

        classes = list(model.classes_)

        # Find probability for At Risk (class 0)
        at_risk_index = classes.index(0)
        at_risk_probability = probabilities[at_risk_index]

        print("\n" + "=" * 50)
        print("PREDICTION RESULT")
        print("=" * 50)

        if prediction == 0:
            print("Prediction: AT RISK")
            print(
                f"At-Risk Probability: "
                f"{at_risk_probability * 100:.2f}%"
            )
            print(
                "Recommendation: "
                "The student may require additional academic attention."
            )

        else:
            print("Prediction: SAFE")
            print(
                f"At-Risk Probability: "
                f"{at_risk_probability * 100:.2f}%"
            )
            print(
                "Recommendation: "
                "The student's current indicators appear relatively safe."
            )

        print("=" * 50)

    except ValueError:
        print("\nInvalid input.")
        print("Please enter numerical values where required.")


if __name__ == "__main__":
    predict_student()