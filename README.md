# Projekt: Ocena ryzyka kredytowego


Instrukcja:
1. Stwórz środowisko (venv) i zainstaluj zależności: `pip install -r requirements.txt`.
2. Uruchom trening: `python run_train.py`.
3. `python inspect_model_data.py`  
4. `python3 example_usage.py`  
5. Wyniki modeli oraz wytrenowany model zostaną zapisane w folderze `models/`.



Pliki:
- `src/preprocessing.py` - wczytywanie i przygotowanie danych
- `src/feature_selection.py` - wybór cech
- `src/model_training.py` - trenowanie modeli i porównanie
- `src/evaluation.py` - funkcje oceny i wykresy
- `run_train.py` - główny skrypt wywołujący pipeline


Autorzy: Danylo Moskovchuk i Nazar Marakhovkyi