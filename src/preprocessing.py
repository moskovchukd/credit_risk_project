import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from src.utils import create_multiclass_from_binary_or_features
from ucimlrepo import fetch_ucirepo




def load_data(path: str):
    df = pd.read_csv(path)
    return df




def build_preprocessing_pipeline(df: pd.DataFrame, numeric_impute_strategy='median'):
# rozpoznaj kolumny numeryczne i kategoryczne
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()


# usuń kolumnę celu jeśli jest w datafrejmie
    if 'Risk' in num_cols:
        num_cols.remove('Risk')
    if 'Risk' in cat_cols:
        cat_cols.remove('Risk')


    numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy=numeric_impute_strategy)),
    ('scaler', StandardScaler())
    ])


    categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])


    preprocessor = ColumnTransformer(
    transformers=[
    ('num', numeric_transformer, num_cols),
    ('cat', categorical_transformer, cat_cols)
    ], remainder='drop')


    return preprocessor, num_cols, cat_cols




def prepare_data(path: str):
    df = load_data(path)


    # utwórz kolumnę Risk 3-klasową jeśli trzeba
    df = create_multiclass_from_binary_or_features(df, target_col='Risk')


    # usuwanie duplikatów
    df = df.drop_duplicates().reset_index(drop=True)


    # buduj pipeline
    preprocessor, num_cols, cat_cols = build_preprocessing_pipeline(df)


    # oddziel X,y
    X = df.drop(columns=['Risk'])
    y = df['Risk'].astype(int)


    return X, y, preprocessor




def prepare_data_from_ucimlrepo():
    # Pobierz dane z UCI
    statlog_german_credit_data = fetch_ucirepo(id=144)
    X = statlog_german_credit_data.data.features
    y = statlog_german_credit_data.data.targets

    # Zmień nazwę kolumny celu na 'Risk', żeby zachować spójność z projektem
    y = y.rename(columns={'class': 'Risk'}).squeeze()  # .squeeze() konwertuje DF → Series

    y = (y.astype(int) - 1).astype(int)
    
    # Połącz X i y, aby pipeline mógł rozpoznać typy kolumn
    df = pd.concat([X, y], axis=1)

    # Zbuduj preprocessing pipeline (automatycznie wykryje typy)
    preprocessor, num_cols, cat_cols = build_preprocessing_pipeline(df)

    # Oddziel dane i etykiety
    X = df.drop(columns=['Risk'])
    y = df['Risk'].astype(int)

    return X, y, preprocessor
