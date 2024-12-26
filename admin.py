import gradio as gr
import os
import zipfile
import subprocess
import time
from google.colab import files
import signal

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
    """Startet den Roop-Prozess in Colab neu"""
    try:
        # Finde und beende alle Python-Prozesse 
        os.system("pkill -9 python")
        
        # Warte kurz
        time.sleep(2)
        
        # Starte Roop neu
        process = subprocess.Popen(["python", "run.py"], 
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)
        
        # Warte auf den Start und suche nach der URL
        for i in range(30):  # 30 Sekunden Timeout
            line = process.stdout.readline()
            if "gradio.live" in line:
                return f"Roop neu gestartet. Neue URL: {line.strip()}"
            time.sleep(1)
            
        return "Roop wurde neu gestartet. Bitte schaue in der Konsolenausgabe nach der neuen URL."
        
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
            gr.Markdown("""
            **Hinweis zum Neustart:**
            1. Nach dem Klick auf 'Restart Roop' wird die neue URL hier angezeigt
            2. Öffne die neue URL in einem neuen Tab
            """)
            
    # Event Handler
    download_btn.click(create_zip_from_output, outputs=status_download)
    restart_btn.click(restart_roop, outputs=status_output)

# Starte das Admin Interface
if __name__ == "__main__":
    # Starte zuerst Roop
    process = subprocess.Popen(["python", "run.py"])
    
    # Warte kurz damit Roop starten kann
    time.sleep(5)
    
    # Dann starte das Admin Interface
    admin_interface.launch(
        share=True,  # Erstellt einen öffentlichen Link
        server_port=7861,  # Anderer Port als Roop
        server_name="0.0.0.0"  # Erlaubt externe Verbindungen
    )