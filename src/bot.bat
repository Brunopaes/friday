@echo off
setlocal EnableExtensions

:start_python_files
E:
cd E:\PythonProjects\Personal\friday\src

python friday.py

:check_python_files
call:infinite telegram_replier.py
goto:check_python_files

:infinite
tasklist /FI "WINDOWTITLE eq %1 - %2" | findstr /c:PID > nul
rem findstr /c:PID command added above to confirm that tasklist has found the process (errorlevel = 0). If not (errorlevel = 1).
if %errorlevel% EQU 1 (start "%1" "%2")