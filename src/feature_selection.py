from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
import numpy as np




def select_k_best(X, y, preprocessor, k=20):

# dopasuj preprocessor i transformuj X
    X_trans = preprocessor.fit_transform(X)


    selector = SelectKBest(score_func=f_classif, k=min(k, X_trans.shape[1]))
    selector.fit(X_trans, y)


    mask = selector.get_support()
    return selector, mask




def rf_feature_importances(X, y, preprocessor, top_n=20, random_state=42):
    X_trans = preprocessor.fit_transform(X)
    rf = RandomForestClassifier(n_estimators=200, random_state=random_state)
    rf.fit(X_trans, y)
    importances = rf.feature_importances_
    # zwróć indeksy posortowane
    idx = np.argsort(importances)[::-1][:top_n]
    return idx, importances