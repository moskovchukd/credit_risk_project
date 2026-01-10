"""
Flask API for Credit Risk Assessment
Provides REST endpoints for the React frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import sys
import os

# Add parent directory to path to import src modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.predict import CreditRiskPredictor

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the model at startup
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'LogisticRegression.pkl')
predictor = None

try:
    predictor = CreditRiskPredictor(MODEL_PATH)
    print(f"✓ Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    print("  Make sure you've trained the model by running: python run_train.py")


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor is not None
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict credit risk based on survey data

    Expected JSON format:
    {
        "Attribute1": "A13",
        "Attribute2": 24,
        "Attribute3": "A32",
        ...
        "Attribute20": "A202"
    }

    Returns:
    {
        "prediction": 0 or 1 (0 = low risk, 1 = high risk),
        "probabilities": [0.91, 0.09],
        "risk_level": "Low" or "High",
        "decision": "APPROVED" or "REJECTED",
        "confidence": 0.91
    }
    """
    if predictor is None:
        return jsonify({
            'error': 'Model not loaded. Please train the model first by running: python run_train.py'
        }), 500

    try:
        # Get data from request
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate that all required attributes are present
        required_attributes = [f'Attribute{i}' for i in range(1, 21)]
        missing_attributes = [attr for attr in required_attributes if attr not in data]

        if missing_attributes:
            return jsonify({
                'error': 'Missing required attributes',
                'missing': missing_attributes
            }), 400

        # Create DataFrame
        df = pd.DataFrame([data])

        # Make prediction
        prediction = predictor.predict(df)[0]

        # Get probabilities if available
        probabilities = None
        if hasattr(predictor.model, 'predict_proba'):
            proba = predictor.predict_proba(df)[0]
            probabilities = proba.tolist()

        # Determine risk level and decision
        n_classes = len(probabilities) if probabilities else 2

        if n_classes == 2:
            # Binary classification
            if prediction == 0:
                risk_level = "Niskie"
                decision = "ZATWIERDZONY - Klient jest wiarygodny kredytowo"
            else:
                risk_level = "Wysokie"
                decision = "ODRZUCONY - Klient stanowi wysokie ryzyko kredytowe"
        else:
            # Multi-class classification
            risk_labels = {0: 'Niskie', 1: 'Średnie', 2: 'Wysokie'}
            risk_decisions = {
                0: 'ZATWIERDZONY - Klient jest wiarygodny kredytowo',
                1: 'WYMAGA DODATKOWEJ WERYFIKACJI - Klient wymaga dodatkowej analizy',
                2: 'ODRZUCONY - Klient stanowi wysokie ryzyko kredytowe'
            }
            risk_level = risk_labels.get(prediction, 'Nieznane')
            decision = risk_decisions.get(prediction, 'Nieznane')

        # Calculate confidence (max probability)
        confidence = max(probabilities) if probabilities else 0.0

        return jsonify({
            'prediction': int(prediction),
            'probabilities': probabilities,
            'risk_level': risk_level,
            'decision': decision,
            'confidence': float(confidence)
        })

    except Exception as e:
        print(f"Error during prediction: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Prediction failed: {str(e)}'
        }), 500


@app.route('/api/questions', methods=['GET'])
def get_questions():
    """
    Get survey questions metadata
    This endpoint can be used to dynamically load questions if needed
    """
    return jsonify({
        'message': 'Questions are currently hardcoded in frontend',
        'total_questions': 20
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  CREDIT RISK ASSESSMENT API")
    print("="*60)
    print(f"\nModel Status: {'✓ Loaded' if predictor else '✗ Not Loaded'}")
    print("\nAvailable endpoints:")
    print("  GET  /api/health   - Health check")
    print("  POST /api/predict  - Make credit risk prediction")
    print("  GET  /api/questions - Get questions metadata")
    print("\nStarting server on http://localhost:5001")
    print("="*60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5001)
