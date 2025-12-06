@echo off
echo ========================================
echo   EnergiMate Ai - Starting Server...
echo ========================================
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting Flask server...
echo Open http://localhost:5000 in your browser
echo.
python app.py
pause

