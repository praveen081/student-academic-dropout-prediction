# Student Academic Performance and Dropout Risk Prediction

Intermediate-level Python + SQLite + Machine Learning mini-project.

## Features
- 500 reproducible mock student records
- SQLite database using `sqlite3`
- SQL-to-Pandas data extraction
- Missing-value imputation
- One-hot encoding for parental education
- StandardScaler for numeric features
- Logistic Regression
- Random Forest Classifier
- Automatic model selection
- Accuracy, Precision, Recall and Confusion Matrix
- Correlation heatmap
- Feature-importance/coefficient chart

## Project Structure

```text
student_academic_dropout_prediction/
├── database_setup.py
├── data_preprocessing.py
├── train_model.py
├── evaluate_visualize.py
├── main.py
├── requirements.txt
├── README.md
├── students.db              # generated after running
├── models/
│   ├── best_model.joblib    # generated after training
│   └── test_data.joblib     # generated after training
└── outputs/
    ├── confusion_matrix.png
    ├── correlation_heatmap.png
    └── feature_importance.png
```

## Run in VS Code

Open the project folder in VS Code, then run:

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the entire pipeline:

```bash
python main.py
```

You can also run each stage separately:

```bash
python database_setup.py
python data_preprocessing.py
python train_model.py
python evaluate_visualize.py
```

## Target definition

`passed_status` is encoded as:
- `1` = Safe
- `0` = At Risk

The synthetic target is generated from study hours, attendance, previous GPA, parental education and random variation. It is intended for learning purposes, not real-world student-risk decisions.

## Important design choice

The preprocessing object is kept inside the scikit-learn Pipeline. This prevents data leakage because imputation, encoding and scaling are fitted using the training data when the model is trained.

The test set is saved by `train_model.py` so `evaluate_visualize.py` evaluates exactly the same 20% holdout set used during model comparison.
