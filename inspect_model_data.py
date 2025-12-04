"""
Skrypt do inspekcji struktury danych i modelu
"""

import pandas as pd
from src.preprocessing import prepare_data_from_ucimlrepo
from src.predict import load_best_model

print("=" * 70)
print("INSPEKCJA STRUKTURY DANYCH I MODELU")
print("=" * 70)

# Pobierz dane z UCI
print("\n1. Pobieranie danych z UCI ML Repository...")
X, y, preprocessor = prepare_data_from_ucimlrepo()

print(f"\n2. Struktura danych:")
print(f"   Liczba próbek: {len(X)}")
print(f"   Liczba cech: {len(X.columns)}")
print(f"\n3. Nazwy kolumn:")
print(f"   {list(X.columns)}")

print(f"\n4. Pierwsze 3 wiersze danych:")
print(X.head(3))

print(f"\n5. Typy danych:")
print(X.dtypes)

print(f"\n6. Rozkład klas ryzyka:")
risk_counts = y.value_counts().sort_index()
print(risk_counts)
print(f"\nLiczba klas: {len(risk_counts)}")

if len(risk_counts) == 2:
    print("Model: BINARNY (dobre ryzyko vs. złe ryzyko)")
    print("  Klasa 0 = Dobre ryzyko (low risk)")
    print("  Klasa 1 = Złe ryzyko (bad risk)")
elif len(risk_counts) == 3:
    print("Model: WIELOKLASOWY (niskie, średnie, wysokie ryzyko)")
    print("  Klasa 0 = Niskie ryzyko")
    print("  Klasa 1 = Średnie ryzyko")
    print("  Klasa 2 = Wysokie ryzyko")

# Wczytaj model
print("\n7. Informacje o wytrenowanym modelu:")
predictor = load_best_model('models')

print(f"\n8. Typ modelu: {type(predictor.model).__name__}")
print(f"   Liczba klas w modelu: {len(predictor.model.classes_)}")
print(f"   Klasy: {predictor.model.classes_}")

# Spróbuj przewidzieć dla pierwszego wiersza
print("\n9. Test przewidywania dla pierwszej próbki:")
sample = X.iloc[0:1]
prediction = predictor.predict(sample)
print(f"   Dane wejściowe (pierwsze 5 kolumn): {dict(sample.iloc[0, :5])}")
print(f"   Przewidziana klasa: {prediction[0]}")
print(f"   Rzeczywista klasa: {y.iloc[0]}")

if hasattr(predictor.model, 'predict_proba'):
    proba = predictor.predict_proba(sample)
    print(f"   Prawdopodobieństwa: {proba[0]}")

print("\n" + "=" * 70)
print("UTWORZENIE SZABLONU PLIKU CSV DLA NOWYCH DANYCH")
print("=" * 70)

# Utwórz szablon CSV z przykładowymi danymi
template = X.iloc[0:3].copy()
template.to_csv('new_customers.csv', index=False)
print("\n✓ Utworzono plik: template_new_customers.csv")
print("  Użyj tego pliku jako szablonu dla nowych danych.")
print("  Wypełnij go danymi nowych klientów zachowując nazwy i kolejność kolumn.")

print("\n" + "=" * 70)
print("JAK UŻYWAĆ MODELU Z NOWYMI DANYMI")
print("=" * 70)
print("""
1. Przygotuj plik CSV z danymi klientów:
   - Użyj template_new_customers.csv jako wzór
   - Kolumny muszą mieć DOKŁADNIE takie same nazwy
   - Możesz usunąć przykładowe wiersze i dodać własne dane

2. Wczytaj i przewiduj:
   
   from predict import load_best_model
   import pandas as pd
   
   # Wczytaj model
   predictor = load_best_model('models')
   
   # Wczytaj dane nowych klientów
   new_data = pd.read_csv('your_new_customers.csv')
   
   # Wykonaj przewidywania
   results = predictor.predict_with_details(new_data)
   
   # Zapisz wyniki
   results.to_csv('predictions.csv', index=False)
   
3. Lub użyj przykładowego skryptu:
   python example_usage.py
""")

print("=" * 70)