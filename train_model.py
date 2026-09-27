from pathlib import Path
import json

import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    make_scorer,
)

from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_val_score,
)

from sklearn.pipeline import Pipeline

from data_preprocessing import prepare_data


# ============================================================
# DIRECTORIES
# ============================================================

MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================
# FILE PATHS
# ============================================================

MODEL_PATH = MODEL_DIR / "best_model.joblib"
TEST_DATA_PATH = MODEL_DIR / "test_data.joblib"

MODEL_COMPARISON_PATH = OUTPUT_DIR / "model_comparison.json"


# ============================================================
# TRAIN MODELS
# ============================================================

def train_models():

    # --------------------------------------------------------
    # Load and prepare data
    # --------------------------------------------------------

    X, y, preprocessor = prepare_data()

    # --------------------------------------------------------
    # Train/Test Split
    # --------------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    # --------------------------------------------------------
    # Models
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Store results
    # --------------------------------------------------------

    results = {}

    # ========================================================
    # TRAIN AND EVALUATE EACH MODEL
    # ========================================================

    for name, estimator in models.items():

        print(f"\nTraining {name}...")

        # ----------------------------------------------------
        # Create complete ML pipeline
        # ----------------------------------------------------

        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("classifier", estimator),
            ]
        )

        # ----------------------------------------------------
        # Train model
        # ----------------------------------------------------

        pipeline.fit(
            X_train,
            y_train
        )

        # ----------------------------------------------------
        # Predictions
        # ----------------------------------------------------

        predictions = pipeline.predict(
            X_test
        )

        # ----------------------------------------------------
        # Accuracy
        # ----------------------------------------------------

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        # ----------------------------------------------------
        # At-Risk Precision
        #
        # At Risk = class 0
        # ----------------------------------------------------

        precision = precision_score(
            y_test,
            predictions,
            pos_label=0,
            zero_division=0,
        )

        # ----------------------------------------------------
        # At-Risk Recall
        #
        # At Risk = class 0
        # ----------------------------------------------------

        recall = recall_score(
            y_test,
            predictions,
            pos_label=0,
            zero_division=0,
        )

        # ----------------------------------------------------
        # At-Risk F1 Score
        # ----------------------------------------------------

        f1 = f1_score(
            y_test,
            predictions,
            pos_label=0,
            zero_division=0,
        )

        # ----------------------------------------------------
        # ROC-AUC
        #
        # Convert At-Risk class (0) into positive class (1)
        # for ROC-AUC calculation.
        # ----------------------------------------------------

        probabilities = pipeline.predict_proba(
            X_test
        )

        # Find the probability column belonging to class 0
        at_risk_probability = probabilities[
            :,
            list(pipeline.classes_).index(0)
        ]

        y_at_risk = (
            y_test == 0
        ).astype(int)

        roc_auc = roc_auc_score(
            y_at_risk,
            at_risk_probability
        )

        # ----------------------------------------------------
        # 5-Fold Cross Validation
        #
        # Evaluate At-Risk F1 score across 5 folds.
        # ----------------------------------------------------

        cv = StratifiedKFold(
            n_splits=5,
            shuffle=True,
            random_state=42,
        )

        at_risk_f1_scorer = make_scorer(
            f1_score,
            pos_label=0,
            zero_division=0,
        )

        cv_scores = cross_val_score(
            pipeline,
            X,
            y,
            cv=cv,
            scoring=at_risk_f1_scorer,
        )

        cv_mean = cv_scores.mean()
        cv_std = cv_scores.std()

        # ----------------------------------------------------
        # Save all metrics
        # ----------------------------------------------------

        results[name] = {

            "model": pipeline,

            "accuracy": accuracy,

            "precision": precision,

            "recall": recall,

            "f1": f1,

            "roc_auc": roc_auc,

            "cv_f1_mean": cv_mean,

            "cv_f1_std": cv_std,
        }

    # ========================================================
    # SELECT BEST MODEL
    #
    # At-Risk Recall is prioritized because this is an
    # early-warning system.
    # ========================================================

    best_name = max(
        results,
        key=lambda name: (
            results[name]["recall"],
            results[name]["precision"],
            results[name]["accuracy"],
        ),
    )

    best_model = results[best_name]["model"]

    # ========================================================
    # SAVE BEST MODEL
    # ========================================================

    joblib.dump(
        best_model,
        MODEL_PATH
    )

    # ========================================================
    # SAVE TEST DATA
    # ========================================================

    joblib.dump(
        {
            "X_test": X_test,
            "y_test": y_test,
            "best_name": best_name,
        },
        TEST_DATA_PATH,
    )

    # ========================================================
    # SAVE MODEL COMPARISON FOR DASHBOARD
    # ========================================================

    comparison = {}

    for name, result in results.items():

        comparison[name] = {

            "accuracy": result["accuracy"],

            "precision": result["precision"],

            "recall": result["recall"],

            "f1": result["f1"],

            "roc_auc": result["roc_auc"],

            "cv_f1_mean": result["cv_f1_mean"],

            "cv_f1_std": result["cv_f1_std"],
        }

    with open(
        MODEL_COMPARISON_PATH,
        "w"
    ) as file:

        json.dump(
            comparison,
            file,
            indent=4
        )

    # ========================================================
    # PRINT MODEL COMPARISON
    # ========================================================

    print("\n" + "=" * 60)
    print("MODEL COMPARISON")
    print("=" * 60)

    for name, result in results.items():

        print(f"\n{name}")

        print(
            f"Accuracy          : "
            f"{result['accuracy']:.4f}"
        )

        print(
            f"At-Risk Precision : "
            f"{result['precision']:.4f}"
        )

        print(
            f"At-Risk Recall    : "
            f"{result['recall']:.4f}"
        )

        print(
            f"At-Risk F1 Score  : "
            f"{result['f1']:.4f}"
        )

        print(
            f"ROC-AUC           : "
            f"{result['roc_auc']:.4f}"
        )

        print(
            f"5-Fold CV F1      : "
            f"{result['cv_f1_mean']:.4f} "
            f"+/- {result['cv_f1_std']:.4f}"
        )

    # ========================================================
    # BEST MODEL INFORMATION
    # ========================================================

    print("\n" + "=" * 60)

    print(
        f"Best model: {best_name}"
    )

    print(
        f"Saved model: {MODEL_PATH}"
    )

    print(
        f"Saved test data: {TEST_DATA_PATH}"
    )

    print(
        f"Saved comparison: {MODEL_COMPARISON_PATH}"
    )

    print("=" * 60)

    return best_model, best_name


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    train_models()
