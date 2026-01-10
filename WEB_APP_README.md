# Credit Risk Assessment Web Application

A modern, full-stack web application for assessing credit risk through an interactive survey. Built with React, TypeScript, Tailwind CSS, and Flask.

## Features

- **Modern, Responsive UI**: Beautiful gradient design that works on all devices
- **Interactive Survey**: 20 questions with step-by-step navigation
- **Real-time Progress**: Visual progress bar showing completion percentage
- **Instant Results**: Immediate credit risk assessment with detailed probability breakdown
- **Professional Design**: Clean, modern interface with smooth animations

## Architecture

### Frontend (React + TypeScript + Tailwind CSS)
- **Location**: `/frontend`
- **Framework**: React with Vite
- **Styling**: Tailwind CSS v4
- **Components**:
  - `SurveyForm.tsx`: Multi-step survey with validation
  - `ResultsDisplay.tsx`: Beautiful results visualization
  - `App.tsx`: Main application logic

### Backend (Flask API)
- **Location**: `/api`
- **Framework**: Flask with Flask-CORS
- **ML Model**: Logistic Regression (pre-trained)
- **Endpoints**:
  - `GET /api/health`: Health check
  - `POST /api/predict`: Credit risk prediction
  - `GET /api/questions`: Questions metadata

## Prerequisites

1. **Python 3.8+** with venv
2. **Node.js 18+** and npm
3. **Trained ML model** (run `python run_train.py` if not already done)

## Installation

### 1. Install Python Dependencies

```bash
# Create and activate virtual environment (if not already done)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (includes Flask)
pip install -r requirements.txt
```

### 2. Train the Model (if not already done)

```bash
python run_train.py
```

This will create trained models in the `models/` directory.

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
```

## Running the Application

You need to run both the backend and frontend servers:

### Terminal 1: Start the Backend API

```bash
# From project root
source venv/bin/activate  # On Windows: venv\Scripts\activate
python api/app.py
```

The API will start on `http://localhost:5001`

### Terminal 2: Start the Frontend

```bash
# From project root
cd frontend
npm run dev
```

The app will start on `http://localhost:5173` (or another port if 5173 is busy)

### Access the Application

Open your browser and navigate to: **http://localhost:5173**

## How to Use

1. **Start the Survey**: Click through the welcome screen
2. **Answer Questions**: Respond to all 20 questions
   - Use radio buttons for multiple choice
   - Enter numbers for quantitative fields
3. **Navigate**: Use "Next" and "Previous" buttons
4. **Submit**: Click "Submit & Get Results" on the last question
5. **View Results**: See your credit risk assessment with:
   - Approval/Rejection decision
   - Risk level (Low/High or Low/Medium/High)
   - Confidence percentage
   - Probability breakdown
6. **Start Over**: Click "Start New Assessment" to begin again

## API Documentation

### POST /api/predict

**Request Body:**
```json
{
  "Attribute1": "A13",
  "Attribute2": 24,
  "Attribute3": "A32",
  "Attribute4": "A43",
  "Attribute5": 5000,
  "Attribute6": "A61",
  "Attribute7": "A75",
  "Attribute8": 4,
  "Attribute9": "A93",
  "Attribute10": "A101",
  "Attribute11": 4,
  "Attribute12": "A121",
  "Attribute13": 35,
  "Attribute14": "A143",
  "Attribute15": "A152",
  "Attribute16": 1,
  "Attribute17": "A173",
  "Attribute18": 1,
  "Attribute19": "A192",
  "Attribute20": "A202"
}
```

**Response:**
```json
{
  "prediction": 0,
  "probabilities": [0.91, 0.09],
  "risk_level": "Low",
  "decision": "APPROVED - Client is creditworthy",
  "confidence": 0.91
}
```

## Project Structure

```
credit_risk_project/
├── frontend/                    # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── SurveyForm.tsx       # Survey component
│   │   │   └── ResultsDisplay.tsx   # Results component
│   │   ├── data/
│   │   │   └── questions.ts         # Survey questions data
│   │   ├── App.tsx                  # Main app component
│   │   ├── main.tsx                 # Entry point
│   │   └── index.css                # Tailwind styles
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── api/
│   └── app.py                   # Flask API server
├── models/                      # Trained ML models
│   └── LogisticRegression.pkl
├── src/                         # Python ML modules
│   ├── predict.py
│   ├── preprocessing.py
│   └── ...
├── requirements.txt             # Python dependencies
└── WEB_APP_README.md           # This file
```

## Development

### Frontend Development

```bash
cd frontend
npm run dev      # Start dev server with hot reload
npm run build    # Build for production
npm run preview  # Preview production build
```

### Backend Development

The Flask server runs in debug mode by default, which includes:
- Auto-reload on code changes
- Detailed error messages
- CORS enabled for local development

### Making Changes

**Frontend:**
- Components are in `/frontend/src/components/`
- Questions data is in `/frontend/src/data/questions.ts`
- Styles use Tailwind CSS utility classes

**Backend:**
- API logic is in `/api/app.py`
- ML prediction uses `/src/predict.py`

## Troubleshooting

### Backend Issues

**Problem**: "Model not loaded" error
**Solution**: Train the model first:
```bash
python run_train.py
```

**Problem**: Port 5000 already in use
**Solution**: Change the port in `/api/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

### Frontend Issues

**Problem**: API calls failing
**Solution**:
1. Make sure backend is running on `http://localhost:5001`
2. Check the proxy settings in `/frontend/vite.config.ts`

**Problem**: Tailwind styles not working
**Solution**:
```bash
cd frontend
npm install -D tailwindcss postcss autoprefixer
```

**Problem**: TypeScript errors
**Solution**:
```bash
cd frontend
npm install -D @types/react @types/react-dom
```

## Production Deployment

### Build Frontend

```bash
cd frontend
npm run build
```

This creates optimized files in `/frontend/dist/`

### Serve Frontend + Backend

You can:
1. **Use Flask to serve static files**: Modify `api/app.py` to serve the built frontend
2. **Use separate servers**: Deploy frontend to Vercel/Netlify and backend to Heroku/AWS
3. **Use a reverse proxy**: Nginx to route frontend and API requests

### Environment Variables

For production, set:
- `FLASK_ENV=production`
- Update CORS settings in `api/app.py` to allow only your domain

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License

This project is part of the Credit Risk Assessment system by Danylo Moskovchuk and Nazar Marakhovkyi.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the original project README.md
3. Contact the project authors
