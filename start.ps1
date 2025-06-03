# PowerShell script to run the Flask Forms application
# Sets the correct Python path and starts the server

$PYTHON_PATH = "C:\Users\Abdelrahman\AppData\Local\Programs\Python\Python312\python.exe"

Write-Host "Starting Flask Forms Application..." -ForegroundColor Green
Write-Host "Python: $PYTHON_PATH" -ForegroundColor Yellow
Write-Host "Server will be available at: http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ("-" * 50) -ForegroundColor Gray

& $PYTHON_PATH run.py
