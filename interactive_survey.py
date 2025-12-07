"""
Interaktywna ankieta do oceny ryzyka kredytowego
Użytkownik wprowadza dane w formacie czytelnym dla człowieka (po polsku),
a system automatycznie konwertuje je do formatu wymaganego przez model
"""

import pandas as pd
from src.predict import load_best_model


# Mapowania z polskich odpowiedzi na kody używane przez model
ENCODINGS = {
    'Attribute1': {
        'pytanie': 'Status istniejącego konta czekowego:',
        'opcje': {
            '1': ('mniej niż 0 DM', 'A11'),
            '2': ('od 0 do 200 DM', 'A12'),
            '3': ('200 DM lub więcej / wypłaty przez co najmniej 1 rok', 'A13'),
            '4': ('brak konta czekowego', 'A14')
        }
    },
    'Attribute2': {
        'pytanie': 'Czas trwania kredytu (w miesiącach):',
        'typ': 'numeryczny'
    },
    'Attribute3': {
        'pytanie': 'Historia kredytowa:',
        'opcje': {
            '1': ('brak kredytów / wszystkie kredyty spłacone prawidłowo', 'A30'),
            '2': ('wszystkie kredyty w tym banku spłacone prawidłowo', 'A31'),
            '3': ('istniejące kredyty spłacane prawidłowo do tej pory', 'A32'),
            '4': ('opóźnienia w spłatach w przeszłości', 'A33'),
            '5': ('konto krytyczne / inne istniejące kredyty (nie w tym banku)', 'A34')
        }
    },
    'Attribute4': {
        'pytanie': 'Cel kredytu:',
        'opcje': {
            '1': ('samochód (nowy)', 'A40'),
            '2': ('samochód (używany)', 'A41'),
            '3': ('meble/wyposażenie', 'A42'),
            '4': ('radio/telewizja', 'A43'),
            '5': ('sprzęt AGD', 'A44'),
            '6': ('naprawy', 'A45'),
            '7': ('edukacja', 'A46'),
            '8': ('przekwalifikowanie', 'A48'),
            '9': ('biznes', 'A49'),
            '10': ('inne', 'A410')
        }
    },
    'Attribute5': {
        'pytanie': 'Kwota kredytu (w DM):',
        'typ': 'numeryczny'
    },
    'Attribute6': {
        'pytanie': 'Konto oszczędnościowe/obligacje:',
        'opcje': {
            '1': ('mniej niż 100 DM', 'A61'),
            '2': ('od 100 do 500 DM', 'A62'),
            '3': ('od 500 do 1000 DM', 'A63'),
            '4': ('1000 DM lub więcej', 'A64'),
            '5': ('nieznane / brak konta oszczędnościowego', 'A65')
        }
    },
    'Attribute7': {
        'pytanie': 'Obecne zatrudnienie od:',
        'opcje': {
            '1': ('bezrobotny', 'A71'),
            '2': ('mniej niż 1 rok', 'A72'),
            '3': ('od 1 do 4 lat', 'A73'),
            '4': ('od 4 do 7 lat', 'A74'),
            '5': ('7 lat lub więcej', 'A75')
        }
    },
    'Attribute8': {
        'pytanie': 'Rata w procentach dochodu rozporządzalnego:',
        'typ': 'numeryczny'
    },
    'Attribute9': {
        'pytanie': 'Status osobisty i płeć:',
        'opcje': {
            '1': ('mężczyzna : rozwiedziony/w separacji', 'A91'),
            '2': ('kobieta : rozwiedziona/w separacji/zamężna', 'A92'),
            '3': ('mężczyzna : kawaler', 'A93'),
            '4': ('mężczyzna : żonaty/wdowiec', 'A94'),
            '5': ('kobieta : panna', 'A95')
        }
    },
    'Attribute10': {
        'pytanie': 'Inni dłużnicy / poręczyciele:',
        'opcje': {
            '1': ('brak', 'A101'),
            '2': ('współwnioskodawca', 'A102'),
            '3': ('poręczyciel', 'A103')
        }
    },
    'Attribute11': {
        'pytanie': 'Obecne miejsce zamieszkania od (w latach):',
        'typ': 'numeryczny'
    },
    'Attribute12': {
        'pytanie': 'Własność:',
        'opcje': {
            '1': ('nieruchomość', 'A121'),
            '2': ('umowa oszczędnościowo-budowlana / ubezpieczenie na życie', 'A122'),
            '3': ('samochód lub inne (nie w atrybucie 6)', 'A123'),
            '4': ('nieznane / brak własności', 'A124')
        }
    },
    'Attribute13': {
        'pytanie': 'Wiek (w latach):',
        'typ': 'numeryczny'
    },
    'Attribute14': {
        'pytanie': 'Inne plany ratalne:',
        'opcje': {
            '1': ('bank', 'A141'),
            '2': ('sklepy', 'A142'),
            '3': ('brak', 'A143')
        }
    },
    'Attribute15': {
        'pytanie': 'Mieszkanie:',
        'opcje': {
            '1': ('wynajem', 'A151'),
            '2': ('własne', 'A152'),
            '3': ('za darmo', 'A153')
        }
    },
    'Attribute16': {
        'pytanie': 'Liczba istniejących kredytów w tym banku:',
        'typ': 'numeryczny'
    },
    'Attribute17': {
        'pytanie': 'Praca:',
        'opcje': {
            '1': ('bezrobotny / niewykwalifikowany - nierezydent', 'A171'),
            '2': ('niewykwalifikowany - rezydent', 'A172'),
            '3': ('wykwalifikowany pracownik / urzędnik', 'A173'),
            '4': ('menedżer / samozatrudniony / wysoko wykwalifikowany / oficer', 'A174')
        }
    },
    'Attribute18': {
        'pytanie': 'Liczba osób na utrzymaniu:',
        'typ': 'numeryczny'
    },
    'Attribute19': {
        'pytanie': 'Telefon:',
        'opcje': {
            '1': ('brak', 'A191'),
            '2': ('tak, zarejestrowany na nazwisko klienta', 'A192')
        }
    },
    'Attribute20': {
        'pytanie': 'Pracownik zagraniczny:',
        'opcje': {
            '1': ('tak', 'A201'),
            '2': ('nie', 'A202')
        }
    }
}


