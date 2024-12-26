import gradio as gr
import os
import zipfile
import subprocess
import time
from google.colab import files

# Konfiguration
OUTPUT_PATH = "output"  
ROOP_PROCESS = None

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

# Erstelle das Gradio Interface
with gr.Blocks(title="Roop Admin Interface für Colab") as admin_interface:
    with gr.Row():
        gr.Markdown("# Roop Admin Interface für Google Colab")
    
    with gr.Row():
        with gr.Column(scale=1):
            download_btn = gr.Button("Download als ZIP", variant="primary")
            status_download = gr.Textbox(label="Download Status", interactive=False)
    
    with gr.Row():
        with gr.Column(scale=1):
            restart_btn = gr.Button("Restart Roop", variant="primary")
            status_output = gr.Textbox(label="Status", interactive=False)
            
    # Event Handler
    download_btn.click(create_zip_from_output, outputs=status_download)
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
        server_port=7861,  # Anderer Port als Roop
        server_name="0.0.0.0"  # Erlaubt externe Verbindungen
    )