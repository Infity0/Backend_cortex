@echo off
echo ================================================
echo Starting Cortex AI Backend Server
echo ================================================
echo.
echo Server will start at: http://localhost:8000
echo API Docs: http://localhost:8000/api/docs
echo.
echo Press Ctrl+C to stop the server
echo.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
