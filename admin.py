import gradio as gr
import os
import zipfile
import subprocess
import webbrowser
from pathlib import Path
import signal
import psutil
import time
import requests

# Konfiguration
OUTPUT_PATH = "output"  # Der Pfad zum Output-Ordner
ROOP_PROCESS = None
ADMIN_PORT = 7861
ROOP_PORT = 7860
ROOP_PUBLIC_URL = None

def create_zip_from_output():
    """Erstellt ein Zip-Archiv aus dem Output-Ordner"""
    if not os.path.exists(OUTPUT_PATH):
        return "Output-Ordner existiert nicht!"
    
    zip_path = os.path.join(OUTPUT_PATH, "output_files.zip")
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(OUTPUT_PATH):
            for file in files:
                if file != "output_files.zip":  # Exclude the zip file itself
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, OUTPUT_PATH)
                    zipf.write(file_path, arcname)
    
    return zip_path

def kill_process_on_port(port):
    """Beendet den Prozess auf dem angegebenen Port"""
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conns in proc.connections(kind='inet'):
                if conns.laddr.port == port:
                    parent = psutil.Process(proc.pid)
                    for child in parent.children(recursive=True):
                        child.terminate()
                    parent.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def wait_for_gradio_link(timeout=60):
    """Wartet auf den öffentlichen Gradio Link"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Lese die letzten Zeilen der Konsolenausgabe
            process = subprocess.Popen(['tail', '-n', '20', 'roop_output.log'], stdout=subprocess.PIPE)
            output = process.stdout.read().decode()
            
            # Suche nach dem Public Link
            for line in output.split('\n'):
                if "gradio.live" in line:
                    return line.strip()
        except:
            pass
        time.sleep(1)
    return None

def restart_roop():
    """Startet den Roop-Prozess neu"""
    global ROOP_PROCESS, ROOP_PUBLIC_URL
    
    # Beende alle existierenden Prozesse auf den relevanten Ports
    kill_process_on_port(ROOP_PORT)
    
    # Warte kurz
    time.sleep(2)
    
    # Starte Roop neu mit Share Option
    ROOP_PROCESS = subprocess.Popen(
        ['python', 'run.py'],
        env={**os.environ, 'ROOP_SHARE': 'true'},  # Setze Umgebungsvariable
        stdout=open('roop_output.log', 'w'),
        stderr=subprocess.STDOUT
    )
    
    # Warte kurz damit Roop starten kann
    time.sleep(10)
    
    # Versuche den öffentlichen Link zu bekommen
    try:
        with open('roop_output.log', 'r') as f:
            for line in f:
                if "gradio.live" in line:
                    ROOP_PUBLIC_URL = line.strip()
                    return ROOP_PUBLIC_URL
    except:
        pass
    
    return "Roop wurde neu gestartet. Bitte warte einen Moment bis der öffentliche Link erscheint."

def get_roop_interface():
    """Gibt die URL zum Roop Interface zurück"""
    global ROOP_PUBLIC_URL
    return ROOP_PUBLIC_URL if ROOP_PUBLIC_URL else "Warte auf öffentlichen Link..."

# Erstelle das Gradio Interface
with gr.Blocks(title="Roop Admin Interface") as admin_interface:
    with gr.Row():
        gr.Markdown("# Roop Admin Interface")
    
    with gr.Row():
        with gr.Column():
            download_btn = gr.Button("Download Output Files", variant="primary")
            output_file = gr.File(label="Downloaded Files")
    
    with gr.Row():
        with gr.Column():
            restart_btn = gr.Button("Restart Roop", variant="primary")
            link_output = gr.Textbox(label="Roop Interface Link", interactive=False)
            open_interface_btn = gr.Button("Open Roop Interface")
    
    # Event Handler
    download_btn.click(create_zip_from_output, outputs=output_file)
    restart_btn.click(restart_roop, outputs=link_output)
    open_interface_btn.click(fn=lambda: webbrowser.open(ROOP_PUBLIC_URL if ROOP_PUBLIC_URL else ""))

# Starte das Admin Interface
if __name__ == "__main__":
    # Modifiziere die run.py um Share zu aktivieren
    with open('run.py', 'r') as f:
        content = f.read()
    
    if 'share=True' not in content:
        content = content.replace('server_share=False', 'server_share=True')
        with open('run.py', 'w') as f:
            f.write(content)
    
    # Starte zuerst Roop
    ROOP_PROCESS = subprocess.Popen(
        ['python', 'run.py'],
        stdout=open('roop_output.log', 'w'),
        stderr=subprocess.STDOUT
    )
    
    # Warte kurz damit Roop starten kann
    time.sleep(10)
    
    # Hole den öffentlichen Link
    try:
        with open('roop_output.log', 'r') as f:
            for line in f:
                if "gradio.live" in line:
                    ROOP_PUBLIC_URL = line.strip()
    except:
        pass
    
    # Dann starte das Admin Interface
    admin_interface.launch(server_port=ADMIN_PORT, share=True, show_error=True)