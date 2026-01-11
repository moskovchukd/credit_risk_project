# Mathematical Explanation - Credit Risk Assessment Project

## Table of Contents
1. [Problem Definition](#problem-definition)
2. [Data Preprocessing](#data-preprocessing)
3. [Class Imbalance Handling (SMOTE)](#class-imbalance-handling-smote)
4. [Logistic Regression Model](#logistic-regression-model)
5. [Training Process](#training-process)
6. [Evaluation Metrics](#evaluation-metrics)
7. [Prediction Process](#prediction-process)

---

## 1. Problem Definition

### 1.1 Classification Task

This project solves a **supervised classification problem** where we predict credit risk based on customer attributes.

**Given:**
- Input features: **X** ∈ ℝⁿˣᵐ (n samples, m features)
  - n = 1000 customers
  - m = 20 attributes (after preprocessing becomes ~61 features due to one-hot encoding)

- Target variable: **y** ∈ {0, 1, 2}
  - 0 = Low Risk (Good credit)
  - 1 = Medium Risk
  - 2 = High Risk (Bad credit)

**Objective:** Learn a function f: ℝᵐ → {0, 1, 2} that minimizes prediction error.

### 1.2 Mathematical Formulation

**Training set:** D = {(x₁, y₁), (x₂, y₂), ..., (xₙ, yₙ)}

Where:
- xᵢ ∈ ℝᵐ is the feature vector for customer i
- yᵢ ∈ {0, 1, 2} is the true risk class

**Goal:** Find optimal parameters θ that minimize the loss function:

```
θ* = argmin_θ L(θ, D)
```

---

## 2. Data Preprocessing

### 2.1 Feature Types

The dataset contains two types of features:

**Numerical Features (7 features):**
- Duration (months)
- Credit Amount (DM)
- Installment Rate (%)
- Residence Duration (years)
- Age (years)
- Number of Credits
- Number of Dependents

**Categorical Features (13 features):**
- Checking Account Status (4 categories)
- Credit History (5 categories)
- Purpose (10 categories)
- Savings Account (5 categories)
- Employment (5 categories)
- Personal Status (5 categories)
- Debtors/Guarantors (3 categories)
- Property (4 categories)
- Other Installments (3 categories)
- Housing (3 categories)
- Job (4 categories)
- Telephone (2 categories)
- Foreign Worker (2 categories)

### 2.2 One-Hot Encoding

Categorical variables are transformed using one-hot encoding:

For a categorical variable C with k categories {c₁, c₂, ..., cₖ}:

```
C → [I(C=c₁), I(C=c₂), ..., I(C=cₖ₋₁)]
```

Where I(·) is the indicator function:

```
I(C=cᵢ) = {1  if C = cᵢ
          {0  otherwise
```

**Example:** Checking Account Status (4 categories)
- "A11" → [1, 0, 0]
- "A12" → [0, 1, 0]
- "A13" → [0, 0, 1]
- "A14" → [0, 0, 0]

Note: We use k-1 dummy variables to avoid multicollinearity.

### 2.3 Feature Scaling

Numerical features are standardized using z-score normalization:

```
x'ᵢⱼ = (xᵢⱼ - μⱼ) / σⱼ
```

Where:
- xᵢⱼ = original value of feature j for sample i
- μⱼ = mean of feature j: μⱼ = (1/n)Σᵢ xᵢⱼ
- σⱼ = standard deviation: σⱼ = √[(1/n)Σᵢ(xᵢⱼ - μⱼ)²]
- x'ᵢⱼ = standardized value

**Properties:**
- E[x'ⱼ] = 0 (mean = 0)
- Var[x'ⱼ] = 1 (variance = 1)

This ensures all features have equal influence regardless of their original scale.

### 2.4 Train-Test Split

The dataset is split into training and test sets using stratified sampling:

```
D_train, D_test = split(D, test_size=0.25, stratify=y)
```

**Stratification ensures:**
```
P(y=k | x ∈ D_train) ≈ P(y=k | x ∈ D_test) for all k ∈ {0,1,2}
```

This maintains class distribution across splits.

---

## 3. Class Imbalance Handling (SMOTE)

### 3.1 Problem

Credit risk datasets are typically imbalanced:
- Many good customers (class 0): ~70%
- Few bad customers (class 2): ~30%

This causes the model to be biased toward the majority class.

### 3.2 SMOTE Algorithm

**SMOTE** (Synthetic Minority Over-sampling Technique) generates synthetic samples for minority classes.

**Algorithm:**

For each sample xᵢ in minority class:

1. Find k nearest neighbors in feature space:
   ```
   N_k(xᵢ) = {xⱼ : ||xⱼ - xᵢ||₂ ≤ r_k}
   ```
   Where r_k is the distance to the k-th nearest neighbor.

2. Randomly select one neighbor xⱼ ∈ N_k(xᵢ)

3. Generate synthetic sample along the line segment:
   ```
   x_synthetic = xᵢ + λ(xⱼ - xᵢ)
   ```
   Where λ ~ U(0,1) is uniformly distributed random number.

**Intuition:** Creates new samples that are "believable" because they interpolate between existing samples.

**In our implementation:**
```python
smote = SMOTE(random_state=42, k_neighbors=3)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
```

---

## 4. Logistic Regression Model

### 4.1 Multinomial Logistic Regression

Since we have 3 classes (Low, Medium, High risk), we use **multinomial logistic regression**.

### 4.2 Model Architecture

**Linear combination for each class k:**
```
zₖ(x) = θₖ₀ + θₖ₁x₁ + θₖ₂x₂ + ... + θₖₘxₘ = θₖᵀx
```

Where:
- θₖ ∈ ℝᵐ⁺¹ = parameter vector for class k
- x ∈ ℝᵐ⁺¹ = feature vector (with x₀=1 for intercept)

**Softmax function** converts scores to probabilities:
```
P(y=k|x; θ) = exp(zₖ(x)) / Σⱼ₌₀² exp(zⱼ(x))
```

**Properties:**
1. Σₖ P(y=k|x; θ) = 1 (probabilities sum to 1)
2. P(y=k|x; θ) ∈ (0, 1) for all k
3. exp(zₖ) ensures non-negativity

### 4.3 Decision Boundary

The decision boundary between classes k and j is defined by:
```
P(y=k|x) = P(y=j|x)
⟺ exp(zₖ(x)) / Σᵢ exp(zᵢ(x)) = exp(zⱼ(x)) / Σᵢ exp(zᵢ(x))
⟺ exp(zₖ(x)) = exp(zⱼ(x))
⟺ zₖ(x) = zⱼ(x)
⟺ θₖᵀx = θⱼᵀx
⟺ (θₖ - θⱼ)ᵀx = 0
```

This is a **hyperplane** in feature space.

### 4.4 Loss Function

We use **cross-entropy loss** (negative log-likelihood):

```
L(θ) = -1/n Σᵢ₌₁ⁿ Σₖ₌₀² I(yᵢ=k) log P(y=k|xᵢ; θ)
```

Where I(yᵢ=k) is the indicator function:
```
I(yᵢ=k) = {1  if yᵢ = k
          {0  otherwise
```

**Expanded form:**
```
L(θ) = -1/n Σᵢ₌₁ⁿ Σₖ₌₀² I(yᵢ=k) [zₖ(xᵢ) - log(Σⱼ₌₀² exp(zⱼ(xᵢ)))]
```

**Intuition:** Minimizing L(θ) maximizes the likelihood of the correct class.

### 4.5 Regularization

To prevent overfitting, we add **L2 regularization** (Ridge):

```
L_reg(θ) = L(θ) + λ/2 Σₖ₌₀² ||θₖ||₂²
```

Where:
- λ > 0 is the regularization parameter
- ||θₖ||₂² = Σⱼ θₖⱼ² is the squared L2 norm

**Effect:** Penalizes large weights, encouraging simpler models.

---

## 5. Training Process

### 5.1 Optimization Algorithm

We use **L-BFGS** (Limited-memory Broyden–Fletcher–Goldfarb–Shanno) algorithm.

**Objective:**
```
θ* = argmin_θ L_reg(θ)
```

**L-BFGS is a quasi-Newton method:**

1. **Gradient computation:**
   ```
   ∇_θₖ L(θ) = -1/n Σᵢ₌₁ⁿ [I(yᵢ=k) - P(y=k|xᵢ; θ)]xᵢ
   ```

2. **Update rule:**
   ```
   θₖ^(t+1) = θₖ^(t) - α_t H_t^(-1) ∇_θₖ L(θ^(t))
   ```

   Where:
   - α_t = learning rate at iteration t
   - H_t ≈ Hessian approximation (using limited memory)
   - ∇_θₖ L(θ^(t)) = gradient at current parameters

**Convergence criterion:**
```
||∇L(θ^(t))|| < ε  or  t > max_iter
```

In our implementation:
- max_iter = 2000
- ε = 10⁻⁴ (default tolerance)

### 5.2 Parameter Initialization

Parameters are initialized randomly:
```
θₖⱼ ~ N(0, σ²)
```

Where σ is chosen based on the number of features (Xavier initialization).

---

## 6. Evaluation Metrics

### 6.1 Accuracy

**Definition:**
```
Accuracy = (TP + TN) / n = 1/n Σᵢ₌₁ⁿ I(ŷᵢ = yᵢ)
```

Where:
- ŷᵢ = predicted class
- yᵢ = true class
- n = total number of samples

### 6.2 Confusion Matrix

For multiclass (K=3 classes), confusion matrix C ∈ ℝ^(K×K):

```
C[i,j] = number of samples with true class i predicted as class j
```

**Example:**
```
           Predicted
         Low  Med  High
True Low  [70   5    3]
    Med   [ 4  15    6]
   High   [ 2   8   87]
```

### 6.3 Precision, Recall, F1-Score

For each class k:

**Precision:**
```
Precision_k = TP_k / (TP_k + FP_k)
```
Proportion of predicted class k that are actually class k.

**Recall (Sensitivity):**
```
Recall_k = TP_k / (TP_k + FN_k)
```
Proportion of actual class k that are correctly predicted.

**F1-Score:**
```
F1_k = 2 · (Precision_k · Recall_k) / (Precision_k + Recall_k)
```
Harmonic mean of precision and recall.

Where:
- TP_k = True Positives for class k = C[k,k]
- FP_k = False Positives = Σᵢ≠ₖ C[i,k]
- FN_k = False Negatives = Σⱼ≠ₖ C[k,j]

### 6.4 ROC Curve and AUC

**ROC Curve** (Receiver Operating Characteristic) for binary classification:

For each threshold t ∈ [0,1]:
1. Predict class 1 if P(y=1|x) ≥ t, else class 0
2. Calculate:
   ```
   TPR(t) = TP(t) / (TP(t) + FN(t))  (True Positive Rate)
   FPR(t) = FP(t) / (FP(t) + TN(t))  (False Positive Rate)
   ```

Plot: (FPR(t), TPR(t)) for all t ∈ [0,1]

**AUC** (Area Under Curve):
```
AUC = ∫₀¹ TPR(FPR⁻¹(x)) dx
```

**Interpretation:**
- AUC = 1.0: Perfect classifier
- AUC = 0.5: Random classifier
- AUC > 0.8: Good classifier

**For multiclass:** Use One-vs-Rest (OvR) approach:
```
AUC_k = AUC(class k vs all other classes)
AUC_macro = 1/K Σₖ AUC_k
```

### 6.5 Precision-Recall Curve

For each threshold t:
```
Precision(t) = TP(t) / (TP(t) + FP(t))
Recall(t) = TP(t) / (TP(t) + FN(t))
```

Plot: (Recall(t), Precision(t)) for all t

**Average Precision:**
```
AP = Σₙ [Recall(n) - Recall(n-1)] · Precision(n)
```

---

## 7. Prediction Process

### 7.1 Preprocessing New Data

For a new customer with features x_new:

1. **One-hot encode** categorical variables
2. **Standardize** numerical features using training statistics:
   ```
   x'_new = (x_new - μ_train) / σ_train
   ```

### 7.2 Computing Probabilities

```
z_k = θ_k^T x'_new  for k ∈ {0, 1, 2}

P(y=k|x_new) = exp(z_k) / Σⱼ exp(z_j)
```

**Example output:**
```
P(y=0|x_new) = 0.85  (Low risk)
P(y=1|x_new) = 0.12  (Medium risk)
P(y=2|x_new) = 0.03  (High risk)
```

### 7.3 Making Decision

**Prediction:**
```
ŷ = argmax_k P(y=k|x_new)
```

**Confidence:**
```
Confidence = max_k P(y=k|x_new)
```

**Decision rule:**
```
if ŷ = 0 (Low risk):
    Decision = "APPROVED"
elif ŷ = 1 (Medium risk):
    Decision = "REQUIRES VERIFICATION"
else:  # ŷ = 2 (High risk)
    Decision = "REJECTED"
```

### 7.4 Mathematical Interpretation

The model learns decision boundaries in 61-dimensional feature space:

**For 3 classes, we have 3 hyperplanes:**
```
H_{0,1}: (θ_0 - θ_1)^T x = 0  (separates Low from Medium)
H_{0,2}: (θ_0 - θ_2)^T x = 0  (separates Low from High)
H_{1,2}: (θ_1 - θ_2)^T x = 0  (separates Medium from High)
```

**Prediction regions:**
```
R_0 = {x : θ_0^T x > θ_1^T x and θ_0^T x > θ_2^T x}  (Low risk)
R_1 = {x : θ_1^T x > θ_0^T x and θ_1^T x > θ_2^T x}  (Medium risk)
R_2 = {x : θ_2^T x > θ_0^T x and θ_2^T x > θ_1^T x}  (High risk)
```

---

## 8. Complete Mathematical Pipeline

### Input → Output Process:

1. **Input:** Raw customer data (20 attributes)
   ```
   x_raw ∈ {categorical values} × ℝ^7
   ```

2. **Preprocessing:**
   ```
   x_encoded = OneHotEncode(x_categorical) ∈ {0,1}^54
   x_scaled = (x_numerical - μ) / σ ∈ ℝ^7
   x = [x_encoded, x_scaled] ∈ ℝ^61
   ```

3. **Linear Transformation:**
   ```
   z_k = θ_k^T x = θ_{k,0} + Σⱼ₌₁⁶¹ θ_{k,j} x_j  for k ∈ {0,1,2}
   ```

4. **Softmax:**
   ```
   P(y=k|x) = exp(z_k) / [exp(z_0) + exp(z_1) + exp(z_2)]
   ```

5. **Classification:**
   ```
   ŷ = argmax_{k∈{0,1,2}} P(y=k|x)
   ```

6. **Output:**
   ```
   {
     prediction: ŷ ∈ {0, 1, 2},
     probabilities: [P(y=0|x), P(y=1|x), P(y=2|x)],
     confidence: max_k P(y=k|x),
     decision: "APPROVED" | "VERIFICATION" | "REJECTED"
   }
   ```

---

## 9. Why Logistic Regression Works Well

### 9.1 Theoretical Advantages

1. **Convex Loss Function:**
   - Global minimum guaranteed
   - No local minima problems

2. **Probabilistic Interpretation:**
   - Provides well-calibrated probabilities
   - Uncertainty quantification

3. **Linear Decision Boundaries:**
   - Interpretable
   - Fast to compute
   - Generalizes well with proper regularization

4. **Efficiency:**
   - Training: O(n·m·K) per iteration
   - Prediction: O(m·K) per sample
   - Where n=samples, m=features, K=classes

### 9.2 Empirical Performance

For credit risk data:
- **Accuracy:** Typically 70-80%
- **AUC:** 0.75-0.85
- **Fast training:** ~1-2 seconds
- **Fast prediction:** <1ms per sample

---

## 10. Summary

This credit risk assessment system uses:

1. **Data Preprocessing** to handle mixed categorical/numerical data
2. **SMOTE** to address class imbalance
3. **Multinomial Logistic Regression** for multi-class classification
4. **L-BFGS optimization** with L2 regularization
5. **Comprehensive evaluation metrics** to assess performance

The mathematical foundation ensures:
- **Interpretability:** Linear model with clear feature weights
- **Efficiency:** Fast training and prediction
- **Robustness:** Regularization prevents overfitting
- **Reliability:** Well-calibrated probability estimates

---

## References

### Key Formulas Summary:

**Softmax:**
```
P(y=k|x) = exp(θ_k^T x) / Σⱼ exp(θ_j^T x)
```

**Cross-Entropy Loss:**
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

**Authors:** Danylo Moskovchuk and Nazar Marakhovkyi
**Date:** January 2026
