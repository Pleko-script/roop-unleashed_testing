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
                    if file != "output_files.zip":
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, OUTPUT_PATH)
                        zipf.write(file_path, arcname)
        
        files.download(zip_path)
        return "Download gestartet"
    except Exception as e:
        return f"Fehler beim Erstellen des ZIP-Archivs: {str(e)}"

def start_stop_roop():
    """Startet oder stoppt den Roop-Prozess"""
    global ROOP_PROCESS
    
    try:
        if ROOP_PROCESS is None:
            # Starte Roop
            env = os.environ.copy()
            env['ROOP_SERVER_SHARE'] = 'true'
            
            ROOP_PROCESS = subprocess.Popen(
                ['python', 'run.py'],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            # Warte und suche nach der URL
            for i in range(30):
                line = ROOP_PROCESS.stdout.readline()
                if "gradio.live" in line:
                    return ("Stop Roop", f"Roop läuft. URL: {line.strip()}")
                if i == 29:
                    return ("Stop Roop", "Roop läuft, konnte aber keine URL finden")
        else:
            # Stoppe Roop
            ROOP_PROCESS.terminate()
            time.sleep(1)
            if ROOP_PROCESS.poll() is None:
                ROOP_PROCESS.kill()
            ROOP_PROCESS = None
            return ("Start Roop", "Roop wurde gestoppt")
            
    except Exception as e:
        ROOP_PROCESS = None
        return ("Start Roop", f"Fehler: {str(e)}")

# Erstelle das Gradio Interface
with gr.Blocks(title="Roop Admin Interface für Colab") as admin_interface:
    with gr.Row():
        gr.Markdown("# Roop Admin Interface")
    
    with gr.Row():
        with gr.Column(scale=1):
            download_btn = gr.Button("Download als ZIP", variant="primary")
            status_download = gr.Textbox(label="Download Status", interactive=False)
    
    with gr.Row():
        with gr.Column(scale=1):
            start_btn = gr.Button("Start Roop", variant="primary")
            status_output = gr.Textbox(label="Status", interactive=False, value="Roop ist gestoppt")
            gr.Markdown("""
            **Bedienung:**
            1. Klicke 'Start Roop' um Roop zu starten
            2. Der gradio.live Link erscheint im Status-Feld
            3. Zum Neustarten erst auf 'Stop Roop' und dann wieder auf 'Start Roop' klicken
            """)
            
    # Event Handler
    download_btn.click(create_zip_from_output, outputs=status_download)
    start_btn.click(start_stop_roop, outputs=[start_btn, status_output])

# Starte das Admin Interface
if __name__ == "__main__":
    admin_interface.launch(
        share=True,
        server_port=7861,
        server_name="0.0.0.0"
    )