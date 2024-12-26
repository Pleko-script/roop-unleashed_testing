@echo off

:: Starte Roop
start /B python run.py

:: Warte kurz
timeout /t 2

:: Starte Admin Interface
python admin.py