# Web App Quick Start Guide

Get the Credit Risk Assessment web app running in 3 simple steps!

## Quick Setup (First Time Only)

### 1. Install Backend Dependencies

```bash
# Install Python packages (includes Flask)
pip install -r requirements.txt
```

### 2. Train the Model

```bash
# Train the ML model (takes a few minutes)
python run_train.py
```

### 3. Install Frontend Dependencies

```bash
# Install Node packages
cd frontend
npm install
cd ..
```

## Running the App

### Option 1: Automatic (Recommended)

**Mac/Linux:**
```bash
./start_webapp.sh
```

**Windows:**
```bash
start_webapp.bat
```

This will automatically start both the backend and frontend servers.

### Option 2: Manual

**Terminal 1 - Backend:**
```bash
source venv/bin/activate  # Windows: venv\Scripts\activate
python api/app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Access the App

Open your browser and go to: **http://localhost:5173**

## What You'll See

1. **Landing Page**: Beautiful gradient design with title
2. **Survey Form**: 20 questions with step-by-step navigation
3. **Progress Bar**: Shows completion percentage
4. **Results Page**: Credit risk assessment with:
   - Approval/Rejection decision
   - Risk level visualization
   - Confidence percentage
   - Probability breakdown with charts

## Troubleshooting

**Models not found?**
```bash
python run_train.py
```

**Flask not installed?**
```bash
pip install flask flask-cors
```

**Frontend dependencies missing?**
```bash
cd frontend && npm install
```

**Port 5001 already in use?**
- Edit `api/app.py` and change the port number

**Port 5173 already in use?**
- Vite will automatically use the next available port

## Tech Stack

- **Frontend**: React + TypeScript + Tailwind CSS
- **Backend**: Flask + scikit-learn
- **ML Model**: Logistic Regression

## For More Details

See [WEB_APP_README.md](WEB_APP_README.md) for comprehensive documentation.

---

Made with ❤️ by Danylo Moskovchuk and Nazar Marakhovkyi
