"""
Przetwarzanie wsadowe - ocena ryzyka dla wielu klientów naraz
Wczytuje dane z pliku CSV i wykonuje predykcje dla wszystkich klientów
"""

import pandas as pd
from src.predict import load_best_model
import sys


def wyswietl_instrukcje():
    """Wyświetla instrukcje użycia"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║         PRZETWARZANIE WSADOWE - OCENA RYZYKA KREDYTOWEGO      ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

UŻYCIE:
  python batch_survey.py <plik_wejściowy.csv> [plik_wyjściowy.csv]

OPIS:
  Wczytuje dane wielu klientów z pliku CSV i wykonuje predykcje
  ryzyka kredytowego dla każdego z nich.

FORMAT PLIKU WEJŚCIOWEGO:
  Plik CSV powinien zawierać następujące kolumny:
  - Attribute1, Attribute2, ..., Attribute20

  Wartości powinny być w formacie kodów (A11, A12, etc.) lub
  wartości numeryczne dla atrybutów numerycznych.

PRZYKŁAD:
  python batch_survey.py klienci.csv wyniki.csv

UWAGI:
  - Jeśli nie podasz pliku wyjściowego, domyślnie zostanie użyta
    nazwa: <plik_wejściowy>_predictions.csv
  - Wyniki zawierają wszystkie dane wejściowe oraz predykcje
  - Model automatycznie wybiera najlepszy wytrenowany model

════════════════════════════════════════════════════════════════
""")


def przetwarzaj_plik(plik_wejsciowy, plik_wyjsciowy=None):
    """
    Przetwarza plik CSV z danymi klientów i generuje predykcje

    Args:
        plik_wejsciowy: Ścieżka do pliku CSV z danymi klientów
        plik_wyjsciowy: Opcjonalna ścieżka do pliku wyjściowego
    """
    print("\n" + "="*70)
    print("  ROZPOCZĘCIE PRZETWARZANIA WSADOWEGO")
    print("="*70)

    # Domyślna nazwa pliku wyjściowego
    if plik_wyjsciowy is None:
        plik_wyjsciowy = plik_wejsciowy.replace('.csv', '_predictions.csv')

    try:
        # Wczytaj dane
        print(f"\n📂 Wczytywanie danych z: {plik_wejsciowy}")
        dane = pd.read_csv(plik_wejsciowy)
        liczba_klientow = len(dane)
        print(f"✓ Wczytano {liczba_klientow} klientów")

        # Sprawdź wymagane kolumny
        wymagane_kolumny = [f'Attribute{i}' for i in range(1, 21)]
        brakujace_kolumny = [col for col in wymagane_kolumny if col not in dane.columns]

        if brakujace_kolumny:
            print(f"\n❌ BŁĄD: Brakujące kolumny w pliku:")
            for col in brakujace_kolumny:
                print(f"   - {col}")
            print("\nUpewnij się, że plik zawiera wszystkie 20 atrybutów.")
            return False

        print("✓ Wszystkie wymagane kolumny są obecne")

        # Wyświetl przykład danych
        print("\n📊 Przykładowy rekord (pierwsze 5 kolumn):")
        print(dane.iloc[0, :5].to_string())

        # Wczytaj model
        print("\n🤖 Ładowanie modelu...")
        predictor = load_best_model('models')

        # Wykonaj predykcje
        print(f"\n⚙️  Wykonywanie predykcji dla {liczba_klientow} klientów...")
        wyniki = predictor.predict_with_details(dane)

        # Dodaj numery klientów
        wyniki.insert(0, 'ID_Klienta', range(1, len(wyniki) + 1))

        # Zapisz wyniki
        print(f"\n💾 Zapisywanie wyników do: {plik_wyjsciowy}")
        wyniki.to_csv(plik_wyjsciowy, index=False)
        print("✓ Wyniki zapisane pomyślnie")

        # Podsumowanie
        print("\n" + "="*70)
        print("  PODSUMOWANIE WYNIKÓW")
        print("="*70)

        if 'Risk_Label' in wyniki.columns:
            print("\nRozkład decyzji kredytowych:")
            rozklad = wyniki['Risk_Label'].value_counts()
            for kategoria, liczba in rozklad.items():
                procent = (liczba / liczba_klientow) * 100
                print(f"  • {kategoria.upper()}: {liczba} ({procent:.1f}%)")

        if 'Confidence' in wyniki.columns:
            srednia_pewnosc = wyniki['Confidence'].mean()
            print(f"\nŚrednia pewność decyzji: {srednia_pewnosc:.2%}")

        print("\n" + "="*70)
        print(f"✅ Przetworzono {liczba_klientow} klientów pomyślnie!")
        print(f"📄 Plik wynikowy: {plik_wyjsciowy}")
        print("="*70 + "\n")

        return True

    except FileNotFoundError:
        print(f"\n❌ BŁĄD: Nie znaleziono pliku: {plik_wejsciowy}")
        print("Upewnij się, że ścieżka jest prawidłowa.")
        return False

    except Exception as e:
        print(f"\n❌ BŁĄD podczas przetwarzania: {e}")
        print("\nSprawdź:")
        print("  1. Format pliku CSV (prawidłowe separatory, kodowanie UTF-8)")
        print("  2. Poprawność danych w kolumnach")
        print("  3. Czy modele zostały wytrenowane (python run_train.py)")
        return False


