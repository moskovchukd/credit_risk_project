import { useState } from 'react';
import type { SurveyData } from '../types';
import { surveyQuestions } from '../data/questions';

interface SurveyFormProps {
  onSubmit: (data: SurveyData) => void;
  loading: boolean;
}

const SurveyForm = ({ onSubmit, loading }: SurveyFormProps) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState<Partial<SurveyData>>({});
  const [errors, setErrors] = useState<Record<string, string>>({});

  const totalSteps = surveyQuestions.length;
  const currentQuestion = surveyQuestions[currentStep];
  const progress = ((currentStep + 1) / totalSteps) * 100;

  const handleInputChange = (value: string | number) => {
    setFormData({
      ...formData,
      [currentQuestion.attribute]: value,
    });
    setErrors({ ...errors, [currentQuestion.attribute]: '' });
  };

  const validateCurrentStep = (): boolean => {
    const value = formData[currentQuestion.attribute as keyof SurveyData];

    if (value === undefined || value === '' || value === null) {
      setErrors({ ...errors, [currentQuestion.attribute]: 'This field is required' });
      return false;
    }

    if (currentQuestion.type === 'number') {
      const numValue = Number(value);
      if (isNaN(numValue) || numValue < 0) {
        setErrors({ ...errors, [currentQuestion.attribute]: 'Please enter a valid positive number' });
        return false;
      }
    }

    return true;
  };

  const handleNext = () => {
    if (validateCurrentStep()) {
      if (currentStep < totalSteps - 1) {
        setCurrentStep(currentStep + 1);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handleSubmit = () => {
    if (validateCurrentStep()) {
      onSubmit(formData as SurveyData);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">
            Question {currentStep + 1} of {totalSteps}
          </span>
          <span className="text-sm font-medium text-gray-700">
            {Math.round(progress)}% Complete
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
          <div
            className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-500 ease-out"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Question Card */}
      <div className="bg-white rounded-2xl shadow-xl p-8 md:p-12 border border-gray-100">
        <div className="mb-8">
          <h2 className="text-2xl md:text-3xl font-bold text-gray-800 mb-4">
            {currentQuestion.question}
          </h2>

          {currentQuestion.type === 'select' && currentQuestion.options && (
            <div className="space-y-3">
              {currentQuestion.options.map((option) => (
                <label
                  key={option.code}
                  className={`flex items-start p-4 border-2 rounded-xl cursor-pointer transition-all duration-200 hover:border-blue-400 hover:bg-blue-50 ${
                    formData[currentQuestion.attribute as keyof SurveyData] === option.code
                      ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200'
                      : 'border-gray-200'
                  }`}
                >
                  <input
                    type="radio"
                    name={currentQuestion.attribute}
                    value={option.code}
                    checked={formData[currentQuestion.attribute as keyof SurveyData] === option.code}
                    onChange={(e) => handleInputChange(e.target.value)}
                    className="mt-1 h-5 w-5 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="ml-3 text-gray-700 font-medium">{option.label}</span>
                </label>
              ))}
            </div>
          )}

          {currentQuestion.type === 'number' && (
            <div className="mt-4">
              <input
                type="number"
                min="0"
                value={formData[currentQuestion.attribute as keyof SurveyData] || ''}
                onChange={(e) => handleInputChange(Number(e.target.value))}
                className="w-full px-6 py-4 text-lg border-2 border-gray-300 rounded-xl focus:border-blue-500 focus:ring-4 focus:ring-blue-200 transition-all duration-200"
                placeholder="Enter a number"
              />
              {currentQuestion.unit && (
                <p className="mt-2 text-sm text-gray-500">Unit: {currentQuestion.unit}</p>
              )}
            </div>
          )}

          {errors[currentQuestion.attribute] && (
            <p className="mt-3 text-red-600 font-medium flex items-center">
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                  clipRule="evenodd"
                />
              </svg>
              {errors[currentQuestion.attribute]}
            </p>
          )}
        </div>

        {/* Navigation Buttons */}
        <div className="flex justify-between items-center pt-6 border-t border-gray-200">
          <button
            onClick={handlePrevious}
            disabled={currentStep === 0}
            className={`px-6 py-3 rounded-xl font-semibold transition-all duration-200 ${
              currentStep === 0
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300 hover:shadow-md'
            }`}
          >
            ← Previous
          </button>

          {currentStep < totalSteps - 1 ? (
            <button
              onClick={handleNext}
              className="px-8 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-semibold hover:shadow-lg hover:scale-105 transition-all duration-200"
            >
              Next →
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={loading}
              className="px-8 py-3 bg-gradient-to-r from-green-500 to-blue-600 text-white rounded-xl font-semibold hover:shadow-lg hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
            >
              {loading ? (
                <span className="flex items-center">
                  <svg
                    className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
                  Analyzing...
                </span>
              ) : (
                'Submit & Get Results'
              )}
            </button>
          )}
        </div>
      </div>

      {/* Step Indicators */}
      <div className="mt-8 flex justify-center space-x-2">
        {surveyQuestions.map((_, index) => (
          <div
            key={index}
            className={`h-2 rounded-full transition-all duration-300 ${
              index === currentStep
                ? 'w-8 bg-blue-600'
                : index < currentStep
                ? 'w-2 bg-green-500'
                : 'w-2 bg-gray-300'
            }`}
          />
        ))}
      </div>
    </div>
  );
};

export default SurveyForm;
