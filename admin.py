import gradio as gr
import os
import zipfile
import subprocess
import webbrowser
from pathlib import Path
import signal
import psutil

# Konfiguration
OUTPUT_PATH = "output"  # Der Pfad zum Output-Ordner aus dem Code
ROOP_PROCESS = None
CURRENT_PORT = 7860

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

def restart_roop():
    """Startet den Roop-Prozess neu"""
    global ROOP_PROCESS
    
    # Beende den existierenden Prozess
    if ROOP_PROCESS:
        parent = psutil.Process(ROOP_PROCESS.pid)
        for child in parent.children(recursive=True):
            child.terminate()
        parent.terminate()
    
    # Starte den Prozess neu
    ROOP_PROCESS = subprocess.Popen(['python', 'run.py'])
    
    return f"http://localhost:{CURRENT_PORT}"

def get_roop_interface():
    """Gibt die URL zum Roop Interface zurück"""
    return f"http://localhost:{CURRENT_PORT}"

# Erstelle das Gradio Interface
with gr.Blocks(title="Roop Admin Interface") as admin_interface:
    with gr.Row():
        gr.Markdown("# Roop Admin Interface")
    
    with gr.Row():
        download_btn = gr.Button("Download Output Files")
        output_file = gr.File(label="Downloaded Files")
    
    with gr.Row():
        restart_btn = gr.Button("Restart Roop")
        link_output = gr.Textbox(label="Roop Interface Link")
    
    # Event Handler
    download_btn.click(create_zip_from_output, outputs=output_file)
    restart_btn.click(restart_roop, outputs=link_output)

# Starte das Admin Interface
if __name__ == "__main__":
    admin_interface.launch(server_port=7861)  # Nutze einen anderen Port als Roop