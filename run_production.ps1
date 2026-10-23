Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "MEDTRUST V1 - PRODUCTION ENVIRONMENT" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Starting MedTrust unified server on http://localhost:8000" -ForegroundColor Green
Write-Host "Serving API and pre-compiled React single-page frontend..." -ForegroundColor Green
Write-Host "Opening web browser at http://localhost:8000 ..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to terminate the server." -ForegroundColor Yellow
Write-Host ""

$env:MEDTRUST_ENV = "production"
$env:MEDTRUST_SECURE_COOKIES = "0"
$env:PYTHONPATH = $PSScriptRoot
Set-Location -Path $PSScriptRoot
Start-Process "http://localhost:8000"
python backend/server.py
