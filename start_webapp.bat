@echo off
REM Credit Risk Assessment Web App Startup Script for Windows
REM This script starts both the backend API and frontend dev server

echo ======================================
echo   Credit Risk Assessment Web App
echo ======================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo        Please create one first: python -m venv venv
    exit /b 1
)

REM Check if models exist
if not exist "models\LogisticRegression.pkl" (
    echo ERROR: Trained models not found!
    echo        Please train the model first: python run_train.py
    exit /b 1
)

REM Check if frontend dependencies are installed
if not exist "frontend\node_modules\" (
    echo ERROR: Frontend dependencies not installed!
    echo        Please run: cd frontend ^&^& npm install
    exit /b 1
)

echo All prerequisites met!
echo.
echo Starting servers...
echo.

REM Start backend server in a new window
echo Starting Backend API on http://localhost:5001
start "Backend API" cmd /k "venv\Scripts\activate && python api\app.py"

REM Wait a bit for backend to start
timeout /t 3 /nobreak > nul

REM Start frontend server in a new window
echo Starting Frontend on http://localhost:5173
start "Frontend Dev Server" cmd /k "cd frontend && npm run dev"

echo.
echo ======================================
echo   Application is running!
echo ======================================
echo.
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:5001
echo.
echo   Close the terminal windows to stop
echo ======================================
echo.

pause
