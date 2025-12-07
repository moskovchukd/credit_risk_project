# Instrukcja użycia interaktywnej ankiety

## Przegląd

Interaktywna ankieta kredytowa to narzędzie umożliwiające ocenę ryzyka kredytowego klientów poprzez proste pytania w języku polskim. System automatycznie konwertuje odpowiedzi do formatu wymaganego przez model i natychmiast zwraca decyzję kredytową.

## Wymagania

1. Wytrenowane modele w folderze `models/`
   - Jeśli nie masz modeli, uruchom: `python run_train.py`
2. Zainstalowane zależności: `pip install -r requirements.txt`
3. Aktywne środowisko wirtualne (venv)

## Uruchomienie

### Opcja 1: Interaktywna ankieta (dla użytkowników końcowych)

```bash
python interactive_survey.py
```

System poprowadzi Cię przez serię 20 pytań, zbierając informacje o kliencie. Po zakończeniu ankiety otrzymasz:
- Podsumowanie wprowadzonych danych
- Decyzję kredytową (zatwierdzony/odrzucony)
- Poziom ryzyka
- Prawdopodobieństwa dla każdej kategorii
- Pewność decyzji

### Opcja 2: Demo z przykładami (dla testowania)

```bash
python demo_survey.py
```

Uruchamia predykcje dla dwóch predefiniowanych profili klientów:
- Klient o niskim ryzyku
- Klient o wysokim ryzyku

## Struktura ankiety

Ankieta składa się z 20 pytań podzielonych na następujące kategorie:

### 1. Informacje finansowe (6 pytań)
- Status konta czekowego
- Kwota kredytu
- Konto oszczędnościowe
- Czas trwania kredytu
- Rata jako procent dochodu
- Liczba istniejących kredytów

### 2. Historia kredytowa (2 pytania)
- Historia kredytowa
- Inne plany ratalne

### 3. Zatrudnienie i dochód (2 pytania)
- Czas zatrudnienia
- Rodzaj pracy

### 4. Informacje osobiste (5 pytań)
- Wiek
- Status osobisty i płeć
- Liczba osób na utrzymaniu
- Czas zamieszkania w obecnym miejscu
- Status pracownika zagranicznego

### 5. Własność i zabezpieczenia (3 pytania)
- Typ mieszkania
- Własność (nieruchomość, samochód, itp.)
- Inni dłużnicy/poręczyciele

### 6. Inne (2 pytania)
- Cel kredytu
- Posiadanie telefonu

## Przykład użycia

### Krok 1: Uruchomienie
```bash
python interactive_survey.py
```

### Krok 2: Odpowiadanie na pytania

Dla każdego pytania:
1. Przeczytaj pytanie
2. Zobacz dostępne opcje
3. Wprowadź numer wybranej opcji (dla pytań kategorycznych) lub wartość liczbową (dla pytań numerycznych)

Przykład:
```
============================================================
Status istniejącego konta czekowego:

  1. mniej niż 0 DM
  2. od 0 do 200 DM
  3. 200 DM lub więcej / wypłaty przez co najmniej 1 rok
  4. brak konta czekowego

Wybierz numer opcji: 3
```

### Krok 3: Weryfikacja danych

Po odpowiedzeniu na wszystkie pytania, system wyświetli podsumowanie:
```
============================================================
  PODSUMOWANIE WPROWADZONYCH DANYCH
============================================================

Status istniejącego konta czekowego:
  → 200 DM lub więcej / wypłaty przez co najmniej 1 rok

Czas trwania kredytu (w miesiącach):
  → 24

[...]
```

### Krok 4: Potwierdzenie i wynik

```
Czy chcesz wykonać ocenę ryzyka kredytowego? (tak/nie): tak
```

System zwróci decyzję:
```
============================================================
  WYNIK OCENY RYZYKA KREDYTOWEGO
============================================================

✅ WNIOSEK KREDYTOWY: ZATWIERDZONY
   Ryzyko: NISKIE
   Klient jest wiarygodny kredytowo.

Prawdopodobieństwa:
  • Niskie ryzyko:  91.00%
  • Wysokie ryzyko: 9.00%

Pewność decyzji: 91.00%
============================================================
```

## Interpretacja wyników

### Model binarny (2 klasy):
- **Klasa 0 (Niskie ryzyko)**: Kredyt zatwierdzony - klient wiarygodny
- **Klasa 1 (Wysokie ryzyko)**: Kredyt odrzucony - klient stanowi ryzyko

### Model trójklasowy (3 klasy):
- **Klasa 0 (Niskie ryzyko)**: Kredyt zatwierdzony
- **Klasa 1 (Średnie ryzyko)**: Wymaga dodatkowej weryfikacji
- **Klasa 2 (Wysokie ryzyko)**: Kredyt odrzucony

### Prawdopodobieństwa:
- Pokazują pewność modelu dla każdej kategorii
- Suma wszystkich prawdopodobieństw = 100%
- Wyższe prawdopodobieństwo = większa pewność

### Pewność decyzji:
- Wartość od 0% do 100%
- Powyżej 70%: Wysoka pewność
- 50-70%: Średnia pewność
- Poniżej 50%: Niska pewność (rzadkie)

## Mapowanie atrybutów

System automatycznie konwertuje czytelne odpowiedzi na kody używane przez model:

| Atrybut | Opis | Format wejściowy | Format modelu |
|---------|------|------------------|---------------|
| Attribute1 | Status konta | "200 DM lub więcej..." | A13 |
| Attribute2 | Czas trwania | 24 | 24 |
| Attribute3 | Historia | "istniejące kredyty..." | A32 |
| ... | ... | ... | ... |

Pełne mapowanie znajduje się w pliku `interactive_survey.py` w słowniku `ENCODINGS`.

## Rozwiązywanie problemów

### Błąd: "Model nie został znaleziony"
**Rozwiązanie**: Wytrenuj modele:
```bash
python run_train.py
```

### Błąd: "ModuleNotFoundError: No module named 'pandas'"
**Rozwiązanie**: Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

### Błąd: "Nieprawidłowy wybór"
**Rozwiązanie**: Upewnij się, że wprowadzasz numer opcji (nie tekst)

## Integracja z systemem

### Dla programistów

Możesz zintegrować funkcjonalność ankiety z własnym systemem:

```python
from interactive_survey import przeprowadz_ankiete, wykonaj_predykcje

# Zbierz dane od użytkownika
dane_klienta = przeprowadz_ankiete()

# Wykonaj predykcję
wynik, prawdopodobienstwa = wykonaj_predykcje(dane_klienta)

# Przetwórz wynik
if wynik == 0:
    print("Kredyt zatwierdzony")
else:
    print("Kredyt odrzucony")
```

### API REST (przyszła funkcjonalność)

W przyszłości planowane jest udostępnienie API REST:
```bash
POST /api/predict
{
  "Attribute1": "A13",
  "Attribute2": 24,
  ...
}
```

## Bezpieczeństwo i prywatność

- System nie przechowuje danych użytkownika
- Wszystkie obliczenia wykonywane są lokalnie
- Dane nie są wysyłane do żadnych zewnętrznych serwisów
- Po zamknięciu programu dane są usuwane z pamięci

## Kontakt i wsparcie

Autorzy: Danylo Moskovchuk i Nazar Marakhovkyi

Jeśli masz pytania lub napotkasz problemy, skontaktuj się z zespołem projektu.
