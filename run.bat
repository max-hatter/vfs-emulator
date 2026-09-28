@echo off
REM Скрипт запуска эмулятора VFS (Вариант 27)
REM Запускает со всеми параметрами по умолчанию.

cd /d "%~dp0"
python -m src.main --vfs data\vfs.csv --script scripts\startup.txt