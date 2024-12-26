import gradio as gr
import os
import zipfile
import subprocess
import shutil
import sys
from pathlib import Path
from google.colab import files
import time

# Konfiguration
OUTPUT_PATH = "output"  # Der Pfad zum Output-Ordner
ROOP_PROCESS = None
ADMIN_PORT = 7861
ROOP_PORT = 7860

def create_zip_from_output():
    """Erstellt ein Zip-Archiv aus dem Output-Ordner und lädt es herunter"""
    if not os.path.exists(OUTPUT_PATH):
        return "Output-Ordner existiert nicht!"
    
    zip_path = os.path.join(OUTPUT_PATH, "output_files.zip")
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(OUTPUT_PATH):
                for file in files:
                    if file != "output_files.zip":  # Exclude the zip file itself
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, OUTPUT_PATH)
                        zipf.write(file_path, arcname)
        
        # Für Colab: Direkt den Download starten
        files.download(zip_path)
        return "Download gestartet"
    except Exception as e:
        return f"Fehler beim Erstellen des ZIP-Archivs: {str(e)}"

def restart_roop():
    """Startet den Roop-Prozess neu"""
    global ROOP_PROCESS
    
    try:
        # Beende den existierenden Prozess
        if ROOP_PROCESS:
            ROOP_PROCESS.terminate()
            time.sleep(1)
            if ROOP_PROCESS.poll() is None:
                ROOP_PROCESS.kill()
        
        # Warte kurz
        time.sleep(2)
        
        # Setze die Umgebungsvariable für Server Share
        env = os.environ.copy()
        env['ROOP_SERVER_SHARE'] = 'true'
        
        # Starte Roop neu mit Share Option
        ROOP_PROCESS = subprocess.Popen(
            ['python', 'run.py'],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        # Warte und suche nach der öffentlichen URL
        time.sleep(10)
        for line in ROOP_PROCESS.stdout:
            if "gradio.live" in line:
                return f"Roop neu gestartet. Öffentliche URL: {line.strip()}"
            
        return "Roop wurde neu gestartet, aber keine öffentliche URL gefunden."
    except Exception as e:
        return f"Fehler beim Neustarten von Roop: {str(e)}"

def mount_google_drive():
    """Verbindet Google Drive"""
    try:
        from google.colab import drive
        drive.mount('/content/drive')
        return "Google Drive erfolgreich verbunden"
    except Exception as e:
        return f"Fehler beim Verbinden von Google Drive: {str(e)}"

def copy_to_drive():
    """Kopiert den Output-Ordner nach Google Drive"""
    try:
        drive_path = "/content/drive/MyDrive/roop_output"
        os.makedirs(drive_path, exist_ok=True)
        
        # Kopiere alle Dateien aus dem Output-Ordner
        for item in os.listdir(OUTPUT_PATH):
            s = os.path.join(OUTPUT_PATH, item)
            d = os.path.join(drive_path, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)
        
        return f"Dateien nach {drive_path} kopiert"
    except Exception as e:
        return f"Fehler beim Kopieren nach Google Drive: {str(e)}"

# Erstelle das Gradio Interface
with gr.Blocks(title="Roop Admin Interface für Colab") as admin_interface:
    with gr.Row():
        gr.Markdown("# Roop Admin Interface für Google Colab")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("""
            ## Download
            Lade verarbeitete Dateien herunter oder speichere sie auf Google Drive
            """)
            download_btn = gr.Button("Download als ZIP", variant="primary")
            status_download = gr.Textbox(label="Download Status", interactive=False)
            
            mount_drive_btn = gr.Button("Google Drive verbinden", variant="secondary")
            copy_drive_btn = gr.Button("Nach Google Drive kopieren", variant="secondary")
            status_drive = gr.Textbox(label="Drive Status", interactive=False)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("""
            ## Roop Verwaltung
            Verwalte den Roop-Prozess und siehe den öffentlichen Link
            """)
            restart_btn = gr.Button("Restart Roop", variant="primary")
            status_output = gr.Textbox(label="Status", interactive=False)
            
    # Event Handler
    download_btn.click(create_zip_from_output, outputs=status_download)
    mount_drive_btn.click(mount_google_drive, outputs=status_drive)
    copy_drive_btn.click(copy_to_drive, outputs=status_drive)
    restart_btn.click(restart_roop, outputs=status_output)

# Starte das Admin Interface
if __name__ == "__main__":
    # Starte zuerst Roop
    env = os.environ.copy()
    env['ROOP_SERVER_SHARE'] = 'true'
    
    ROOP_PROCESS = subprocess.Popen(['python', 'run.py'], env=env)
    
    # Warte kurz damit Roop starten kann
    time.sleep(5)
    
    # Dann starte das Admin Interface
    admin_interface.launch(
        share=True,  # Erstellt einen öffentlichen Link
        server_port=ADMIN_PORT,
        server_name="0.0.0.0"  # Erlaubt externe Verbindungen
    )