def wyswietl_opcje(opcje):
    """Wyświetla dostępne opcje dla użytkownika"""
    print()
    for key, (opis, _) in opcje.items():
        print(f"  {key}. {opis}")
    print()


def pobierz_odpowiedz_kategoryczna(atrybut_nazwa):
    """Pobiera odpowiedź użytkownika dla atrybutu kategorycznego"""
    config = ENCODINGS[atrybut_nazwa]
    print(f"\n{'='*60}")
    print(config['pytanie'])
    wyswietl_opcje(config['opcje'])

    while True:
        wybor = input("Wybierz numer opcji: ").strip()
        if wybor in config['opcje']:
            _, kod = config['opcje'][wybor]
            return kod
        else:
            print("❌ Nieprawidłowy wybór. Spróbuj ponownie.")


def pobierz_odpowiedz_numeryczna(atrybut_nazwa):
    """Pobiera odpowiedź użytkownika dla atrybutu numerycznego"""
    config = ENCODINGS[atrybut_nazwa]
    print(f"\n{'='*60}")
    print(config['pytanie'])

    while True:
        try:
            wartosc = input("Wprowadź wartość: ").strip()
            return int(wartosc)
        except ValueError:
            print("❌ Wprowadź prawidłową liczbę całkowitą.")


def przeprowadz_ankiete():
    """Przeprowadza interaktywną ankietę i zbiera dane od użytkownika"""
    print("\n" + "="*60)
    print("  ANKIETA OCENY RYZYKA KREDYTOWEGO")
    print("="*60)
    print("\nProszę odpowiedzieć na następujące pytania.")
    print("Twoje odpowiedzi zostaną użyte do oceny ryzyka kredytowego.\n")

    dane_klienta = {}

    # Przejdź przez wszystkie 20 atrybutów
    for i in range(1, 21):
        atrybut_nazwa = f'Attribute{i}'
        config = ENCODINGS[atrybut_nazwa]

        if config.get('typ') == 'numeryczny':
            dane_klienta[atrybut_nazwa] = pobierz_odpowiedz_numeryczna(atrybut_nazwa)
        else:
            dane_klienta[atrybut_nazwa] = pobierz_odpowiedz_kategoryczna(atrybut_nazwa)

    return dane_klienta


def wyswietl_podsumowanie(dane):
    """Wyświetla podsumowanie wprowadzonych danych"""
    print("\n" + "="*60)
    print("  PODSUMOWANIE WPROWADZONYCH DANYCH")
    print("="*60)

    for atrybut, wartosc in dane.items():
        config = ENCODINGS[atrybut]
        pytanie = config['pytanie']

        if config.get('typ') == 'numeryczny':
            print(f"\n{pytanie}")
            print(f"  → {wartosc}")
        else:
            # Znajdź opis dla kodu
            opis = None
            for key, (opis_txt, kod) in config['opcje'].items():
                if kod == wartosc:
                    opis = opis_txt
                    break
            print(f"\n{pytanie}")
            print(f"  → {opis}")


