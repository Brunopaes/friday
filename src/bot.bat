@echo off
setlocal EnableExtensions

:start_python_files
D:
cd E:\PythonProjects\Personal\friday\src

python friday.py

:check_python_files
call:infinite telegram_replier.py
goto:check_python_files

:infinite
