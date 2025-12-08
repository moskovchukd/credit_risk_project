import pandas as pd
from src.predict import load_best_model


# KLIENT O NISKIM RYZYKU
przykladowy_klient_nizkie_ryzyko = {
    'Attribute1': 'A14',    # Brak konta (często lepsze niż zadłużone)
    'Attribute2': 6,        # Bardzo krótki okres kredytu
    'Attribute3': 'A32',    # Dobre kredyty spłacane prawidłowo
    'Attribute4': 'A43',    # Radio/TV (niskie ryzyko)
    'Attribute5': 1000,     # Bardzo mała kwota kredytu
    'Attribute6': 'A65',    # Nieznane oszczędności (neutralne)
    'Attribute7': 'A75',    # 7+ lat zatrudnienia
    'Attribute8': 1,        # Bardzo niska rata jako % dochodu
    'Attribute9': 'A93',    # Mężczyzna kawaler
    'Attribute10': 'A101',  # Brak współdłużników
    'Attribute11': 4,       # 4 lata w obecnym mieszkaniu
    'Attribute12': 'A121',  # Posiada nieruchomość
    'Attribute13': 67,      # Starszy wiek (stabilny)
    'Attribute14': 'A143',  # Brak innych planów ratalnych
    'Attribute15': 'A152',  # Własne mieszkanie
    'Attribute16': 1,       # 1 kredyt w tym banku
    'Attribute17': 'A173',  # Wykwalifikowany pracownik
    'Attribute18': 1,       # 1 osoba na utrzymaniu
    'Attribute19': 'A192',  # Ma telefon
    'Attribute20': 'A201'   # Pracownik zagraniczny
}

# KLIENT O ŚREDNIM RYZYKU
przykladowy_klient_srednie_ryzyko = {
    'Attribute1': 'A12',    # 0-200 DM na koncie
    'Attribute2': 18,       # Średni okres kredytu
    'Attribute3': 'A34',    # Konto krytyczne/problemy
    'Attribute4': 'A43',    # Radio/TV
    'Attribute5': 3000,     # Średnia kwota kredytu
    'Attribute6': 'A61',    # Małe oszczędności <100 DM
    'Attribute7': 'A74',    # 4-7 lat zatrudnienia
    'Attribute8': 2,        # Średnia rata jako % dochodu
    'Attribute9': 'A93',    # Mężczyzna kawaler
    'Attribute10': 'A103',  # Poręczyciel
    'Attribute11': 3,       # 3 lata w obecnym mieszkaniu
    'Attribute12': 'A121',  # Posiada nieruchomość
    'Attribute13': 30,      # Średni wiek
    'Attribute14': 'A143',  # Brak innych planów ratalnych
    'Attribute15': 'A152',  # Własne mieszkanie
    'Attribute16': 2,       # 2 kredyty w tym banku
    'Attribute17': 'A173',  # Wykwalifikowany pracownik
    'Attribute18': 1,       # 1 osoba na utrzymaniu
    'Attribute19': 'A191',  # Brak telefonu
    'Attribute20': 'A201'   # Pracownik zagraniczny
}

# KLIENT O WYSOKIM RYZYKU
przykladowy_klient_wysokie_ryzyko = {
    'Attribute1': 'A11',    # Poniżej 0 DM (zadłużone konto)
    'Attribute2': 48,       # Bardzo długi okres kredytu
    'Attribute3': 'A34',    # Konto krytyczne/problemy
    'Attribute4': 'A42',    # Meble/wyposażenie
    'Attribute5': 12612,    # Bardzo duża kwota kredytu
    'Attribute6': 'A65',    # Brak oszczędności
    'Attribute7': 'A75',    # 7+ lat zatrudnienia (ale inne czynniki złe)
    'Attribute8': 4,        # Bardzo wysoka rata jako % dochodu
    'Attribute9': 'A93',    # Mężczyzna kawaler
    'Attribute10': 'A101',  # Brak współdłużników
    'Attribute11': 4,       # 4 lata w obecnym mieszkaniu
    'Attribute12': 'A124',  # Brak własności
    'Attribute13': 24,      # Młody wiek
    'Attribute14': 'A143',  # Brak innych planów ratalnych
    'Attribute15': 'A153',  # Mieszkanie za darmo
    'Attribute16': 2,       # 2 kredyty w tym banku
    'Attribute17': 'A174',  # Menedżer/samozatrudniony
    'Attribute18': 2,       # 2 osoby na utrzymaniu
    'Attribute19': 'A192',  # Ma telefon
    'Attribute20': 'A201'   # Pracownik zagraniczny
}


