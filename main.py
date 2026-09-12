from database_setup import setup_database
from train_model import train_models
from evaluate_visualize import evaluate_model


def main():
    print("=" * 60)
    print("STUDENT ACADEMIC PERFORMANCE & DROPOUT RISK PIPELINE")
    print("=" * 60)

    print("\n[1/3] Setting up SQLite database...")
    setup_database()

    print("\n[2/3] Training classification models...")
    train_models()

    print("\n[3/3] Evaluating model and generating visualizations...")
    evaluate_model()

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
