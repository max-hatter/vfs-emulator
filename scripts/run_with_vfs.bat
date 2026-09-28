@echo off
REM Запуск эмулятора с указанием пути к VFS
cd /d "%~dp0\.."
python -m src.main --vfs data\vfs.csv
pause