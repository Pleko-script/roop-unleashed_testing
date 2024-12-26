import gradio as gr
import os
import zipfile
import subprocess
import webbrowser
from pathlib import Path
import signal
import psutil
import time
import shutil
import sys

# Konfiguration
OUTPUT_PATH = "output"  # Der Pfad zum Output-Ordner
ROOP_PROCESS = None
ADMIN_PORT = 7861
ROOP_PORT = 7860

def create_zip_from_output():
    """Erstellt ein Zip-Archiv aus dem Output-Ordner"""
    if not os.path.exists(OUTPUT_PATH):
        return "Output-Ordner existiert nicht!"
    
    # Erstelle einen temporären Ordner für die ZIP-Datei
    temp_dir = os.path.join(OUTPUT_PATH, "temp_zip")
    os.makedirs(temp_dir, exist_ok=True)
    
    zip_path = os.path.join(temp_dir, "output_files.zip")
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(OUTPUT_PATH):
                if root == temp_dir:  # Überspringe den temp_zip Ordner
                    continue
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, OUTPUT_PATH)
                    try:
                        zipf.write(file_path, arcname)
                    except Exception as e:
                        print(f"Fehler beim Hinzufügen von {file_path}: {str(e)}")
                        continue
    except Exception as e:
        print(f"Fehler beim Erstellen des ZIP-Archivs: {str(e)}")
        return None
    
    return zip_path

def kill_process_on_port(port):
    """Beendet den Prozess auf dem angegebenen Port"""
    try:
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            try:
                for conns in proc.connections(kind='inet'):
                    if conns.laddr.port == port:
                        parent = psutil.Process(proc.pid)
                        children = parent.children(recursive=True)
                        for child in children:
                            try:
                                child.terminate()
                            except:
                                pass
                        parent.terminate()
                        time.sleep(1)
                        if parent.is_running():
                            parent.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception as e:
        print(f"Fehler beim Beenden der Prozesse: {str(e)}")

def restart_roop():
    """Startet den Roop-Prozess neu"""
    global ROOP_PROCESS
    
    try:
        # Beende alle existierenden Prozesse
        kill_process_on_port(ROOP_PORT)
        if ROOP_PROCESS:
            try:
                ROOP_PROCESS.terminate()
                time.sleep(1)
                if ROOP_PROCESS.poll() is None:
                    ROOP_PROCESS.kill()
            except:
                pass
        
        # Warte kurz
        time.sleep(2)
        
        # Setze die Umgebungsvariable für Server Share
        env = os.environ.copy()
        env['ROOP_SERVER_SHARE'] = 'true'
        
        # Starte Roop neu
        if os.name == 'nt':  # Windows
            ROOP_PROCESS = subprocess.Popen(['python', 'run.py'], 
                                          creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                                          env=env)
        else:  # Linux/Mac
            ROOP_PROCESS = subprocess.Popen(['python', 'run.py'],
                                          preexec_fn=os.setsid,
                                          env=env)
        
        time.sleep(5)  # Warte bis Roop gestartet ist
        
        return "Roop wurde neu gestartet. Das Interface ist unter http://localhost:7860 verfügbar."
    except Exception as e:
        return f"Fehler beim Neustarten von Roop: {str(e)}"

# Erstelle das Gradio Interface
with gr.Blocks(title="Roop Admin Interface") as admin_interface:
    with gr.Row():
        gr.Markdown("# Roop Admin Interface")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("""
            ## Download
            Lade alle verarbeiteten Dateien als ZIP herunter
            """)
            download_btn = gr.Button("Download Output Files", variant="primary")
            output_file = gr.File(label="Downloaded Files", type="filepath")  # Korrigierter type-Parameter
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("""
            ## Roop Verwaltung
            Verwalte den Roop-Prozess und öffne das Interface
            """)
            restart_btn = gr.Button("Restart Roop", variant="primary")
            status_output = gr.Textbox(label="Status", interactive=False)
            gr.Markdown("Das Roop Interface ist verfügbar unter:")
            gr.Markdown("http://localhost:7860")
    
    # Event Handler
    download_btn.click(create_zip_from_output, outputs=output_file)
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
        server_name="0.0.0.0",  # Erlaube externe Verbindungen
        server_port=ADMIN_PORT,
        share=True,  # Versuche einen öffentlichen Link zu erstellen
        show_error=True
    )