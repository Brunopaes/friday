@echo off
setlocal EnableExtensions

:start_python_files
E:
cd E:\PythonProjects\Personal\friday\src

python friday_telegram.py
python friday_discord.py

:check_python_files
call:infinite telegram_replier.py
goto:check_python_files

:infinite
