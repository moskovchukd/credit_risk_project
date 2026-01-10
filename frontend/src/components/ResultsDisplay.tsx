import type { PredictionResult } from '../types';

interface ResultsDisplayProps {
  results: PredictionResult | null;
  onReset: () => void;
}

const ResultsDisplay = ({ results, onReset }: ResultsDisplayProps) => {
  if (!results) {
    return null;
  }

  const getRiskColor = (riskLevel: string) => {
    switch (riskLevel.toLowerCase()) {
      case 'low':
      case 'niskie':
        return 'green';
      case 'medium':
      case 'średnie':
        return 'yellow';
      case 'high':
      case 'wysokie':
        return 'red';
      default:
        return 'gray';
    }
  };

  const getRiskIcon = (riskLevel: string) => {
    const color = getRiskColor(riskLevel);
    if (color === 'green') {
      return (
        <svg className="w-24 h-24" fill="currentColor" viewBox="0 0 20 20">
          <path
            fillRule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
            clipRule="evenodd"
          />
        </svg>
      );
    } else if (color === 'yellow') {
      return (
        <svg className="w-24 h-24" fill="currentColor" viewBox="0 0 20 20">
          <path
            fillRule="evenodd"
            d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
            clipRule="evenodd"
          />
        </svg>
      );
    } else {
      return (
        <svg className="w-24 h-24" fill="currentColor" viewBox="0 0 20 20">
          <path
            fillRule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
            clipRule="evenodd"
          />
        </svg>
      );
    }
  };

  const getBackgroundGradient = (riskLevel: string) => {
    const color = getRiskColor(riskLevel);
    if (color === 'green') {
      return 'from-green-50 to-emerald-100';
    } else if (color === 'yellow') {
      return 'from-yellow-50 to-amber-100';
    } else {
      return 'from-red-50 to-pink-100';
    }
  };

  const getTextColor = (riskLevel: string) => {
    const color = getRiskColor(riskLevel);
    if (color === 'green') {
      return 'text-green-600';
    } else if (color === 'yellow') {
      return 'text-yellow-600';
    } else {
      return 'text-red-600';
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div
        className={`bg-gradient-to-br ${getBackgroundGradient(
          results.risk_level
        )} rounded-2xl shadow-2xl p-8 md:p-12 border-2 ${
          getRiskColor(results.risk_level) === 'green'
            ? 'border-green-200'
            : getRiskColor(results.risk_level) === 'yellow'
            ? 'border-yellow-200'
            : 'border-red-200'
        }`}
      >
        {/* Header with Icon */}
        <div className="text-center mb-8">
          <div className={`inline-block ${getTextColor(results.risk_level)} mb-4`}>
            {getRiskIcon(results.risk_level)}
          </div>
          <h2 className="text-4xl md:text-5xl font-bold text-gray-800 mb-4">
            Assessment Complete
          </h2>
        </div>

        {/* Decision */}
        <div className="bg-white rounded-xl p-8 mb-6 shadow-lg">
          <h3 className="text-2xl font-bold text-gray-800 mb-3">Credit Decision:</h3>
          <p className={`text-3xl font-bold ${getTextColor(results.risk_level)}`}>
            {results.decision}
          </p>
        </div>

        {/* Risk Level */}
        <div className="bg-white rounded-xl p-8 mb-6 shadow-lg">
          <h3 className="text-2xl font-bold text-gray-800 mb-3">Risk Level:</h3>
          <p className={`text-3xl font-bold ${getTextColor(results.risk_level)}`}>
            {results.risk_level.toUpperCase()}
          </p>
        </div>

        {/* Confidence */}
        <div className="bg-white rounded-xl p-8 mb-6 shadow-lg">
          <h3 className="text-2xl font-bold text-gray-800 mb-4">Decision Confidence:</h3>
          <div className="mb-3">
            <div className="flex justify-between mb-2">
              <span className="text-lg font-semibold text-gray-700">
                {(results.confidence * 100).toFixed(1)}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-6 overflow-hidden">
              <div
                className={`h-6 rounded-full transition-all duration-1000 ${
                  getRiskColor(results.risk_level) === 'green'
                    ? 'bg-gradient-to-r from-green-400 to-emerald-500'
                    : getRiskColor(results.risk_level) === 'yellow'
                    ? 'bg-gradient-to-r from-yellow-400 to-amber-500'
                    : 'bg-gradient-to-r from-red-400 to-pink-500'
                }`}
                style={{ width: `${results.confidence * 100}%` }}
              />
            </div>
          </div>
          <p className="text-sm text-gray-600 mt-2">
            {results.confidence >= 0.7
              ? 'High confidence in this assessment'
              : results.confidence >= 0.5
              ? 'Moderate confidence in this assessment'
              : 'Lower confidence - additional review may be needed'}
          </p>
        </div>

        {/* Probabilities */}
        {results.probabilities && results.probabilities.length > 0 && (
          <div className="bg-white rounded-xl p-8 shadow-lg">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Risk Probabilities:</h3>
            <div className="space-y-4">
              {results.probabilities.length === 2 ? (
                <>
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="font-semibold text-gray-700">Low Risk</span>
                      <span className="font-bold text-green-600">
                        {(results.probabilities[0] * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-4">
                      <div
                        className="bg-gradient-to-r from-green-400 to-emerald-500 h-4 rounded-full"
                        style={{ width: `${results.probabilities[0] * 100}%` }}
                      />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="font-semibold text-gray-700">High Risk</span>
                      <span className="font-bold text-red-600">
                        {(results.probabilities[1] * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-4">
                      <div
                        className="bg-gradient-to-r from-red-400 to-pink-500 h-4 rounded-full"
                        style={{ width: `${results.probabilities[1] * 100}%` }}
                      />
                    </div>
                  </div>
                </>
              ) : (
                <>
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="font-semibold text-gray-700">Low Risk</span>
                      <span className="font-bold text-green-600">
                        {(results.probabilities[0] * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-4">
                      <div
                        className="bg-gradient-to-r from-green-400 to-emerald-500 h-4 rounded-full"
                        style={{ width: `${results.probabilities[0] * 100}%` }}
                      />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="font-semibold text-gray-700">Medium Risk</span>
                      <span className="font-bold text-yellow-600">
                        {(results.probabilities[1] * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-4">
                      <div
                        className="bg-gradient-to-r from-yellow-400 to-amber-500 h-4 rounded-full"
                        style={{ width: `${results.probabilities[1] * 100}%` }}
                      />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="font-semibold text-gray-700">High Risk</span>
                      <span className="font-bold text-red-600">
                        {(results.probabilities[2] * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-4">
                      <div
                        className="bg-gradient-to-r from-red-400 to-pink-500 h-4 rounded-full"
                        style={{ width: `${results.probabilities[2] * 100}%` }}
                      />
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>
        )}

        {/* Reset Button */}
        <div className="mt-8 text-center">
          <button
            onClick={onReset}
            className="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-semibold text-lg hover:shadow-lg hover:scale-105 transition-all duration-200"
          >
            Start New Assessment
          </button>
        </div>
      </div>
    </div>
  );
};

export default ResultsDisplay;
