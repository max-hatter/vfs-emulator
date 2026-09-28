@echo off
REM Запуск эмулятора со стартовым скриптом
cd /d "%~dp0\.."
python -m src.main --script scripts\startup.txt
pause