from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
import pandas as pd

def train_logistic_regression(X, y, preprocessor, output_dir='models', random_state=42):
    """
    Train Logistic Regression model for credit risk assessment.

    Args:
        X: Feature matrix
        y: Target variable
        preprocessor: Fitted preprocessor
        output_dir: Directory to save the model
        random_state: Random seed for reproducibility

    Returns:
        dict: Training results including model and accuracy
        X_test_trans: Transformed test features
        y_test: Test labels
    """
    os.makedirs(output_dir, exist_ok=True)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=random_state
    )

    # Transform features
    X_train_trans = preprocessor.fit_transform(X_train)
    X_test_trans = preprocessor.transform(X_test)

    # Apply SMOTE for balanced classes
    smote = SMOTE(random_state=random_state, k_neighbors=3)
    X_train_bal, y_train_bal = smote.fit_resample(X_train_trans, y_train)

    # Train Logistic Regression
    print("Trenuję model Logistic Regression...")
    model = LogisticRegression(
        max_iter=2000,
        multi_class='multinomial',
        solver='lbfgs',
        random_state=random_state
    )

    model.fit(X_train_bal, y_train_bal)

    # Evaluate
    y_pred = model.predict(X_test_trans)
    acc = accuracy_score(y_test, y_pred)
    print(f"Logistic Regression accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred))

    # Save model + preprocessor
    model_path = os.path.join(output_dir, 'LogisticRegression.pkl')
    joblib.dump(
        {'preprocessor': preprocessor, 'model': model},
        model_path
    )
    print(f"✓ Model zapisany: {model_path}")

    # Save results
    results_summary = pd.DataFrame([{
        'Model': 'LogisticRegression',
        'Accuracy': acc
    }])
    results_summary.to_csv(
        os.path.join(output_dir, 'model_results.csv'),
        index=False
    )

    # Save test data for evaluation
    joblib.dump({
        'X_test_trans': X_test_trans,
        'y_test': y_test,
        'preprocessor': preprocessor
    }, os.path.join(output_dir, 'test_data.pkl'))

    # Save full results for backward compatibility
    joblib.dump({
        'LogisticRegression': {
            'model': model,
            'accuracy': acc
        }
    }, os.path.join(output_dir, 'results_summary.pkl'))

    return {'LogisticRegression': {'model': model, 'accuracy': acc}}, X_test_trans, y_test
