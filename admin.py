import gradio as gr
import subprocess
import threading
import queue
import os
import zipfile
import time
from google.colab import files

ROOP_PROCESS = None
LOG_QUEUE = queue.Queue()
STOP_THREAD = False
OUTPUT_PATH = "output"


def create_zip_from_output():
    """
    Packt den 'output'-Ordner (ohne bereits erstelltes ZIP) in ein ZIP-Archiv
    und startet den Download in Google Colab.
    """
    if not os.path.exists(OUTPUT_PATH):
        return "Output-Ordner existiert nicht!"

    zip_path = os.path.join(OUTPUT_PATH, "output_files.zip")
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files_ in os.walk(OUTPUT_PATH):
                for f in files_:
                    if f == "output_files.zip":
                        continue
                    file_path = os.path.join(root, f)
                    arcname = os.path.relpath(file_path, OUTPUT_PATH)
                    zipf.write(file_path, arcname)

        files.download(zip_path)
        return "ZIP wird heruntergeladen..."
    except Exception as e:
        return f"Fehler beim Erstellen des ZIP: {e}"


def roop_logger(proc):
    """
    Läuft in einem Thread, liest stdout des Subprozesses
    und legt Zeilen in LOG_QUEUE ab, bis der Prozess oder STOP_THREAD endet.
    """
    global STOP_THREAD
    while True:
        if proc.poll() is not None:
            break
        line = proc.stdout.readline()
        if line:
            LOG_QUEUE.put(line)
        if STOP_THREAD:
            break
    print("Logger-Thread beendet.")


def start_stop_roop(console):
    """
    Startet oder stoppt den 'roop-unleashed'-Prozess (run.py).
    Nutzt console (Textbox-Inhalt) als Ein-/Ausgabe-String.
    """
    global ROOP_PROCESS, STOP_THREAD

    if ROOP_PROCESS is None:
        console.value = "Starte roop-unleashed...\n"
        ROOP_PROCESS = subprocess.Popen(
            ["python", "run.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        STOP_THREAD = False
        threading.Thread(target=roop_logger, args=(ROOP_PROCESS,), daemon=True).start()
        return "Stop Roop", "roop-unleashed gestartet", console.value
    else:
        console.value += "\nStoppe roop-unleashed...\n"
        STOP_THREAD = True
        ROOP_PROCESS.terminate()
        time.sleep(1)
        if ROOP_PROCESS.poll() is None:
            ROOP_PROCESS.kill()
        ROOP_PROCESS = None
        return "Start Roop", "roop-unleashed gestoppt", console.value


def poll_logs(console):
    """
    Alle x Sekunden aufgerufen, um neue Log-Zeilen aus LOG_QUEUE
    an das Konsolen-Textbox anzuhängen.
    """
    logs = []
    while not LOG_QUEUE.empty():
        logs.append(LOG_QUEUE.get_nowait())
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

    download_btn.click(fn=create_zip_from_output, outputs=download_info)
    start_btn.click(fn=start_stop_roop, inputs=[console], outputs=[start_btn, status_box, console])

    # Poll-Funktion alle 2s, um Logs ins Konsole-Textbox zu übertragen
    admin_interface.load(fn=poll_logs, inputs=[console], outputs=[console], every=2)


if __name__ == "__main__":
    admin_interface.launch(share=True)
