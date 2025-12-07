# Nowe funkcje - System ankiety kredytowej

## Przegląd

Dodano kompletny system ankiety kredytowej w języku polskim, który umożliwia:
- Interaktywne zbieranie danych od klientów
- Automatyczną konwersję odpowiedzi z formatu czytelnego do kodów modelu
- Natychmiastową ocenę ryzyka kredytowego
- Przetwarzanie wsadowe wielu klientów

---

## 1. Interaktywna ankieta (interactive_survey.py)

### Opis
Pełna interaktywna ankieta przeprowadzana w terminalu, która krok po kroku zbiera informacje o kliencie.

### Użycie
```bash
python interactive_survey.py
```

### Funkcjonalności
- ✅ 20 pytań w języku polskim
- ✅ Walidacja danych wejściowych
- ✅ Podsumowanie wprowadzonych danych
- ✅ Automatyczna konwersja do formatu modelu
- ✅ Natychmiastowa decyzja kredytowa
- ✅ Prawdopodobieństwa i pewność decyzji

### Przykładowy output
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

---

## 2. Demo z przykładami (demo_survey.py)

### Opis
Skrypt demonstracyjny pokazujący działanie systemu na predefiniowanych danych.

### Użycie
```bash
python demo_survey.py
```

### Funkcjonalności
- ✅ Dwa przykładowe profile klientów
- ✅ Automatyczne predykcje
- ✅ Wyświetlanie szczegółowych wyników
- ✅ Brak potrzeby ręcznego wprowadzania danych

### Przykładowe profile
1. **Klient o niskim ryzyku**: Stabilna sytuacja finansowa, długoterminowe zatrudnienie
2. **Klient o wysokim ryzyku**: Brak oszczędności, krótkie zatrudnienie, wysokie zadłużenie

---

## 3. Przetwarzanie wsadowe (batch_survey.py)

### Opis
Przetwarzanie wielu klientów jednocześnie z pliku CSV.

### Użycie
```bash
python batch_survey.py klienci.csv wyniki.csv
```

### Funkcjonalności
- ✅ Wczytywanie danych z CSV
- ✅ Walidacja wszystkich wymaganych kolumn
- ✅ Wykonywanie predykcji dla wielu klientów
- ✅ Zapisywanie wyników do CSV
- ✅ Statystyki i podsumowanie
- ✅ Tworzenie przykładowych plików testowych

### Format pliku wejściowego
CSV z kolumnami: `Attribute1, Attribute2, ..., Attribute20`

### Format pliku wyjściowego
Wszystkie dane wejściowe + dodatkowe kolumny:
- `ID_Klienta`: Numer klienta (1, 2, 3, ...)
- `Predicted_Risk`: Przewidywana klasa (0, 1, lub 2)
- `Risk_Label`: Etykieta tekstowa (good/bad lub low/medium/high)
- `Prob_Good`, `Prob_Bad`: Prawdopodobieństwa (dla modelu binarnego)
- `Prob_Low`, `Prob_Medium`, `Prob_High`: Prawdopodobieństwa (dla modelu 3-klasowego)
- `Confidence`: Pewność decyzji

### Przykładowy output
```
======================================================================
  PODSUMOWANIE WYNIKÓW
======================================================================

Rozkład decyzji kredytowych:
  • GOOD: 67 (67.0%)
  • BAD: 33 (33.0%)

Średnia pewność decyzji: 78.50%

======================================================================
✅ Przetworzono 100 klientów pomyślnie!
📄 Plik wynikowy: wyniki.csv
======================================================================
```

---

## 4. Dokumentacja

### INSTRUKCJA_ANKIETY.md
Kompletna instrukcja użycia systemu ankiety:
- Wymagania i instalacja
- Krok po kroku instrukcje
- Interpretacja wyników
- Rozwiązywanie problemów
- Integracja z innymi systemami

### MAPOWANIE_ATRYBUTOW.md
Szczegółowe mapowanie wszystkich 20 atrybutów:
- Tabelki z kodami i opisami
- Przykłady użycia
- Format danych wejściowych i wyjściowych

---

## Struktura kodów

### Mapowanie atrybutów (ENCODINGS)
Słownik zawierający wszystkie mapowania z polskiego na kody:

