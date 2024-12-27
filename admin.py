import gradio as gr
import subprocess
import threading
import queue
import os
import zipfile
import time
import re
from google.colab import files

ROOP_PROCESS = None
LOG_QUEUE = queue.Queue()
STOP_THREAD = False
OUTPUT_PATH = "output"

# Globale Variable für roop-unleashed-Link
ROOP_URL = None

def create_zip_from_output():
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
        return f"Fehler beim Erstellen des ZIP: {str(e)}"


def find_gradio_url(line):
    """Sucht in einer Zeile nach einer https://...gradio.live URL."""
    pattern = r'https://[a-zA-Z0-9_-]+\.gradio\.live'
    match = re.search(pattern, line)
    if match:
        return match.group(0)
    return None

def roop_logger(proc):
    """
    Läuft in einem Thread, liest stdout des Subprozesses (run.py)
    und legt Zeilen in LOG_QUEUE ab, bis der Prozess oder STOP_THREAD endet.
    Findet er eine Gradio-URL, speichern wir sie in ROOP_URL.
    """
    global STOP_THREAD, ROOP_URL

    while True:
        if proc.poll() is not None:
            break
        line = proc.stdout.readline()
        if line:
            # Falls wir eine Gradio-URL in dieser Zeile finden, merken wir sie uns
            url = find_gradio_url(line)
            if url:
                ROOP_URL = url  # Speichere Link in globaler Variable

            LOG_QUEUE.put(line)
        if STOP_THREAD:
            break
    print("Logger-Thread beendet.")


def start_stop_roop(console_str):
    """
    Startet oder stoppt den 'roop-unleashed'-Prozess (run.py).
    console_str ist der Inhalt der 'Konsole'-Textbox (string).
    """
    global ROOP_PROCESS, STOP_THREAD, ROOP_URL

    if ROOP_PROCESS is None:
        # Start
        console_str = "Starte roop-unleashed...\n"
        ROOP_URL = None  # Zurücksetzen, falls alt
        ROOP_PROCESS = subprocess.Popen(
            ["python", "run.py"],  # run.py sollte share=True aufrufen
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        STOP_THREAD = False
        threading.Thread(target=roop_logger, args=(ROOP_PROCESS,), daemon=True).start()
        return "Stop Roop", "roop-unleashed gestartet", console_str
    else:
        # Stop
        console_str += "\nStoppe roop-unleashed...\n"
        STOP_THREAD = True
        ROOP_PROCESS.terminate()
        time.sleep(1)
        if ROOP_PROCESS.poll() is None:
            ROOP_PROCESS.kill()
        ROOP_PROCESS = None
        return "Start Roop", "roop-unleashed gestoppt", console_str


def poll_logs(console_str, roop_url_str):
    """
    Alle 2s aufgerufen. Liest neue Logs aus LOG_QUEUE
    und hängt sie an 'console_str'. roop_url_str aktualisieren wir
    aus der globalen ROOP_URL-Variable (falls dort was erkannt wurde).
    """
    global ROOP_URL
    # Logs abholen
    logs = []
    while not LOG_QUEUE.empty():
        logs.append(LOG_QUEUE.get_nowait())
    if logs:
        console_str += "".join(logs)

    # Falls wir eine roop-Unleashed-URL gefunden haben:
    if ROOP_URL:
        roop_url_str = ROOP_URL

    return console_str, roop_url_str


with gr.Blocks(title="Roop Admin Interface für Colab") as admin_interface:
    gr.Markdown("# Admin Interface für roop-unleashed")

    with gr.Row():
        download_btn = gr.Button("Download als ZIP")
        download_info = gr.Textbox(label="Download-Status", interactive=False)

    with gr.Row():
        start_btn = gr.Button("Start Roop", variant="primary")
        status_box = gr.Textbox(label="Status", value="Roop ist gestoppt", interactive=False, lines=1)
        console = gr.Textbox(label="Konsole", value="", interactive=False, lines=10)

    # Eine extra Textbox, um den roop-Interface-Link anzuzeigen
    roop_link_box = gr.Textbox(
        label="roop-Unleashed Link",
        value="(Noch nicht bekannt)",
        interactive=False,
        lines=1
    )

    # Download-Button
    download_btn.click(
        fn=create_zip_from_output,
        outputs=download_info
    )

    # Start-/Stop-Button
    start_btn.click(
        fn=start_stop_roop,
        inputs=[console],
        outputs=[start_btn, status_box, console]
    )

    # Timer-Funktion: poll_logs
    # Wir geben 2 Outputs zurück: console (string) und roop_link_box (string)
    admin_interface.load(
        fn=poll_logs,
        inputs=[console, roop_link_box],
        outputs=[console, roop_link_box],
        every=2
    )


if __name__ == "__main__":
    # Starte das Admin-Interface
    admin_interface.launch(share=True)