def wyswietl_profil_klienta(nazwa, dane):
    """Wyświetla szczegółowy profil klienta"""
    print("\n" + "-"*70)
    print(f"  📋 PROFIL KLIENTA")
    print("-"*70)
    
  
    nazwa_lower = nazwa.lower()
    
    if 'niskim' in nazwa_lower or 'niskie' in nazwa_lower:
        print("\nCharakterystyka (NISKIE RYZYKO):")
        print("  ✓ Bardzo krótki okres kredytu (6 miesięcy)")
        print("  ✓ Bardzo mała kwota kredytu (1000 DM)")
        print("  ✓ Długoletnie zatrudnienie (7+ lat)")
        print("  ✓ Bardzo niska rata (1% dochodu)")
        print("  ✓ Posiada nieruchomość")
        print("  ✓ Starszy, stabilny wiek (67 lat)")
        print("  ✓ Brak innych planów ratalnych")
        
    elif 'średnim' in nazwa_lower or 'srednie' in nazwa_lower:
        print("\nCharakterystyka (ŚREDNIE RYZYKO):")
        print("  ⚠ Średni okres kredytu (18 miesięcy)")
        print("  ⚠ Średnia kwota kredytu (3000 DM)")
        print("  ⚠ Historia kredytowa z problemami")
        print("  ⚠ Małe oszczędności (<100 DM)")
        print("  ⚠ Wymaga poręczyciela")
        print("  ⚠ Brak telefonu")
        print("  ✓ Posiada nieruchomość")
        print("  ✓ Stabilne zatrudnienie (4-7 lat)")
        
    else: 
        print("\nCharakterystyka (WYSOKIE RYZYKO):")
        print("  ✗ Bardzo długi okres kredytu (48 miesięcy)")
        print("  ✗ Bardzo duża kwota kredytu (12612 DM)")
        print("  ✗ Zadłużone konto (<0 DM)")
        print("  ✗ Konto krytyczne, problemy w przeszłości")
        print("  ✗ Brak oszczędności")
        print("  ✗ Bardzo wysoka rata (4% dochodu)")
        print("  ✗ Młody wiek (24 lata)")
        print("  ✗ Brak własności")
        print("  ✗ 2 osoby na utrzymaniu")


def test_predykcji(nazwa_klienta, dane_klienta):
    """Testuje predykcję dla danego klienta"""
    print("\n" + "="*70)
    print(f"  🔍 TESTOWANIE: {nazwa_klienta}")
    print("="*70)

    wyswietl_profil_klienta(nazwa_klienta, dane_klienta)

    print("\n📊 Dane klienta (wybrane atrybuty):")
    key_attributes = ['Attribute1', 'Attribute2', 'Attribute3', 'Attribute5', 
                      'Attribute6', 'Attribute7', 'Attribute8', 'Attribute13']
    for key in key_attributes:
        print(f"  {key}: {dane_klienta[key]}")
    print("  ...")

    print("\n🤖 Ładowanie modelu...")
    predictor = load_best_model('models')

    df = pd.DataFrame([dane_klienta])

    print("⚙️  Wykonywanie predykcji...")
    prediction = predictor.predict(df)

    if hasattr(predictor.model, 'predict_proba'):
        probabilities = predictor.predict_proba(df)
        n_classes = probabilities.shape[1]
    else:
        probabilities = None
        n_classes = 2

    print("\n" + "="*70)
    print("  📈 WYNIK PREDYKCJI")
    print("="*70)

    if n_classes == 2:
        if prediction[0] == 0:
            print("\n✅ DECYZJA: KREDYT ZATWIERDZONY")
            print("   Ryzyko: NISKIE")
        else:
            print("\n❌ DECYZJA: KREDYT ODRZUCONY")
            print("   Ryzyko: WYSOKIE")

        if probabilities is not None:
            print(f"\n📊 Prawdopodobieństwa:")
            print(f"  • Niskie ryzyko:  {probabilities[0][0]:.2%}")
            print(f"  • Wysokie ryzyko: {probabilities[0][1]:.2%}")
            print(f"\n🎯 Pewność decyzji: {probabilities.max():.2%}")

    elif n_classes == 3:
        risk_labels = {0: 'NISKIE', 1: 'ŚREDNIE', 2: 'WYSOKIE'}
        risk_symbols = {0: '✅', 1: '⚠️', 2: '❌'}
        risk_decisions = {
            0: 'KREDYT ZATWIERDZONY - Klient jest wiarygodny',
            1: 'WYMAGA DODATKOWEJ WERYFIKACJI - Analiza przypadku',
            2: 'KREDYT ODRZUCONY - Zbyt wysokie ryzyko'
        }

        pred = prediction[0]
        print(f"\n{risk_symbols[pred]} DECYZJA: {risk_decisions[pred]}")
        print(f"   Poziom ryzyka: {risk_labels[pred]}")

        if probabilities is not None:
            print(f"\n📊 Prawdopodobieństwa:")
            print(f"  • Niskie ryzyko:  {probabilities[0][0]:.2%}")
            print(f"  • Średnie ryzyko: {probabilities[0][1]:.2%}")
            print(f"  • Wysokie ryzyko: {probabilities[0][2]:.2%}")
            
            max_prob = probabilities.max()
            print(f"\n🎯 Pewność decyzji: {max_prob:.2%}")
            
            if max_prob > 0.8:
                print(f"   → Bardzo pewna decyzja")
            elif max_prob > 0.6:
                print(f"   → Umiarkowanie pewna decyzja")
            else:
                print(f"   → Niska pewność, zalecana dodatkowa weryfikacja")

    print("="*70)


