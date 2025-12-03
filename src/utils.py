import pandas as pd
import numpy as np




def ensure_columns(df: pd.DataFrame, required_cols: list):
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Brakuje kolumn: {missing}")
    return True




def create_multiclass_from_binary_or_features(df: pd.DataFrame, target_col: str = "Risk"):
    if target_col in df.columns:
        uniques = df[target_col].unique()
    if len(uniques) >= 3:
    # Upewnij się, że są stringi
        df[target_col] = df[target_col].astype(str)
        return df
# jeśli tu — musimy utworzyć kolumnę
# spróbujmy na podstawie CreditAmount i Duration
    if 'CreditAmount' in df.columns and 'Duration' in df.columns:
# prosty score — większe kwoty i dłuższe okresy => wyższe ryzyko
        ca = (df['CreditAmount'] - df['CreditAmount'].mean()) / (df['CreditAmount'].std() + 1e-9)
        du = (df['Duration'] - df['Duration'].mean()) / (df['Duration'].std() + 1e-9)
# jeśli jest Age, młodsze osoby = wyższe ryzyko? zostawimy neutralnie
        score = ca + du
# podziel na tercyle
        df['Risk'] = pd.qcut(score, q=3, labels=['low', 'medium', 'high'])
        return df
# jeśli nie ma potrzebnych cech, utworzymy równomierny rozkład (ostrożne)
    df['Risk'] = pd.Categorical(pd.qcut(np.random.rand(len(df)), q=3, labels=['low','medium','high']))
    return df