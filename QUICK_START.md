# Quick Start - System ankiety kredytowej

## Szybki start w 3 krokach

### 1️⃣ Sprawdź czy masz wytrenowane modele
```bash
ls models/*.pkl
```

Jeśli nie ma modeli, wytrenuj je:
```bash
python run_train.py
```

### 2️⃣ Wybierz tryb pracy

#### Opcja A: Interaktywna ankieta (pojedynczy klient)
```bash
python interactive_survey.py
```
Odpowiadaj na pytania krok po kroku.

#### Opcja B: Demo (testowanie)
```bash
python demo_survey.py
```
Zobacz przykładowe predykcje.

#### Opcja C: Przetwarzanie wsadowe (wielu klientów)
```bash
python batch_survey.py klienci.csv wyniki.csv
```
Przetwórz plik CSV z wieloma klientami.

### 3️⃣ Interpretuj wyniki

**✅ Kredyt zatwierdzony**: Niskie ryzyko, klient wiarygodny
**⚠️ Wymaga weryfikacji**: Średnie ryzyko (tylko model 3-klasowy)
**❌ Kredyt odrzucony**: Wysokie ryzyko

---

## Przykład sesji

```bash
$ python interactive_survey.py

╔══════════════════════════════════════════════════════════╗
║                                                          ║
║          SYSTEM OCENY RYZYKA KREDYTOWEGO                 ║
║          Interaktywna ankieta klienta                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

Prosze odpowiedzieć na następujące pytania.

============================================================
Status istniejącego konta czekowego:

  1. mniej niż 0 DM
  2. od 0 do 200 DM
  3. 200 DM lub więcej / wypłaty przez co najmniej 1 rok
  4. brak konta czekowego

Wybierz numer opcji: 3

============================================================
Czas trwania kredytu (w miesiącach):

Wprowadź wartość: 24

[... 18 kolejnych pytań ...]

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

## Pliki i dokumentacja

| Plik | Opis |
|------|------|
| [interactive_survey.py](interactive_survey.py) | Interaktywna ankieta |
| [demo_survey.py](demo_survey.py) | Demo z przykładami |
| [batch_survey.py](batch_survey.py) | Przetwarzanie wsadowe |
| [INSTRUKCJA_ANKIETY.md](INSTRUKCJA_ANKIETY.md) | Szczegółowa instrukcja |
| [MAPOWANIE_ATRYBUTOW.md](MAPOWANIE_ATRYBUTOW.md) | Mapowanie kodów |
| [NOWE_FUNKCJE.md](NOWE_FUNKCJE.md) | Opis nowych funkcji |

---

## Najczęstsze problemy

### Problem: "ModuleNotFoundError: No module named 'pandas'"
**Rozwiązanie:**
```bash
pip install -r requirements.txt
```

### Problem: "Model nie został znaleziony"
**Rozwiązanie:**
```bash
python run_train.py
```

### Problem: "Nieprawidłowy wybór"
**Rozwiązanie:** Wprowadź numer opcji (np. "1", "2", "3"), nie tekst opisowy.

---

## Pomoc

**📖 Dokumentacja**: Zobacz [INSTRUKCJA_ANKIETY.md](INSTRUKCJA_ANKIETY.md)

**🗺️ Mapowanie**: Zobacz [MAPOWANIE_ATRYBUTOW.md](MAPOWANIE_ATRYBUTOW.md)

**🆕 Nowe funkcje**: Zobacz [NOWE_FUNKCJE.md](NOWE_FUNKCJE.md)

**👥 Autorzy**: Danylo Moskovchuk i Nazar Marakhovkyi

---

**Gotowe!** Możesz teraz korzystać z systemu ankiety kredytowej. 🎉
