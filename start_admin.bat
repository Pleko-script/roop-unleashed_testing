@echo off

:: Setze Umgebungsvariablen
set ROOP_SERVER_SHARE=true
set GRADIO_SERVER_NAME=0.0.0.0

:: Upgrade Gradio (optional)
pip install --upgrade gradio

:: Starte das Admin Interface
python admin.py

pause