from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from data_preprocessing import prepare_data


MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "best_model.joblib"
TEST_DATA_PATH = MODEL_DIR / "test_data.joblib"


def train_models():
    X, y, preprocessor = prepare_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            random_state=42,
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            max_depth=8,
            min_samples_split=5,
            random_state=42,
            class_weight="balanced",
        ),
    }

    results = {}

    for name, estimator in models.items():

        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("classifier", estimator),
            ]
        )

        pipeline.fit(X_train, y_train)

        predictions = pipeline.predict(X_test)

        results[name] = {
            "model": pipeline,

            "accuracy": accuracy_score(
                y_test,
                predictions
            ),

            # At Risk = 0
            "precision": precision_score(
                y_test,
                predictions,
                pos_label=0,
                zero_division=0,
            ),

            # At Risk = 0
            "recall": recall_score(
                y_test,
                predictions,
                pos_label=0,
                zero_division=0,
            ),
        }

    # Prioritize identifying At-Risk students.
    best_name = max(
        results,
        key=lambda name: (
            results[name]["recall"],
            results[name]["precision"],
            results[name]["accuracy"],
        ),
    )

    best_model = results[best_name]["model"]

    # Save trained model
    joblib.dump(best_model, MODEL_PATH)

    # Save test data for evaluation
    joblib.dump(
        {
            "X_test": X_test,
            "y_test": y_test,
            "best_name": best_name,
        },
        TEST_DATA_PATH,
    )

    print("\nModel comparison:")

    for name, result in results.items():

        print(
            f"{name}: "
            f"Accuracy={result['accuracy']:.4f}, "
            f"At-Risk Precision={result['precision']:.4f}, "
            f"At-Risk Recall={result['recall']:.4f}"
        )

    print(f"\nBest model: {best_name}")
    print(f"Saved to: {MODEL_PATH}")

    return best_model, best_name


if __name__ == "__main__":
    train_models()