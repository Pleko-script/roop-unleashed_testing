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
    if not os.path.exists(OUTPUT_PATH):
        return "Output-Ordner existiert nicht!"
    zip_path = os.path.join(OUTPUT_PATH, "output_files.zip")
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files_ in os.walk(OUTPUT_PATH):
                for file_ in files_:
                    if file_ == "output_files.zip":
                        continue
                    file_path = os.path.join(root, file_)
                    arcname = os.path.relpath(file_path, OUTPUT_PATH)
                    zipf.write(file_path, arcname)
        files.download(zip_path)
        return "ZIP wird heruntergeladen ..."
    except Exception as e:
        return f"Fehler beim Erstellen des ZIP: {str(e)}"


def roop_logger(proc):
    global stop_thread
    while True:
        if proc.poll() is not None:
            break
        line = proc.stdout.readline()
        if line:
            log_queue.put(line)
        if stop_thread:
            break
    print("Logger-Thread beendet.")


def start_stop_roop(console_str):
    """
    - console_str = aktueller Text aus der Console-Textbox (string)
    - Rückgabe: (button_label, status_text, neuer_console_text)
    """
    global ROOP_PROCESS, stop_thread

    if ROOP_PROCESS is None:
        # Start
        console_str = "Starte roop-unleashed...\n"
        cmd = ["python", "run.py"]
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
        return "Stop Roop", "roop-unleashed gestartet", console_str
    else:
        # Stop
        console_str += "\nStoppe roop-unleashed...\n"
        stop_thread = True
        ROOP_PROCESS.terminate()
        time.sleep(1)
        if ROOP_PROCESS.poll() is None:
            ROOP_PROCESS.kill()
        ROOP_PROCESS = None
        return "Start Roop", "roop-unleashed gestoppt", console_str


def poll_logs(console_str):
    """Alle 2s aufgerufen, um neue Logs ins console_str anzuhängen"""
    lines = []
    while not log_queue.empty():
        line = log_queue.get_nowait()
        lines.append(line)
    if lines:
        console_str += "".join(lines)
    return console_str


with gr.Blocks(title="Roop Admin Interface für Colab") as admin_interface:
    gr.Markdown("# Admin Interface für roop-unleashed")

    with gr.Row():
        download_btn = gr.Button("Download als ZIP")
        download_info = gr.Textbox(label="Download-Status", interactive=False)

    with gr.Row():
        start_btn = gr.Button("Start Roop", variant="primary")
        status_box = gr.Textbox(label="Status", value="Roop ist gestoppt", interactive=False, lines=1)
        console = gr.Textbox(label="Konsole", value="", interactive=False, lines=10)

    # Aktionen
    download_btn.click(fn=create_zip_from_output, outputs=download_info)

    # WICHTIG: console als Input-> string
    start_btn.click(
        fn=start_stop_roop,
        inputs=[console],
        outputs=[start_btn, status_box, console]
    )

    # Alle 2 Sekunden poll_logs -> console
    admin_interface.load(fn=poll_logs, inputs=[console], outputs=[console], every=2)

if __name__ == "__main__":
    admin_interface.launch(share=True)
