import pandas as pd
import joblib
import os
import numpy as np


class CreditRiskPredictor:
  
    def __init__(self, model_path):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model nie został znaleziony: {model_path}")
        
        saved_objects = joblib.load(model_path)
        self.model = saved_objects['model']
        self.preprocessor = saved_objects['preprocessor']
        self.model_name = os.path.basename(model_path).replace('.pkl', '')
        
        print(f"✓ Załadowano model: {self.model_name}")
    
    def predict(self, X):
        if not isinstance(X, pd.DataFrame):
            raise ValueError("Dane wejściowe muszą być DataFrame")
        
        if 'Risk' in X.columns:
            X = X.drop(columns=['Risk'])
        
        X_transformed = self.preprocessor.transform(X)
        
        predictions = self.model.predict(X_transformed)
        
        return predictions
    
    def predict_proba(self, X):
       
        if 'Risk' in X.columns:
            X = X.drop(columns=['Risk'])
        
        X_transformed = self.preprocessor.transform(X)
        
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(X_transformed)
            return probabilities
        else:
            raise AttributeError(f"Model {self.model_name} nie wspiera predict_proba")
    
    def predict_single(self, data_dict):
        
        df = pd.DataFrame([data_dict])
        prediction = self.predict(df)
        return prediction[0]
    
    def predict_with_details(self, X):
       
        predictions = self.predict(X)
        
        result_df = X.copy()
        result_df['Predicted_Risk'] = predictions
        
       
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.predict_proba(X)
            n_classes = probabilities.shape[1]
        else:
            n_classes = len(set(predictions))
        
     
        if n_classes == 2:
            risk_labels = {0: 'good', 1: 'bad'}
            result_df['Risk_Label'] = result_df['Predicted_Risk'].map(risk_labels)
            
            if hasattr(self.model, 'predict_proba'):
                result_df['Prob_Good'] = probabilities[:, 0]
                result_df['Prob_Bad'] = probabilities[:, 1]
                result_df['Confidence'] = probabilities.max(axis=1)
        elif n_classes == 3:
            risk_labels = {0: 'low', 1: 'medium', 2: 'high'}
            result_df['Risk_Label'] = result_df['Predicted_Risk'].map(risk_labels)
            
            if hasattr(self.model, 'predict_proba'):
                result_df['Prob_Low'] = probabilities[:, 0]
                result_df['Prob_Medium'] = probabilities[:, 1]
                result_df['Prob_High'] = probabilities[:, 2]
                result_df['Confidence'] = probabilities.max(axis=1)
        else:
            result_df['Risk_Label'] = result_df['Predicted_Risk'].astype(str)
            
            if hasattr(self.model, 'predict_proba'):
                for i in range(n_classes):
                    result_df[f'Prob_Class_{i}'] = probabilities[:, i]
                result_df['Confidence'] = probabilities.max(axis=1)
        
        return result_df


def load_best_model(models_dir='models', metric='accuracy'):
   
    results_path = os.path.join(models_dir, 'model_results.csv')
    
    if not os.path.exists(results_path):
        raise FileNotFoundError(f"Nie znaleziono pliku z wynikami: {results_path}")
    
    results_df = pd.read_csv(results_path)
    best_model_name = results_df.loc[results_df['Accuracy'].idxmax(), 'Model']
    best_accuracy = results_df['Accuracy'].max()
    
    print(f"Najlepszy model: {best_model_name} (accuracy: {best_accuracy:.4f})")
    
    model_path = os.path.join(models_dir, f'{best_model_name}.pkl')
    return CreditRiskPredictor(model_path)


def compare_models_predictions(X, models_dir='models'):
   
    model_files = [f for f in os.listdir(models_dir) if f.endswith('.pkl') and f != 'results_summary.pkl']
    
    predictions_dict = {}
    
    for model_file in model_files:
        model_name = model_file.replace('.pkl', '')
        try:
            predictor = CreditRiskPredictor(os.path.join(models_dir, model_file))
            predictions = predictor.predict(X)
            predictions_dict[model_name] = predictions
        except Exception as e:
            print(f"Błąd podczas ładowania {model_name}: {e}")
    

    comparison_df = pd.DataFrame(predictions_dict)

    comparison_df['Voting'] = comparison_df.mode(axis=1)[0]
    
    return comparison_df

