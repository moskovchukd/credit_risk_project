from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from imblearn.over_sampling import SMOTE
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
import pandas as pd




def train_and_compare(X, y, preprocessor, output_dir='models', random_state=42):
    os.makedirs(output_dir, exist_ok=True)


    # podział na zbiór treningowy/testowy
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=random_state)


    X_train_trans = preprocessor.fit_transform(X_train)
    X_test_trans = preprocessor.transform(X_test)


    smote = SMOTE(random_state=random_state)
    X_train_bal, y_train_bal = smote.fit_resample(X_train_trans, y_train)


    models = {
    'LogisticRegression': LogisticRegression(max_iter=2000),
    'RandomForest': RandomForestClassifier(n_estimators=200),
    'XGBoost': XGBClassifier(use_label_encoder=False, eval_metric='mlogloss'),
    'SVM': SVC(probability=True),
    'KNN': KNeighborsClassifier()
    }


    results = {}


    for name, model in models.items():
        print(f"Trenuję {name}...")


        # GridSearchCV dla RandomForest i XGBoost
        if name in ['RandomForest', 'XGBoost']:
            param_grid = {
            'RandomForest': {'n_estimators': [100, 200], 'max_depth': [None, 5, 10]},
            'XGBoost': {'n_estimators': [100, 200], 'max_depth': [3, 5, 7]}
            }[name]
            grid = GridSearchCV(model, param_grid, cv=3, scoring='accuracy')
            grid.fit(X_train_bal, y_train_bal)
            model = grid.best_estimator_
            print('Najlepsze parametry:', grid.best_params_)


        else:
            model.fit(X_train_bal, y_train_bal)


        y_pred = model.predict(X_test_trans)
        acc = accuracy_score(y_test, y_pred)
        print(f"{name} accuracy: {acc:.4f}")
        print(classification_report(y_test, y_pred))


    # zapis modelu + preprocessor
        joblib.dump({'preprocessor': preprocessor, 'model': model}, os.path.join(output_dir, f'{name}.pkl'))


        results[name] = {'model': model, 'accuracy': acc}


    # zapis wyników do CSV
    results_summary = [{'Model': k, 'Accuracy': v['accuracy']} for k,v in results.items()]
    pd.DataFrame(results_summary).to_csv(os.path.join(output_dir, 'model_results.csv'), index=False)


    # zapis podsumowania jako pickle
    joblib.dump(results, os.path.join(output_dir, 'results_summary.pkl'))
    return results