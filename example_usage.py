"""
Przykłady użycia modelu do przewidywania ryzyka kredytowego
"""

import pandas as pd
from src.predict import CreditRiskPredictor, load_best_model, compare_models_predictions
from src.preprocessing import prepare_data_from_ucimlrepo


print("=" * 50)
print("METODA 1: Automatyczny wybór najlepszego modelu")
print("=" * 50)

predictor = load_best_model('models')

print("\nPobieranie informacji o kolumnach z datasetu...")
X_sample, y_sample, _ = prepare_data_from_ucimlrepo()
print(f"Kolumny w datasecie: {list(X_sample.columns)}")
print(f"Liczba kolumn: {len(X_sample.columns)}")


print("\n" + "=" * 50)
print("METODA 2: Wczytaj konkretny model")
print("=" * 50)

predictor = CreditRiskPredictor('models/LogisticRegression.pkl')

print("\n" + "=" * 50)
print("PRZYKŁAD 1: Pojedyncze przewidywanie")
print("=" * 50)

sample_customer = X_sample.iloc[0:1].copy()  # Pierwszy wiersz jako DataFrame
print("\nPrzykładowe dane klienta (pierwsze 5 kolumn):")
print(sample_customer.iloc[:, :5])

prediction = predictor.predict(sample_customer)
print(f"\nPrzewidywane ryzyko: {prediction[0]}")

risk_mapping = {0: 'Niskie', 1: 'Średnie', 2: 'Wysokie'}
print(f"Interpretacja: Ryzyko {risk_mapping.get(prediction[0], prediction[0])}")


print("\n" + "=" * 50)
print("PRZYKŁAD 2: Przewidywanie z prawdopodobieństwami")
print("=" * 50)

if hasattr(predictor.model, 'predict_proba'):
    probabilities = predictor.predict_proba(sample_customer)
    n_classes = probabilities.shape[1]
    
    print(f"\nLiczba klas w modelu: {n_classes}")
    print(f"Prawdopodobieństwa:")
    
    if n_classes == 2:
        print(f"  Niskie ryzyko (klasa 0): {probabilities[0][0]:.2%}")
        print(f"  Wysokie ryzyko (klasa 1):   {probabilities[0][1]:.2%}")
    elif n_classes == 3:
        print(f"  Niskie ryzyko:  {probabilities[0][0]:.2%}")
        print(f"  Średnie ryzyko: {probabilities[0][1]:.2%}")
        print(f"  Wysokie ryzyko: {probabilities[0][2]:.2%}")
    else:
        for i in range(n_classes):
            print(f"  Klasa {i}: {probabilities[0][i]:.2%}")


print("\n" + "=" * 50)
print("PRZYKŁAD 3: Przewidywanie dla wielu klientów")
print("=" * 50)

customers_data = X_sample.iloc[0:5].copy()  # Pierwsze 5 klientów

results = predictor.predict_with_details(customers_data)
print("\nWyniki przewidywań (pierwsze 5 kolumn + przewidywania):")
display_cols = list(results.columns[:3]) + ['Risk_Label']
if 'Confidence' in results.columns:
    display_cols.append('Confidence')
print(results[display_cols])


print("\n" + "=" * 50)
print("PRZYKŁAD 4: Przewidywanie z pliku CSV")
print("=" * 50)

try:
    new_customers = pd.read_csv('new_customers.csv')
    
    predictions = predictor.predict_with_details(new_customers)
    
    predictions.to_csv('predictions_output.csv', index=False)
    print(f"✓ Przewidziano ryzyko dla {len(predictions)} klientów")
    print(f"✓ Wyniki zapisano do: predictions_output.csv")
    
    print("\nPodsumowanie przewidywań:")
    print(predictions['Risk_Label'].value_counts())
    
except FileNotFoundError:
    print("Plik 'new_customers.csv' nie został znaleziony")
    print("Utwórz plik CSV z danymi klientów aby wykonać przewidywania")


print("\n" + "=" * 50)
print("PRZYKŁAD 5: Porównanie wszystkich modeli")
print("=" * 50)

try:
    comparison = compare_models_predictions(customers_data, 'models')
    print("\nPorównanie przewidywań różnych modeli:")
    print(comparison)
    
    agreement = (comparison.iloc[:, :-1].nunique(axis=1) == 1).sum()
    total = len(comparison)
    print(f"\nZgodność modeli: {agreement}/{total} przypadków ({agreement/total:.1%})")
    
except Exception as e:
    print(f"Błąd podczas porównywania modeli: {e}")


print("\n" + "=" * 50)
print("PRZYKŁAD 6: Eksport do Excel")
print("=" * 50)

try:
    results_detailed = predictor.predict_with_details(customers_data)
    
    def get_recommendation(row):
        n_classes = len(predictor.model.classes_)
        
        if n_classes == 2:
            if row['Risk_Label'] == 'good':
                return 'Zatwierdzić kredyt'
            else:
                return 'Odrzucić / wysokie ryzyko'
        else:
            if row['Risk_Label'] == 'low':
                return 'Zatwierdzić kredyt'
            elif row['Risk_Label'] == 'medium':
                return 'Wymaga dodatkowej weryfikacji'
            else:
                return 'Odrzucić / wysokie ryzyko'
    
    results_detailed['Rekomendacja'] = results_detailed.apply(get_recommendation, axis=1)
    
    results_detailed.to_excel('credit_risk_report.xlsx', index=False)
    print("✓ Raport zapisany do: credit_risk_report.xlsx")
    
except Exception as e:
    print(f"Uwaga: {e}")
    print("Zainstaluj openpyxl: pip install openpyxl")


print("\n" + "=" * 50)
print("Zakończono wszystkie przykłady!")
print("=" * 50)