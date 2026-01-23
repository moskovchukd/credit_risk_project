# Wyjaśnienie Matematyczne - Projekt Oceny Ryzyka Kredytowego

## Spis Treści
1. [Definicja Problemu](#definicja-problemu)
2. [Przetwarzanie Wstępne Danych](#przetwarzanie-wstępne-danych)
3. [Obsługa Niezbalansowania Klas (SMOTE)](#obsługa-niezbalansowania-klas-smote)
4. [Model Regresji Logistycznej](#model-regresji-logistycznej)
5. [Proces Uczenia](#proces-uczenia)
6. [Metryki Ewaluacji](#metryki-ewaluacji)
7. [Proces Predykcji](#proces-predykcji)

---

## 1. Definicja Problemu

### 1.1 Zadanie Klasyfikacji

Ten projekt rozwiązuje **problem klasyfikacji nadzorowanej**, gdzie przewidujemy ryzyko kredytowe na podstawie atrybutów klienta.

**Dane wejściowe:**
- Cechy wejściowe: **X** ∈ ℝⁿˣᵐ (n próbek, m cech)
  - n = 1000 klientów
  - m = 20 atrybutów (po przetwarzaniu staje się ~61 cech przez kodowanie one-hot)

- Zmienna docelowa: **y** ∈ {0, 1, 2}
  - 0 = Niskie Ryzyko (Dobry kredyt)
  - 1 = Średnie Ryzyko
  - 2 = Wysokie Ryzyko (Zły kredyt)

**Cel:** Nauczyć funkcję f: ℝᵐ → {0, 1, 2} która minimalizuje błąd predykcji.

### 1.2 Sformułowanie Matematyczne

**Zbiór treningowy:** D = {(x₁, y₁), (x₂, y₂), ..., (xₙ, yₙ)}

Gdzie:
- xᵢ ∈ ℝᵐ jest wektorem cech dla klienta i
- yᵢ ∈ {0, 1, 2} jest prawdziwą klasą ryzyka

**Cel:** Znaleźć optymalne parametry θ które minimalizują funkcję straty:

```
θ* = argmin_θ L(θ, D)
```

---

## 2. Przetwarzanie Wstępne Danych

### 2.1 Typy Cech

Zbiór danych zawiera dwa typy cech:

**Cechy Numeryczne (7 cech):**
- Czas trwania (miesiące)
- Kwota kredytu (DM)
- Stopa raty (%)
- Czas zamieszkania (lata)
- Wiek (lata)
- Liczba kredytów
- Liczba osób na utrzymaniu

**Cechy Kategoryczne (13 cech):**
- Status konta czekowego (4 kategorie)
- Historia kredytowa (5 kategorii)
- Cel kredytu (10 kategorii)
- Konto oszczędnościowe (5 kategorii)
- Zatrudnienie (5 kategorii)
- Status osobisty (5 kategorii)
- Dłużnicy/Poręczyciele (3 kategorie)
- Własność (4 kategorie)
- Inne raty (3 kategorie)
- Mieszkanie (3 kategorie)
- Zawód (4 kategorie)
- Telefon (2 kategorie)
- Pracownik zagraniczny (2 kategorie)

### 2.2 Kodowanie One-Hot

Zmienne kategoryczne są przekształcane za pomocą kodowania one-hot:

Dla zmiennej kategorycznej C z k kategoriami {c₁, c₂, ..., cₖ}:

```
C → [I(C=c₁), I(C=c₂), ..., I(C=cₖ₋₁)]
```

Gdzie I(·) jest funkcją wskaźnikową:

```
I(C=cᵢ) = {1  jeśli C = cᵢ
          {0  w przeciwnym razie
```

**Przykład:** Status Konta Czekowego (4 kategorie)
- "A11" → [1, 0, 0]
- "A12" → [0, 1, 0]
- "A13" → [0, 0, 1]
- "A14" → [0, 0, 0]

Uwaga: Używamy k-1 zmiennych dummy aby uniknąć współliniowości.

### 2.3 Skalowanie Cech

Cechy numeryczne są standaryzowane przy użyciu normalizacji z-score:

```
x'ᵢⱼ = (xᵢⱼ - μⱼ) / σⱼ
```

Gdzie:
- xᵢⱼ = oryginalna wartość cechy j dla próbki i
- μⱼ = średnia cechy j: μⱼ = (1/n)Σᵢ xᵢⱼ
- σⱼ = odchylenie standardowe: σⱼ = √[(1/n)Σᵢ(xᵢⱼ - μⱼ)²]
- x'ᵢⱼ = wartość standaryzowana

**Właściwości:**
- E[x'ⱼ] = 0 (średnia = 0)
- Var[x'ⱼ] = 1 (wariancja = 1)

To zapewnia, że wszystkie cechy mają równy wpływ niezależnie od oryginalnej skali.

### 2.4 Podział Treningowo-Testowy

Zbiór danych jest dzielony na zbiory treningowy i testowy przy użyciu próbkowania stratyfikowanego:

```
D_train, D_test = split(D, test_size=0.25, stratify=y)
```

**Stratyfikacja zapewnia:**
```
P(y=k | x ∈ D_train) ≈ P(y=k | x ∈ D_test) dla wszystkich k ∈ {0,1,2}
```

To zachowuje rozkład klas w obu zbiorach.

---

## 3. Obsługa Niezbalansowania Klas (SMOTE)

### 3.1 Problem

Zbiory danych o ryzyku kredytowym są zazwyczaj niezbalansowane:
- Wielu dobrych klientów (klasa 0): ~70%
- Niewielu złych klientów (klasa 2): ~30%

To powoduje, że model jest stronniczy w kierunku klasy większościowej.

### 3.2 Algorytm SMOTE

**SMOTE** (Synthetic Minority Over-sampling Technique) generuje syntetyczne próbki dla klas mniejszościowych.

**Algorytm:**

Dla każdej próbki xᵢ w klasie mniejszościowej:

1. Znajdź k najbliższych sąsiadów w przestrzeni cech:
   ```
   N_k(xᵢ) = {xⱼ : ||xⱼ - xᵢ||₂ ≤ r_k}
   ```
   Gdzie r_k jest odległością do k-tego najbliższego sąsiada.

2. Losowo wybierz jednego sąsiada xⱼ ∈ N_k(xᵢ)

3. Wygeneruj syntetyczną próbkę wzdłuż odcinka linii:
   ```
   x_synthetic = xᵢ + λ(xⱼ - xᵢ)
   ```
   Gdzie λ ~ U(0,1) jest liczbą losową z rozkładu jednostajnego.

**Intuicja:** Tworzy nowe próbki które są "wiarygodne" ponieważ interpolują między istniejącymi próbkami.

**W naszej implementacji:**
```python
smote = SMOTE(random_state=42, k_neighbors=3)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
```

---

## 4. Model Regresji Logistycznej

### 4.1 Wielomianowa Regresja Logistyczna

Ponieważ mamy 3 klasy (Niskie, Średnie, Wysokie ryzyko), używamy **wielomianowej regresji logistycznej**.

### 4.2 Architektura Modelu

**Kombinacja liniowa dla każdej klasy k:**
```
zₖ(x) = θₖ₀ + θₖ₁x₁ + θₖ₂x₂ + ... + θₖₘxₘ = θₖᵀx
```

Gdzie:
- θₖ ∈ ℝᵐ⁺¹ = wektor parametrów dla klasy k
- x ∈ ℝᵐ⁺¹ = wektor cech (z x₀=1 dla wyrazu wolnego)

**Funkcja softmax** konwertuje wyniki na prawdopodobieństwa:
```
P(y=k|x; θ) = exp(zₖ(x)) / Σⱼ₌₀² exp(zⱼ(x))
```

**Właściwości:**
1. Σₖ P(y=k|x; θ) = 1 (prawdopodobieństwa sumują się do 1)
2. P(y=k|x; θ) ∈ (0, 1) dla wszystkich k
3. exp(zₖ) zapewnia nieujemność

### 4.3 Granica Decyzyjna

Granica decyzyjna między klasami k i j jest zdefiniowana przez:
```
P(y=k|x) = P(y=j|x)
⟺ exp(zₖ(x)) / Σᵢ exp(zᵢ(x)) = exp(zⱼ(x)) / Σᵢ exp(zᵢ(x))
⟺ exp(zₖ(x)) = exp(zⱼ(x))
⟺ zₖ(x) = zⱼ(x)
⟺ θₖᵀx = θⱼᵀx
⟺ (θₖ - θⱼ)ᵀx = 0
```

Jest to **hiperpłaszczyzna** w przestrzeni cech.

### 4.4 Funkcja Straty

Używamy **straty entropii krzyżowej** (ujemna log-wiarygodność):

```
L(θ) = -1/n Σᵢ₌₁ⁿ Σₖ₌₀² I(yᵢ=k) log P(y=k|xᵢ; θ)
```

Gdzie I(yᵢ=k) jest funkcją wskaźnikową:
```
I(yᵢ=k) = {1  jeśli yᵢ = k
          {0  w przeciwnym razie
```

**Rozwinięta postać:**
```
L(θ) = -1/n Σᵢ₌₁ⁿ Σₖ₌₀² I(yᵢ=k) [zₖ(xᵢ) - log(Σⱼ₌₀² exp(zⱼ(xᵢ)))]
```

**Intuicja:** Minimalizacja L(θ) maksymalizuje wiarygodność prawidłowej klasy.

### 4.5 Regularyzacja

Aby zapobiec przeuczeniu, dodajemy **regularyzację L2** (Ridge):

```
L_reg(θ) = L(θ) + λ/2 Σₖ₌₀² ||θₖ||₂²
```

Gdzie:
- λ > 0 jest parametrem regularyzacji
- ||θₖ||₂² = Σⱼ θₖⱼ² jest kwadratem normy L2

**Efekt:** Karze duże wagi, zachęcając do prostszych modeli.

---

## 5. Proces Uczenia

### 5.1 Algorytm Optymalizacji

Używamy algorytmu **L-BFGS** (Limited-memory Broyden–Fletcher–Goldfarb–Shanno).

**Cel:**
```
θ* = argmin_θ L_reg(θ)
```

**L-BFGS jest metodą quasi-Newtona:**

1. **Obliczanie gradientu:**
   ```
   ∇_θₖ L(θ) = -1/n Σᵢ₌₁ⁿ [I(yᵢ=k) - P(y=k|xᵢ; θ)]xᵢ
   ```

2. **Reguła aktualizacji:**
   ```
   θₖ^(t+1) = θₖ^(t) - α_t H_t^(-1) ∇_θₖ L(θ^(t))
   ```

   Gdzie:
   - α_t = współczynnik uczenia w iteracji t
   - H_t ≈ aproksymacja Hesjaninu (z ograniczoną pamięcią)
   - ∇_θₖ L(θ^(t)) = gradient przy aktualnych parametrach

**Kryterium zbieżności:**
```
||∇L(θ^(t))|| < ε  lub  t > max_iter
```

W naszej implementacji:
- max_iter = 2000
- ε = 10⁻⁴ (domyślna tolerancja)

### 5.2 Inicjalizacja Parametrów

Parametry są inicjalizowane losowo:
```
θₖⱼ ~ N(0, σ²)
```

Gdzie σ jest wybierane na podstawie liczby cech (inicjalizacja Xaviera).

---

## 6. Metryki Ewaluacji

### 6.1 Dokładność

**Definicja:**
```
Accuracy = (TP + TN) / n = 1/n Σᵢ₌₁ⁿ I(ŷᵢ = yᵢ)
```

Gdzie:
- ŷᵢ = przewidywana klasa
- yᵢ = prawdziwa klasa
- n = całkowita liczba próbek

### 6.2 Macierz Pomyłek

Dla wieloklasowej (K=3 klasy), macierz pomyłek C ∈ ℝ^(K×K):

```
C[i,j] = liczba próbek z prawdziwą klasą i przewidzianą jako klasa j
```

**Przykład:**
```
           Przewidywane
         Niskie  Śred  Wys
Prawdz.  [70     5     3]
Niskie
Średnie  [ 4    15     6]
Wysokie  [ 2     8    87]
```

### 6.3 Precyzja, Czułość, Wskaźnik F1

Dla każdej klasy k:

**Precyzja:**
```
Precision_k = TP_k / (TP_k + FP_k)
```
Proporcja przewidywanej klasy k która faktycznie jest klasą k.

**Czułość (Sensitivity):**
```
Recall_k = TP_k / (TP_k + FN_k)
```
Proporcja faktycznej klasy k która jest poprawnie przewidziana.

**Wskaźnik F1:**
```
F1_k = 2 · (Precision_k · Recall_k) / (Precision_k + Recall_k)
```
Średnia harmoniczna precyzji i czułości.

Gdzie:
- TP_k = Prawdziwe Pozytywy dla klasy k = C[k,k]
- FP_k = Fałszywe Pozytywy = Σᵢ≠ₖ C[i,k]
- FN_k = Fałszywe Negatywy = Σⱼ≠ₖ C[k,j]

### 6.4 Krzywa ROC i AUC

**Krzywa ROC** (Receiver Operating Characteristic) dla klasyfikacji binarnej:

Dla każdego progu t ∈ [0,1]:
1. Przewiduj klasę 1 jeśli P(y=1|x) ≥ t, w przeciwnym razie klasę 0
2. Oblicz:
   ```
   TPR(t) = TP(t) / (TP(t) + FN(t))  (Wskaźnik Prawdziwie Pozytywnych)
   FPR(t) = FP(t) / (FP(t) + TN(t))  (Wskaźnik Fałszywie Pozytywnych)
   ```

Wykres: (FPR(t), TPR(t)) dla wszystkich t ∈ [0,1]

**AUC** (Pole Pod Krzywą):
```
AUC = ∫₀¹ TPR(FPR⁻¹(x)) dx
```

**Interpretacja:**
- AUC = 1.0: Idealny klasyfikator
- AUC = 0.5: Losowy klasyfikator
- AUC > 0.8: Dobry klasyfikator

**Dla wieloklasowej:** Użyj podejścia One-vs-Rest (OvR):
```
AUC_k = AUC(klasa k vs wszystkie inne klasy)
AUC_macro = 1/K Σₖ AUC_k
```

### 6.5 Krzywa Precyzja-Czułość

Dla każdego progu t:
```
Precision(t) = TP(t) / (TP(t) + FP(t))
Recall(t) = TP(t) / (TP(t) + FN(t))
```

Wykres: (Recall(t), Precision(t)) dla wszystkich t

**Średnia Precyzja:**
```
AP = Σₙ [Recall(n) - Recall(n-1)] · Precision(n)
```

---

## 7. Proces Predykcji

### 7.1 Przetwarzanie Nowych Danych

Dla nowego klienta z cechami x_new:

1. **Kodowanie one-hot** zmiennych kategorycznych
2. **Standaryzacja** cech numerycznych przy użyciu statystyk treningowych:
   ```
   x'_new = (x_new - μ_train) / σ_train
   ```

### 7.2 Obliczanie Prawdopodobieństw

```
z_k = θ_k^T x'_new  dla k ∈ {0, 1, 2}

P(y=k|x_new) = exp(z_k) / Σⱼ exp(z_j)
```

**Przykładowy wynik:**
```
P(y=0|x_new) = 0.85  (Niskie ryzyko)
P(y=1|x_new) = 0.12  (Średnie ryzyko)
P(y=2|x_new) = 0.03  (Wysokie ryzyko)
```

### 7.3 Podejmowanie Decyzji

**Predykcja:**
```
ŷ = argmax_k P(y=k|x_new)
```

**Pewność:**
```
Confidence = max_k P(y=k|x_new)
```

**Reguła decyzyjna:**
```
jeśli ŷ = 0 (Niskie ryzyko):
    Decyzja = "ZATWIERDZONY"
jeśli ŷ = 1 (Średnie ryzyko):
    Decyzja = "WYMAGA WERYFIKACJI"
w przeciwnym razie:  # ŷ = 2 (Wysokie ryzyko)
    Decyzja = "ODRZUCONY"
```

### 7.4 Interpretacja Matematyczna

Model uczy się granic decyzyjnych w 61-wymiarowej przestrzeni cech:

**Dla 3 klas mamy 3 hiperpłaszczyzny:**
```
H_{0,1}: (θ_0 - θ_1)^T x = 0  (oddziela Niskie od Średniego)
H_{0,2}: (θ_0 - θ_2)^T x = 0  (oddziela Niskie od Wysokiego)
H_{1,2}: (θ_1 - θ_2)^T x = 0  (oddziela Średnie od Wysokiego)
```

**Regiony predykcji:**
```
R_0 = {x : θ_0^T x > θ_1^T x i θ_0^T x > θ_2^T x}  (Niskie ryzyko)
R_1 = {x : θ_1^T x > θ_0^T x i θ_1^T x > θ_2^T x}  (Średnie ryzyko)
R_2 = {x : θ_2^T x > θ_0^T x i θ_2^T x > θ_1^T x}  (Wysokie ryzyko)
```

---

## 8. Kompletny Proces Matematyczny

### Proces Wejście → Wyjście:

1. **Wejście:** Surowe dane klienta (20 atrybutów)
   ```
   x_raw ∈ {wartości kategoryczne} × ℝ^7
   ```

2. **Przetwarzanie wstępne:**
   ```
   x_encoded = OneHotEncode(x_categorical) ∈ {0,1}^54
   x_scaled = (x_numerical - μ) / σ ∈ ℝ^7
   x = [x_encoded, x_scaled] ∈ ℝ^61
   ```

3. **Transformacja liniowa:**
   ```
   z_k = θ_k^T x = θ_{k,0} + Σⱼ₌₁⁶¹ θ_{k,j} x_j  dla k ∈ {0,1,2}
   ```

4. **Softmax:**
   ```
   P(y=k|x) = exp(z_k) / [exp(z_0) + exp(z_1) + exp(z_2)]
   ```

5. **Klasyfikacja:**
   ```
   ŷ = argmax_{k∈{0,1,2}} P(y=k|x)
   ```

6. **Wyjście:**
   ```
   {
     predykcja: ŷ ∈ {0, 1, 2},
     prawdopodobieństwa: [P(y=0|x), P(y=1|x), P(y=2|x)],
     pewność: max_k P(y=k|x),
     decyzja: "ZATWIERDZONY" | "WERYFIKACJA" | "ODRZUCONY"
   }
   ```

---

## 9. Dlaczego Regresja Logistyczna Działa Dobrze

### 9.1 Zalety Teoretyczne

1. **Wypukła Funkcja Straty:**
   - Gwarantowane globalne minimum
   - Brak problemów z lokalnymi minimami

2. **Interpretacja Probabilistyczna:**
   - Zapewnia dobrze skalibrowane prawdopodobieństwa
   - Kwantyfikacja niepewności

3. **Liniowe Granice Decyzyjne:**
   - Interpretowalność
   - Szybkie obliczenia
   - Dobra generalizacja z odpowiednią regularyzacją

4. **Efektywność:**
   - Uczenie: O(n·m·K) na iterację
   - Predykcja: O(m·K) na próbkę
   - Gdzie n=próbki, m=cechy, K=klasy

### 9.2 Wydajność Empiryczna

Dla danych o ryzyku kredytowym:
- **Dokładność:** Zazwyczaj 70-80%
- **AUC:** 0.75-0.85
- **Szybkie uczenie:** ~1-2 sekundy
- **Szybka predykcja:** <1ms na próbkę

---

## 10. Podsumowanie

Ten system oceny ryzyka kredytowego wykorzystuje:

1. **Przetwarzanie Wstępne Danych** do obsługi mieszanych danych kategorycznych/numerycznych
2. **SMOTE** do rozwiązania problemu niezbalansowania klas
3. **Wielomianową Regresję Logistyczną** do klasyfikacji wieloklasowej
4. **Optymalizację L-BFGS** z regularyzacją L2
5. **Kompleksowe metryki ewaluacji** do oceny wydajności

Fundamenty matematyczne zapewniają:
- **Interpretowalność:** Model liniowy z czytelnymi wagami cech
- **Efektywność:** Szybkie uczenie i predykcja
- **Odporność:** Regularyzacja zapobiega przeuczeniu
- **Niezawodność:** Dobrze skalibrowane estymaty prawdopodobieństwa

---

## Bibliografia

### Podsumowanie Kluczowych Wzorów:

**Softmax:**
```
P(y=k|x) = exp(θ_k^T x) / Σⱼ exp(θ_j^T x)
```

**Strata Entropii Krzyżowej:**
```
L(θ) = -1/n Σᵢ Σₖ I(yᵢ=k) log P(y=k|xᵢ; θ) + λ/2 Σₖ ||θₖ||²
```

**Gradient:**
```
∇_θₖ L = -1/n Σᵢ [I(yᵢ=k) - P(y=k|xᵢ)] xᵢ + λθₖ
```

**SMOTE:**
```
x_synthetic = xᵢ + λ(x_neighbor - xᵢ), λ ~ U(0,1)
```

---

**Autorzy:** Danylo Moskovchuk i Nazar Marakhovkyi
**Data:** Styczeń 2026