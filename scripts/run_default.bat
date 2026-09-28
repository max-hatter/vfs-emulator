@echo off
REM Запуск эмулятора без параметров командной строки
cd /d "%~dp0\.."
python -m src.main
pause