def wykonaj_predykcje(dane_klienta):
    """Wykonuje predykcję ryzyka kredytowego na podstawie danych klienta"""
    try:
        # Wczytaj najlepszy model
        print("\n" + "="*60)
        print("  ANALIZA RYZYKA KREDYTOWEGO")
        print("="*60)
        print("\nŁadowanie modelu...")

        predictor = load_best_model('models')

        # Przygotuj dane w formacie DataFrame
        df = pd.DataFrame([dane_klienta])

        # Wykonaj predykcję
        print("Wykonywanie predykcji...")
        prediction = predictor.predict(df)

        # Pobierz prawdopodobieństwa jeśli model je wspiera
        if hasattr(predictor.model, 'predict_proba'):
            probabilities = predictor.predict_proba(df)
            n_classes = probabilities.shape[1]
        else:
            probabilities = None
            n_classes = 2

        # Wyświetl wyniki
        print("\n" + "="*60)
        print("  WYNIK OCENY RYZYKA KREDYTOWEGO")
        print("="*60)

        if n_classes == 2:
            # Model binarny: 0 = dobre, 1 = złe
            if prediction[0] == 0:
                print("\n✅ WNIOSEK KREDYTOWY: ZATWIERDZONY")
                print("   Ryzyko: NISKIE")
                print("   Klient jest wiarygodny kredytowo.")
            else:
                print("\n❌ WNIOSEK KREDYTOWY: ODRZUCONY")
                print("   Ryzyko: WYSOKIE")
                print("   Klient stanowi wysokie ryzyko kredytowe.")

            if probabilities is not None:
                print(f"\nPrawdopodobieństwa:")
                print(f"  • Niskie ryzyko:  {probabilities[0][0]:.2%}")
                print(f"  • Wysokie ryzyko: {probabilities[0][1]:.2%}")
                print(f"\nPewność decyzji: {probabilities.max():.2%}")

        elif n_classes == 3:
            # Model 3-klasowy: 0 = niskie, 1 = średnie, 2 = wysokie
            risk_labels = {0: 'NISKIE', 1: 'ŚREDNIE', 2: 'WYSOKIE'}
            risk_symbols = {0: '✅', 1: '⚠️', 2: '❌'}
            risk_decision = {
                0: 'ZATWIERDZONY - Klient jest wiarygodny kredytowo.',
                1: 'WYMAGA DODATKOWEJ WERYFIKACJI - Klient wymaga dodatkowej analizy.',
                2: 'ODRZUCONY - Klient stanowi wysokie ryzyko kredytowe.'
            }

            pred = prediction[0]
            print(f"\n{risk_symbols[pred]} WNIOSEK KREDYTOWY: {risk_decision[pred].split('-')[0]}")
            print(f"   Ryzyko: {risk_labels[pred]}")
            print(f"   {risk_decision[pred].split('-')[1].strip()}")

            if probabilities is not None:
                print(f"\nPrawdopodobieństwa:")
                print(f"  • Niskie ryzyko:  {probabilities[0][0]:.2%}")
                print(f"  • Średnie ryzyko: {probabilities[0][1]:.2%}")
                print(f"  • Wysokie ryzyko: {probabilities[0][2]:.2%}")
                print(f"\nPewność decyzji: {probabilities.max():.2%}")

        print("\n" + "="*60)

        return prediction[0], probabilities

    except Exception as e:
        print(f"\n❌ Błąd podczas wykonywania predykcji: {e}")
        print("\nUpewnij się, że:")
        print("  1. Wytrenowałeś modele (uruchom: python run_train.py)")
        print("  2. Folder 'models/' zawiera wytrenowane modele")
        return None, None


def main():
    """Główna funkcja programu"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  SYSTEM OCENY RYZYKA KREDYTOWEGO".center(58) + "║")
    print("║" + "  Interaktywna ankieta klienta".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")

    # Przeprowadź ankietę
    dane_klienta = przeprowadz_ankiete()

    # Wyświetl podsumowanie
    wyswietl_podsumowanie(dane_klienta)

    # Zapytaj czy kontynuować
    print("\n" + "="*60)
    odpowiedz = input("\nCzy chcesz wykonać ocenę ryzyka kredytowego? (tak/nie): ").strip().lower()

    if odpowiedz in ['tak', 't', 'yes', 'y']:
        # Wykonaj predykcję
        wykonaj_predykcje(dane_klienta)
    else:
        print("\nAnulowano ocenę ryzyka kredytowego.")

    print("\nDziękujemy za skorzystanie z systemu!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
