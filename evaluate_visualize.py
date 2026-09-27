from pathlib import Path
import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    make_scorer
)

from data_preprocessing import load_data

MODEL_PATH = Path("models/best_model.joblib")
TEST_DATA_PATH = Path("models/test_data.joblib")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def evaluate_model():
    model = joblib.load(MODEL_PATH)
    test_data = joblib.load(TEST_DATA_PATH)

    X_test = test_data["X_test"]
    y_test = test_data["y_test"]
    best_name = test_data["best_name"]

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, zero_division=0)
    recall = recall_score(y_test, predictions, zero_division=0)
     f1 = f1_score(y_test, predictions, pos_label=0)
    y_probability = model.predict_proba(X_test)[:, list(model.classes_).index(0)]
    roc_auc = roc_auc_score( y_test,y_probability)

    cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)
at_risk_f1_scorer = make_scorer(
    f1_score,
    pos_label=0
)

cv_scores = cross_val_score(
    model,
    X,
    y,
    cv=cv,
    scoring=at_risk_f1_scorer
)

cv_mean = cv_scores.mean()
cv_std = cv_scores.std()

   print(f"\nEvaluation: {best_name}")

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"ROC-AUC  : {roc_auc:.4f}")

print(
    f"5-Fold CV F1: "
    f"{cv_mean:.4f} ± {cv_std:.4f}"
)
    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            target_names=["At Risk", "Safe"],
            zero_division=0,
        )
    )

    # Confusion matrix.
    cm = confusion_matrix(y_test, predictions)
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["At Risk", "Safe"],
        yticklabels=["At Risk", "Safe"],
    )
    plt.title(f"Confusion Matrix - {best_name}")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "confusion_matrix.png", dpi=150)
    plt.close()

    # Correlation heatmap uses numeric columns from the original dataset.
    df = load_data()
    numeric_df = df[
        ["study_hours", "attendance_percentage", "previous_gpa", "passed_status"]
    ].copy()

    plt.figure(figsize=(7, 5))
    sns.heatmap(
        numeric_df.corr(),
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
    )
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "correlation_heatmap.png", dpi=150)
    plt.close()

    # Feature importance / coefficient chart.
    classifier = model.named_steps["classifier"]
    preprocessor = model.named_steps["preprocessor"]
    feature_names = preprocessor.get_feature_names_out()

    if hasattr(classifier, "feature_importances_"):
        importance = classifier.feature_importances_
        chart_title = "Random Forest Feature Importance"
    else:
        importance = abs(classifier.coef_[0])
        chart_title = "Logistic Regression Feature Importance (Absolute Coefficients)"

    importance_df = (
        pd.DataFrame({"feature": feature_names, "importance": importance})
        .sort_values("importance", ascending=False)
        .head(10)
    )

    plt.figure(figsize=(9, 6))
    sns.barplot(
        data=importance_df,
        x="importance",
        y="feature",
    )
    plt.title(chart_title)
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "feature_importance.png", dpi=150)
    plt.close()

    print("\nSaved visualizations:")
    print(f"- {OUTPUT_DIR / 'confusion_matrix.png'}")
    print(f"- {OUTPUT_DIR / 'correlation_heatmap.png'}")
    print(f"- {OUTPUT_DIR / 'feature_importance.png'}")


if __name__ == "__main__":
    evaluate_model()