```python
ENCODINGS = {
    'Attribute1': {
        'pytanie': 'Status istniejącego konta czekowego:',
        'opcje': {
            '1': ('mniej niż 0 DM', 'A11'),
            '2': ('od 0 do 200 DM', 'A12'),
            # ...
        }
    },
    # ... 19 innych atrybutów
}
```

### Funkcje kluczowe

1. **przeprowadz_ankiete()**: Główna funkcja ankiety
2. **pobierz_odpowiedz_kategoryczna()**: Zbiera odpowiedzi kategoryczne
3. **pobierz_odpowiedz_numeryczna()**: Zbiera odpowiedzi numeryczne
4. **wykonaj_predykcje()**: Wykonuje predykcję dla danych klienta
5. **wyswietl_podsumowanie()**: Wyświetla podsumowanie danych
6. **przetwarzaj_plik()**: Przetwarzanie wsadowe (batch)

---

## Integracja

### Z istniejącym kodem
System korzysta z istniejących modułów:
- `src.predict.load_best_model()`: Wczytanie najlepszego modelu
- `src.predict.CreditRiskPredictor`: Klasa predykcji
- Wszystkie wytrenowane modele z folderu `models/`

### Dodatkowe zależności
Brak! System używa tylko istniejących bibliotek:
- pandas
- numpy (pośrednio przez model)
- joblib (pośrednio przez model)

---

## Przypadki użycia

### 1. Bank / Instytucja finansowa
- Pracownik banku prowadzi ankietę z klientem
- System natychmiastowo zwraca decyzję
- Możliwość archiwizacji wyników

### 2. Samoobsługa online
- Klient wypełnia ankietę samodzielnie
- Automatyczna ocena ryzyka
- Natychmiastowa informacja o decyzji

### 3. Analiza portfela
- Import danych wielu klientów z CSV
- Masowa ocena ryzyka
- Raportowanie i statystyki

### 4. Testy i demonstracje
- Demo system dla prezentacji
- Szkolenia pracowników
- Testy automatyczne

---

## Zalety implementacji

✅ **Czytelność**: Wszystkie pytania w języku polskim
✅ **Walidacja**: Sprawdzanie poprawności danych wejściowych
✅ **Elastyczność**: Obsługa różnych typów modeli (binarny/3-klasowy)
✅ **Skalowalność**: Przetwarzanie wsadowe dla wielu klientów
✅ **Dokumentacja**: Kompletna dokumentacja i instrukcje
✅ **Łatwość użycia**: Intuicyjny interfejs tekstowy
✅ **Integracja**: Bezproblemowa integracja z istniejącym kodem

---

## Możliwe rozszerzenia

### Krótkoterminowe
- [ ] GUI (Graphical User Interface) z Tkinter lub PyQt
- [ ] API REST (Flask/FastAPI)
- [ ] Eksport do Excel z formatowaniem
- [ ] Historia predykcji (zapisywanie do bazy danych)

### Długoterminowe
- [ ] Aplikacja webowa (React + Flask)
- [ ] Wielojęzyczność (angielski, niemiecki, etc.)
- [ ] Zaawansowane raporty i wizualizacje
- [ ] Integracja z systemami bankowymi
- [ ] Machine learning monitoring i aktualizacja modeli

---

## Testowanie

### Test manualny
1. Uruchom `python interactive_survey.py`
2. Przejdź przez ankietę
3. Zweryfikuj wynik

### Test automatyczny
1. Uruchom `python demo_survey.py`
2. Sprawdź predykcje dla przykładowych profili

### Test wsadowy
1. Utwórz plik CSV z danymi klientów
2. Uruchom `python batch_survey.py klienci.csv`
3. Sprawdź plik wynikowy

---

## Wkład autorów

**Danylo Moskovchuk i Nazar Marakhovkyi**

Funkcjonalność dodana: 2025-12-07
- System interaktywnej ankiety
- Przetwarzanie wsadowe
- Kompletna dokumentacja
- Skrypty demonstracyjne

---

## Kontakt i wsparcie

Jeśli masz pytania lub sugestie dotyczące nowych funkcji:
1. Sprawdź dokumentację w `INSTRUKCJA_ANKIETY.md`
2. Zobacz mapowanie w `MAPOWANIE_ATRYBUTOW.md`
3. Uruchom demo: `python demo_survey.py`
4. Skontaktuj się z zespołem projektu

---

**Gotowe do użycia!** 🚀
