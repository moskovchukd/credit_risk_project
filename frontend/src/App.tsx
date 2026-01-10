import { useState } from 'react';
import SurveyForm from './components/SurveyForm';
import ResultsDisplay from './components/ResultsDisplay';
import type { SurveyData, PredictionResult } from './types';

function App() {
  const [showResults, setShowResults] = useState(false);
  const [results, setResults] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (data: SurveyData) => {
    setLoading(true);
    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('Prediction failed');
      }

      const result = await response.json();
      setResults(result);
      setShowResults(true);
    } catch (error) {
      console.error('Error:', error);
      alert('Wystąpił błąd podczas przetwarzania Twojego wniosku. Spróbuj ponownie.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setShowResults(false);
    setResults(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-800 mb-3 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">
            Ocena Ryzyka Kredytowego
          </h1>
          <p className="text-xl text-gray-600">
            Wypełnij ankietę, aby ocenić swoją zdolność kredytową
          </p>
        </header>

        {!showResults ? (
          <SurveyForm onSubmit={handleSubmit} loading={loading} />
        ) : (
          <ResultsDisplay results={results} onReset={handleReset} />
        )}
      </div>
    </div>
  );
}

export default App;
