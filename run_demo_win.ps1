# PowerShell helper to run SQLite local demo quickly
cd $PSScriptRoot
conda activate carecrew
python backend\setup_db.py
start powershell -NoExit -Command "python backend\run_demo.py ..\data\health_monitoring.csv"
Write-Host 'Demo started. Use the console window to view events. Close window to stop.'
