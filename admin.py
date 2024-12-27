import gradio as gr
import subprocess
import threading
import queue
import os
import zipfile
import time
from google.colab import files

# Globale Variablen
ROOP_PROCESS = None
LOG_QUEUE = queue.Queue()
STOP_THREAD = False
OUTPUT_PATH = "output"

# Hier speichern wir den roop-Link, sobald wir ihn sehen
ROOPURL_FOUND = None


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
        return f"Fehler beim Erstellen des ZIP: {str(e)}"


def roop_logger(proc):
    """
    Läuft in einem Thread, liest stdout des Subprozesses (run.py)
    und legt Zeilen in LOG_QUEUE ab, bis der Prozess oder STOP_THREAD endet.
    Findet er eine Zeile "ROOPURL::<link>", speichert er diese in ROOPURL_FOUND.
    """
    global STOP_THREAD, ROOPURL_FOUND

    while True:
        if proc.poll() is not None:
            break
        line = proc.stdout.readline()
        if line:
            # Falls wir die markierte Zeile finden:
            if line.startswith("ROOPURL::"):
                link = line.strip().split("ROOPURL::", 1)[-1]
                ROOPURL_FOUND = link

            LOG_QUEUE.put(line)
        if STOP_THREAD:
            break
    print("Logger-Thread beendet.")


def start_stop_roop(console_str, roop_url_str):
    """
    Startet oder stoppt den 'roop-unleashed'-Prozess (run.py).
    - console_str: aktueller Inhalt der Konsolen-Textbox
    - roop_url_str: aktueller Inhalt der roopURL-Textbox
    """
    global ROOP_PROCESS, STOP_THREAD, ROOPURL_FOUND

    if ROOP_PROCESS is None:
        # Start
        console_str = "Starte roop-unleashed...\n"
        ROOPURL_FOUND = None  # alten Link löschen

        ROOP_PROCESS = subprocess.Popen(
            ["python", "run.py"],  # ruft euer run.py auf
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        STOP_THREAD = False
        threading.Thread(target=roop_logger, args=(ROOP_PROCESS,), daemon=True).start()
        return "Stop Roop", "roop-unleashed gestartet", console_str, roop_url_str
    else:
        # Stop
        console_str += "\nStoppe roop-unleashed...\n"
        STOP_THREAD = True
        ROOP_PROCESS.terminate()
        time.sleep(1)
        if ROOP_PROCESS.poll() is None:
            ROOP_PROCESS.kill()
        ROOP_PROCESS = None
        return "Start Roop", "roop-unleashed gestoppt", console_str, "(noch keiner)"


def poll_logs(console_str, roop_url_str):
    """
    Alle 2s aufgerufen. Liest neue Log-Zeilen aus LOG_QUEUE
    und hängt sie an 'console_str'. roop_url_str wird aktualisiert,
    falls in roop_logger(...) 'ROOPURL_FOUND' belegt wurde.
    """
    global ROOPURL_FOUND

    # 1) Logs abholen
    lines = []
    while not LOG_QUEUE.empty():
        lines.append(LOG_QUEUE.get_nowait())
    if lines:
        console_str += "".join(lines)

    # 2) Falls wir in roop_logger(...) "ROOPURL_FOUND" gefunden haben
    if ROOPURL_FOUND:
        roop_url_str = ROOPURL_FOUND

    return console_str, roop_url_str


# Haupt-Gradio-Interface fürs Admin-Panel
with gr.Blocks(title="Admin Interface für roop-unleashed") as admin_interface:
    gr.Markdown("# Admin Interface für roop-unleashed")

    with gr.Row():
        download_btn = gr.Button("Download als ZIP")
        download_info = gr.Textbox(label="Download-Status", interactive=False)

    with gr.Row():
        start_btn = gr.Button("Start Roop", variant="primary")
        status_box = gr.Textbox(label="Status", value="Roop ist gestoppt", interactive=False, lines=1)
        console = gr.Textbox(label="Konsole", value="", interactive=False, lines=10)

    # Textbox, in der wir den roopURL-Link anzeigen
    roop_url_box = gr.Textbox(
        label="roop-Unleashed Link",
        value="(noch keiner)",
        interactive=False,
        lines=1
    )

    # Download-Button => ZIP erstellen
    download_btn.click(
        fn=create_zip_from_output,
        outputs=download_info
    )

    # Start-/Stop-Button => Subprozess starten/stoppen
    # Achtung: wir erweitern 'inputs' und 'outputs', damit roop_url_box in/out übergeben wird
    start_btn.click(
        fn=start_stop_roop,
        inputs=[console, roop_url_box],
        outputs=[start_btn, status_box, console, roop_url_box]
    )

    # Poll-Funktion, um Logs + roopURL zu aktualisieren
    admin_interface.load(
        fn=poll_logs,
        inputs=[console, roop_url_box],
        outputs=[console, roop_url_box],
        every=2
    )


if __name__ == "__main__":
    # Im Colab: share=True
    admin_interface.launch(share=True)
