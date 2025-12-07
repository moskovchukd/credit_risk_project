# Projekt: Ocena ryzyka kredytowego

**🚀 Szybki start z ankietą:** Zobacz [QUICK_START.md](QUICK_START.md)

## Instrukcja:
1. Stwórz środowisko (venv) i zainstaluj zależności: `pip install -r requirements.txt`
2. Uruchom trening: `python run_train.py`
   - Trenuje wszystkie modele (LogisticRegression, RandomForest, XGBoost, SVM, KNN)
   - Automatycznie generuje wszystkie wizualizacje
   - Zapisuje modele w folderze `models/`
   - Zapisuje wizualizacje w folderze `visualizations/`
3. **NOWOŚĆ: Interaktywna ankieta:** `python interactive_survey.py`
   - Przeprowadza ankietę w języku polskim
   - Konwertuje odpowiedzi do formatu modelu
   - Natychmiast zwraca decyzję kredytową
   - **Szczegółowa instrukcja:** Zobacz [INSTRUKCJA_ANKIETY.md](INSTRUKCJA_ANKIETY.md)
4. (Opcjonalnie) Inspekcja modeli: `python inspect_model_data.py`
5. (Opcjonalnie) Przykład użycia: `python example_usage.py`
6. (Opcjonalnie) Regeneruj wizualizacje: `python generate_visualizations.py`


## Wizualizacje

Po uruchomieniu `python run_train.py`, w folderze `visualizations/` znajdziesz:

### Model Performance:
- `model_comparison.png` - Porównanie dokładności wszystkich modeli
- `roc_curves.png` - Krzywe ROC dla wszystkich modeli
- `precision_recall_curves.png` - Krzywe Precision-Recall
- `confusion_matrix_[MODEL].png` - Macierze pomyłek dla każdego modelu
- `feature_importance_[MODEL].png` - Ważność cech dla modeli drzewiastych

### Data Quality:
- `target_distribution.png` - Rozkład zmiennej docelowej (Risk)
- `feature_distributions.png` - Rozkłady wszystkich cech numerycznych
- `correlation_matrix.png` - Macierz korelacji między cechami
- `missing_values.png` - Analiza brakujących wartości


## Struktura projektu:

### Główne skrypty:
- `run_train.py` - Główny skrypt treningu i generowania wizualizacji
- `interactive_survey.py` - **NOWOŚĆ:** Interaktywna ankieta w języku polskim dla klientów
- `batch_survey.py` - **NOWOŚĆ:** Przetwarzanie wsadowe wielu klientów z pliku CSV
- `demo_survey.py` - **NOWOŚĆ:** Demo z przykładowymi predykcjami
- `generate_visualizations.py` - Regeneruj wizualizacje bez ponownego treningu
- `inspect_model_data.py` - Inspekcja wytrenowanych modeli
- `example_usage.py` - Przykład użycia modeli do predykcji (dla programistów)

### Moduły źródłowe (src/):
- `preprocessing.py` - Wczytywanie i przygotowanie danych
- `feature_selection.py` - Wybór cech
- `model_training.py` - Trenowanie modeli i porównanie
- `evaluation.py` - Funkcje oceny i generowania wykresów

### Foldery wynikowe:
- `models/` - Wytrenowane modele i wyniki
- `visualizations/` - Wszystkie wygenerowane wykresy
- `notebooks/` - Jupyter notebooks do eksploracji


## Interaktywna ankieta kredytowa

### Opis
Nowa funkcja pozwala na przeprowadzenie ankiety w języku polskim, która zbiera dane od klienta i automatycznie ocenia ryzyko kredytowe.

### Jak używać:
1. Uruchom: `python interactive_survey.py`
2. Odpowiedz na 20 pytań (wybierając numer opcji lub wpisując wartość)
3. Zweryfikuj wprowadzone dane
4. Otrzymaj natychmiastową decyzję kredytową

### Demo:
Aby przetestować system z przykładowymi danymi:
```bash
python demo_survey.py
```

### Przetwarzanie wsadowe:
Dla wielu klientów jednocześnie (z pliku CSV):
```bash
python batch_survey.py klienci.csv wyniki.csv
```

### Więcej informacji:
Szczegółowa instrukcja dostępna w pliku [INSTRUKCJA_ANKIETY.md](INSTRUKCJA_ANKIETY.md)


## Autorzy
Danylo Moskovchuk i Nazar Marakhovkyi