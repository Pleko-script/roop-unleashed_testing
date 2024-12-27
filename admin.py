# admin.py
import gradio as gr
import subprocess
import threading
import queue
import os
import zipfile
import time
from google.colab import files

ROOP_PROCESS = None
log_queue = queue.Queue()
stop_thread = False
OUTPUT_PATH = "output"

def create_zip_from_output():
    """Erstellt ein Zip-Archiv aus dem Output-Ordner und lädt es herunter."""
    if not os.path.exists(OUTPUT_PATH):
        return "Output-Ordner existiert nicht!"
    zip_path = os.path.join(OUTPUT_PATH, "output_files.zip")
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files_ in os.walk(OUTPUT_PATH):
                for file_ in files_:
                    # Ignoriere die bereits erstellte ZIP-Datei
                    if file_ == "output_files.zip":
                        continue
                    file_path = os.path.join(root, file_)
                    arcname = os.path.relpath(file_path, OUTPUT_PATH)
                    zipf.write(file_path, arcname)
        # Initiieren des Downloads in Colab
        files.download(zip_path)
        return "ZIP wird heruntergeladen ..."
    except Exception as e:
        return f"Fehler beim Erstellen des ZIP: {str(e)}"


def roop_logger(proc):
    """
    Läuft in einem separaten Thread, liest stdout vom Subprozess
    und schreibt Zeilen in die log_queue, damit wir sie später abholen.
    """
    global stop_thread
    while True:
        if proc.poll() is not None:
            # Subprozess ist beendet
            break
        line = proc.stdout.readline()
        if line:
            log_queue.put(line)
        if stop_thread:
            break
    print("Logger-Thread beendet.")


def start_stop_roop(console):
    """
    Gradio-Callback: Startet oder stoppt den roop-Prozess (run.py).
    """
    global ROOP_PROCESS, stop_thread

    if ROOP_PROCESS is None:
        # Start
        console.value = "Starte roop-unleashed...\n"
        cmd = ["python", "run.py"]   # oder euer Skript: ["python", "run.py", "--server_share", ...]
        ROOP_PROCESS = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        stop_thread = False
        t = threading.Thread(target=roop_logger, args=(ROOP_PROCESS,), daemon=True)
        t.start()
        return "Stop Roop", "roop-unleashed gestartet", console.value
    else:
        # Stop
        console.value += "\nStoppe roop-unleashed...\n"
        stop_thread = True
        ROOP_PROCESS.terminate()
        time.sleep(1)
        if ROOP_PROCESS.poll() is None:
            ROOP_PROCESS.kill()
        ROOP_PROCESS = None
        return "Start Roop", "roop-unleashed gestoppt", console.value


def poll_logs(console):
    """
    Poll-Funktion, die regelmäßig aufgerufen wird,
    um neue Logs aus log_queue ins Textfeld zu hängen.
    """
    logs = []
    while not log_queue.empty():
        line = log_queue.get_nowait()
        logs.append(line)
    if logs:
        console.value += "".join(logs)
    return console.value


with gr.Blocks(title="Roop Admin Interface für Colab") as admin_interface:
    gr.Markdown("# Admin Interface für roop-unleashed")
    with gr.Row():
        download_btn = gr.Button("Download als ZIP")
        download_info = gr.Textbox(label="Download-Status", interactive=False)

    with gr.Row():
        start_btn = gr.Button("Start Roop", variant="primary")
        status_box = gr.Textbox(label="Status", value="Roop ist gestoppt", interactive=False, lines=1)
        console = gr.Textbox(label="Konsole", value="", interactive=False, lines=10)

    # Events
    download_btn.click(fn=create_zip_from_output, outputs=download_info)
    start_btn.click(fn=start_stop_roop, inputs=[console], outputs=[start_btn, status_box, console])

    # Timer: Alle 2 Sekunden poll_logs -> console
    admin_interface.load(fn=poll_logs, inputs=[console], outputs=[console], every=2)

# Gradio starten (im Colab: share=True, Port etc. optional)
if __name__ == "__main__":
    admin_interface.launch(share=True)