def main():
    print("\n╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  DEMO: SYSTEM OCENY RYZYKA KREDYTOWEGO".center(68) + "║")
    print("║" + "  Przykłady predykcji dla trzech poziomów ryzyka".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")

    try:
      
        test_predykcji("KLIENT O NISKIM RYZYKU", przykladowy_klient_nizkie_ryzyko)
        
        input("\n⏸️  Naciśnij Enter, aby kontynuować do następnego klienta...")
        
        test_predykcji("KLIENT O ŚREDNIM RYZYKU", przykladowy_klient_srednie_ryzyko)
        
        input("\n⏸️  Naciśnij Enter, aby kontynuować do następnego klienta...")
        
        test_predykcji("KLIENT O WYSOKIM RYZYKU", przykladowy_klient_wysokie_ryzyko)

     
        print("\n" + "="*70)
        print("  📊 PODSUMOWANIE DEMO")
        print("="*70)
        print("\n✅ Demo zakończone pomyślnie!")
        print("\nPrzetestowano trzy profile klientów:")
        print("  1. ✅ Niskie ryzyko  - bardzo stabilny klient")
        print("  2. ⚠️  Średnie ryzyko - klient wymagający uwagi")
        print("  3. ❌ Wysokie ryzyko - klient z poważnymi problemami")
        
        print("\n💡 UWAGA:")
        print("  Jeśli model klasyfikuje średnie ryzyko jako wysokie,")
        print("  może to oznaczać, że:")
        print("  • Model był trenowany tylko na 2 klasach (good/bad)")
        print("  • Dane treningowe nie miały kategorii 'średnie ryzyko'")
        print("  • Model wymaga ponownego wytrenowania z 3 klasami")
        
        print("\n💡 Co dalej?")
        print("  • Aby przeprowadzić interaktywną ankietę:")
        print("    python interactive_survey.py")
        print("\n  • Aby przetworzyć plik CSV z wieloma klientami:")
        print("    python batch_survey.py klienci.csv")
        print("="*70 + "\n")

    except FileNotFoundError as e:
        print(f"\n❌ Błąd: Nie znaleziono plików modeli")
        print("\nUpewnij się, że wytrenowałeś modele:")
        print("  python run_train.py")
        
    except Exception as e:
        print(f"\n❌ Błąd: {e}")
        print("\nUpewnij się, że:")
        print("  1. Wytrenowałeś modele (python run_train.py)")
        print("  2. Folder 'models/' zawiera wytrenowane modele")
        print("  3. Wszystkie zależności są zainstalowane")


if __name__ == "__main__":
    main()