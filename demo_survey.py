"""
Demo skryptu interaktywnej ankiety
Pokazuje przykład użycia z wstępnie wypełnionymi danymi
"""

import pandas as pd
from src.predict import load_best_model


# Przykładowy klient 1: Niskie ryzyko
przykladowy_klient_nizkie_ryzyko = {
    'Attribute1': 'A13',  # 200 DM lub więcej na koncie
    'Attribute2': 12,     # 12 miesięcy
    'Attribute3': 'A32',  # Istniejące kredyty spłacane prawidłowo
    'Attribute4': 'A43',  # Radio/telewizja
    'Attribute5': 2000,   # 2000 DM
    'Attribute6': 'A63',  # 500-1000 DM oszczędności
    'Attribute7': 'A75',  # 7+ lat zatrudnienia
    'Attribute8': 2,      # 2% dochodu na ratę
    'Attribute9': 'A93',  # Mężczyzna kawaler
    'Attribute10': 'A101', # Brak innych dłużników
    'Attribute11': 4,     # 4 lata w obecnym miejscu
    'Attribute12': 'A121', # Nieruchomość
    'Attribute13': 35,    # 35 lat
    'Attribute14': 'A143', # Brak innych planów ratalnych
    'Attribute15': 'A152', # Własne mieszkanie
    'Attribute16': 1,     # 1 kredyt w banku
    'Attribute17': 'A173', # Wykwalifikowany pracownik
    'Attribute18': 1,     # 1 osoba na utrzymaniu
    'Attribute19': 'A192', # Ma telefon
    'Attribute20': 'A202'  # Nie jest pracownikiem zagranicznym
}

# Przykładowy klient 2: Wysokie ryzyko
przykladowy_klient_wysokie_ryzyko = {
    'Attribute1': 'A11',  # Mniej niż 0 DM na koncie
    'Attribute2': 48,     # 48 miesięcy (długi okres)
    'Attribute3': 'A34',  # Konto krytyczne
    'Attribute4': 'A42',  # Meble
    'Attribute5': 15000,  # 15000 DM (duża kwota)
    'Attribute6': 'A65',  # Brak oszczędności
    'Attribute7': 'A71',  # Bezrobotny
    'Attribute8': 4,      # 4% dochodu na ratę
    'Attribute9': 'A93',  # Mężczyzna kawaler
    'Attribute10': 'A101', # Brak innych dłużników
    'Attribute11': 1,     # 1 rok w obecnym miejscu
    'Attribute12': 'A124', # Brak własności
    'Attribute13': 22,    # 22 lata (młody)
    'Attribute14': 'A141', # Inne plany ratalne w banku
    'Attribute15': 'A151', # Wynajem
    'Attribute16': 2,     # 2 kredyty w banku
    'Attribute17': 'A172', # Niewykwalifikowany
    'Attribute18': 2,     # 2 osoby na utrzymaniu
    'Attribute19': 'A191', # Brak telefonu
    'Attribute20': 'A201'  # Pracownik zagraniczny
}


def test_predykcji(nazwa_klienta, dane_klienta):
    """Testuje predykcję dla danego klienta"""
    print("\n" + "="*70)
    print(f"  TESTOWANIE: {nazwa_klienta}")
    print("="*70)

    # Wyświetl dane klienta
    print("\nDane klienta:")
    for key, value in dane_klienta.items():
        print(f"  {key}: {value}")

    # Wczytaj model
    print("\nŁadowanie modelu...")
    predictor = load_best_model('models')

    # Przygotuj dane
    df = pd.DataFrame([dane_klienta])

    # Wykonaj predykcję
    print("Wykonywanie predykcji...")
    prediction = predictor.predict(df)

    # Pobierz prawdopodobieństwa
    if hasattr(predictor.model, 'predict_proba'):
        probabilities = predictor.predict_proba(df)
        n_classes = probabilities.shape[1]
    else:
        probabilities = None
        n_classes = 2

    # Wyświetl wyniki
    print("\n" + "="*70)
    print("  WYNIK PREDYKCJI")
    print("="*70)

    if n_classes == 2:
        if prediction[0] == 0:
            print("\n✅ DECYZJA: KREDYT ZATWIERDZONY")
            print("   Ryzyko: NISKIE")
        else:
            print("\n❌ DECYZJA: KREDYT ODRZUCONY")
            print("   Ryzyko: WYSOKIE")

        if probabilities is not None:
            print(f"\nPrawdopodobieństwa:")
            print(f"  • Niskie ryzyko:  {probabilities[0][0]:.2%}")
            print(f"  • Wysokie ryzyko: {probabilities[0][1]:.2%}")
            print(f"\nPewność: {probabilities.max():.2%}")

    elif n_classes == 3:
        risk_labels = {0: 'NISKIE', 1: 'ŚREDNIE', 2: 'WYSOKIE'}
        risk_symbols = {0: '✅', 1: '⚠️', 2: '❌'}

        pred = prediction[0]
        print(f"\n{risk_symbols[pred]} Ryzyko: {risk_labels[pred]}")

        if probabilities is not None:
            print(f"\nPrawdopodobieństwa:")
            print(f"  • Niskie ryzyko:  {probabilities[0][0]:.2%}")
            print(f"  • Średnie ryzyko: {probabilities[0][1]:.2%}")
            print(f"  • Wysokie ryzyko: {probabilities[0][2]:.2%}")
            print(f"\nPewność: {probabilities.max():.2%}")

    print("="*70)


def main():
    print("\n╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  DEMO: SYSTEM OCENY RYZYKA KREDYTOWEGO".center(68) + "║")
    print("║" + "  Przykłady predykcji dla różnych profili klientów".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")

    try:
        # Test 1: Klient o niskim ryzyku
        test_predykcji("KLIENT O NISKIM RYZYKU", przykladowy_klient_nizkie_ryzyko)

        # Test 2: Klient o wysokim ryzyku
        test_predykcji("KLIENT O WYSOKIM RYZYKU", przykladowy_klient_wysokie_ryzyko)

        print("\n" + "="*70)
        print("  PODSUMOWANIE")
        print("="*70)
        print("\nDemo zakończone pomyślnie!")
        print("\nAby przeprowadzić interaktywną ankietę, uruchom:")
        print("  python interactive_survey.py")
        print("="*70 + "\n")

    except Exception as e:
        print(f"\n❌ Błąd: {e}")
        print("\nUpewnij się, że wytrenowałeś modele:")
        print("  python run_train.py")


if __name__ == "__main__":
    main()