def stworz_przykladowy_plik():
    """Tworzy przykładowy plik CSV do testowania"""
    print("\n📝 Tworzenie przykładowego pliku...")

    przykladowe_dane = [
        {
            'Attribute1': 'A13', 'Attribute2': 24, 'Attribute3': 'A32',
            'Attribute4': 'A43', 'Attribute5': 5000, 'Attribute6': 'A63',
            'Attribute7': 'A75', 'Attribute8': 2, 'Attribute9': 'A93',
            'Attribute10': 'A101', 'Attribute11': 4, 'Attribute12': 'A121',
            'Attribute13': 35, 'Attribute14': 'A143', 'Attribute15': 'A152',
            'Attribute16': 1, 'Attribute17': 'A173', 'Attribute18': 1,
            'Attribute19': 'A192', 'Attribute20': 'A202'
        },
        {
            'Attribute1': 'A12', 'Attribute2': 36, 'Attribute3': 'A32',
            'Attribute4': 'A42', 'Attribute5': 8000, 'Attribute6': 'A62',
            'Attribute7': 'A73', 'Attribute8': 3, 'Attribute9': 'A94',
            'Attribute10': 'A101', 'Attribute11': 3, 'Attribute12': 'A122',
            'Attribute13': 40, 'Attribute14': 'A143', 'Attribute15': 'A152',
            'Attribute16': 1, 'Attribute17': 'A173', 'Attribute18': 2,
            'Attribute19': 'A192', 'Attribute20': 'A202'
        },
        {
            'Attribute1': 'A11', 'Attribute2': 48, 'Attribute3': 'A34',
            'Attribute4': 'A49', 'Attribute5': 15000, 'Attribute6': 'A65',
            'Attribute7': 'A72', 'Attribute8': 4, 'Attribute9': 'A93',
            'Attribute10': 'A101', 'Attribute11': 2, 'Attribute12': 'A124',
            'Attribute13': 28, 'Attribute14': 'A141', 'Attribute15': 'A151',
            'Attribute16': 2, 'Attribute17': 'A172', 'Attribute18': 1,
            'Attribute19': 'A191', 'Attribute20': 'A201'
        }
    ]

    df = pd.DataFrame(przykladowe_dane)
    nazwa_pliku = 'przykladowi_klienci.csv'
    df.to_csv(nazwa_pliku, index=False)

    print(f"✓ Utworzono plik: {nazwa_pliku}")
    print(f"  Zawiera {len(przykladowe_dane)} przykładowych klientów")
    print(f"\nMożesz go teraz przetworzyć:")
    print(f"  python batch_survey.py {nazwa_pliku}")


def main():
    """Główna funkcja programu"""

    # Sprawdź argumenty
    if len(sys.argv) < 2:
        wyswietl_instrukcje()

        # Zapytaj czy stworzyć przykładowy plik (tylko w trybie interaktywnym)
        try:
            print("\nCzy chcesz stworzyć przykładowy plik do testowania?")
            odpowiedz = input("(tak/nie): ").strip().lower()

            if odpowiedz in ['tak', 't', 'yes', 'y']:
                stworz_przykladowy_plik()
        except (EOFError, KeyboardInterrupt):
            print("\n\nUżycie: python batch_survey.py <plik_wejściowy.csv> [plik_wyjściowy.csv]")

        return

    # Pobierz argumenty
    plik_wejsciowy = sys.argv[1]
    plik_wyjsciowy = sys.argv[2] if len(sys.argv) > 2 else None

    # Przetwórz plik
    sukces = przetwarzaj_plik(plik_wejsciowy, plik_wyjsciowy)

    # Kod wyjścia
    sys.exit(0 if sukces else 1)


if __name__ == "__main__":
    main()
