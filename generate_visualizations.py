"""
Skrypt do generowania wizualizacji na podstawie wytrenowanych modeli.
Użyj tego skryptu jeśli chcesz ponownie wygenerować wizualizacje bez ponownego treningu.
"""

import joblib
import pandas as pd
from src.evaluation import save_all_visualizations
from src.preprocessing import prepare_data_from_ucimlrepo
import os


def main():
    # Sprawdź czy modele istnieją
    if not os.path.exists('models/results_summary.pkl'):
        print("Błąd: Nie znaleziono wytrenowanych modeli!")
        print("Najpierw uruchom: python run_train.py")
        return

    print("Ładowanie wyników treningu...")
    results = joblib.load('models/results_summary.pkl')
    test_data = joblib.load('models/test_data.pkl')

    X_test_trans = test_data['X_test_trans']
    y_test = test_data['y_test']

    # Załaduj dane źródłowe
    print("Ładowanie danych źródłowych...")
    X, y, _ = prepare_data_from_ucimlrepo()
    df = pd.concat([X, y], axis=1)

    # Generuj wizualizacje
    print('\n' + '='*50)
    save_all_visualizations(results, X_test_trans, y_test, df, output_dir='visualizations')
    print('='*50)


if __name__ == '__main__':
    main()
