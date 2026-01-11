"""
Train Logistic Regression model for credit risk assessment.
This script trains a single optimized model and generates visualizations.
"""
from src.preprocessing import prepare_data_from_ucimlrepo
from src.model_training import train_logistic_regression
from src.evaluation import save_all_visualizations
import pandas as pd


def main():
    print("\n" + "="*60)
    print("  TRENING MODELU OCENY RYZYKA KREDYTOWEGO")
    print("  Model: Logistic Regression")
    print("="*60 + "\n")

    # Prepare data
    print("Przygotowanie danych...")
    X, y, preprocessor = prepare_data_from_ucimlrepo()
    df = pd.concat([X, y], axis=1)

    # Train model
    print("\n" + "-"*60)
    results, X_test_trans, y_test = train_logistic_regression(
        X, y, preprocessor, output_dir='models'
    )
    print("-"*60)

    # Display results
    print('\n✓ Trening zakończony pomyślnie!')
    for model_name, model_info in results.items():
        print(f'   {model_name}: {model_info["accuracy"]:.4f}')

    # Generate visualizations
    print('\n' + '='*60)
    print("Generowanie wizualizacji...")
    save_all_visualizations(results, X_test_trans, y_test, df, output_dir='visualizations')
    print('='*60)

    print("\n✓ Wszystko gotowe!")
    print("  Model: models/LogisticRegression.pkl")
    print("  Wizualizacje: visualizations/\n")


if __name__ == '__main__':
    main()
