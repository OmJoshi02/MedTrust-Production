@echo off
setlocal
echo ==========================================================
echo MEDTRUST V1 - PRODUCTION ENVIRONMENT
echo ==========================================================
echo Starting MedTrust unified server on http://localhost:8000
echo Serving API and pre-compiled React single-page frontend...
echo Opening your web browser automatically...
echo Press Ctrl+C to terminate the server.
echo.

set MEDTRUST_ENV=production
set MEDTRUST_SECURE_COOKIES=0
set PYTHONPATH=%CD%
start http://localhost:8000
python backend\server.py
