@echo off
REM Test runner script for CuratorAI backend (Windows)

echo 🧪 Running CuratorAI API Tests
echo ================================
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

REM Run pytest with coverage
python -m pytest apps/ ^
    --verbose ^
    --tb=short ^
    --cov=apps ^
    --cov-report=html ^
    --cov-report=term ^
    --cov-report=json ^
    -p no:warnings

echo.
echo ✅ Tests completed!
echo 📊 Coverage report generated in htmlcov\index.html

pause

