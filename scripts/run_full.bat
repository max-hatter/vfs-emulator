@echo off
REM Запуск эмулятора со всеми параметрами
cd /d "%~dp0\.."
python -m src.main --vfs data\vfs.csv --script scripts\startup.txt
pause