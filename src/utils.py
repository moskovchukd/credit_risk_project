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
          
            if df[target_col].dtype == 'object':
                label_map = {'low': 0, 'medium': 1, 'high': 2}
                df[target_col] = df[target_col].map(label_map)
            return df

        
        elif len(uniques) == 2:
            print("Converting binary Risk to 3-class classification...")
     
            df = df.drop(columns=[target_col])

    credit_col = None
    duration_col = None

    if 'CreditAmount' in df.columns:
        credit_col = 'CreditAmount'
    elif 'Attribute5' in df.columns:
        credit_col = 'Attribute5'

    if 'Duration' in df.columns:
        duration_col = 'Duration'
    elif 'Attribute2' in df.columns:
        duration_col = 'Attribute2'

    if credit_col is not None and duration_col is not None:
   
        ca = (df[credit_col] - df[credit_col].mean()) / (df[credit_col].std() + 1e-9)
        du = (df[duration_col] - df[duration_col].mean()) / (df[duration_col].std() + 1e-9)
        score = ca + du

     
        df[target_col] = pd.qcut(score, q=3, labels=[0, 1, 2], duplicates='drop')
        df[target_col] = df[target_col].astype(int)
        print(f"Created 3-class Risk column based on {credit_col} and {duration_col}")
        print(f"Distribution: \n{df[target_col].value_counts().sort_index()}")
        return df

    print("Warning: Creating random 3-class distribution - no relevant features found")
    df[target_col] = pd.Categorical(pd.qcut(np.random.rand(len(df)), q=3, labels=[0, 1, 2]))
    df[target_col] = df[target_col].astype(int)
    return df