# unified.py
import os
import time
import gradio as gr
import roop.globals
import roop.metadata
import roop.utilities as util
import ui.globals as uii

from settings import Settings
from roop.core import pre_check, decode_execution_providers, set_display_ui

# roop-Tabs:
from ui.tabs.faceswap_tab import faceswap_tab
from ui.tabs.livecam_tab import livecam_tab
from ui.tabs.facemgr_tab import facemgr_tab
from ui.tabs.extras_tab import extras_tab
from ui.tabs.settings_tab import settings_tab

import zipfile
from google.colab import files  # Nur in Colab nötig

# Standard-Flags
roop.globals.keep_fps = None
roop.globals.keep_frames = None
roop.globals.skip_audio = None
roop.globals.use_batch = None

OUTPUT_PATH = "output"


def prepare_environment():
    """
    Output-, temp-Verzeichnisse anlegen usw.
    Erfordert roop.globals.CFG (damit use_os_temp_folder nicht None ist).
    """
    roop.globals.output_path = os.path.abspath(os.path.join(os.getcwd(), "output"))
    os.makedirs(roop.globals.output_path, exist_ok=True)

    if not roop.globals.CFG.use_os_temp_folder:
        os.environ["TEMP"] = os.environ["TMP"] = os.path.abspath(os.path.join(os.getcwd(), "temp"))
    os.makedirs(os.environ["TEMP"], exist_ok=True)

    os.environ["GRADIO_TEMP_DIR"] = os.environ["TEMP"]
    os.environ['GRADIO_ANALYTICS_ENABLED'] = '0'


def reset_roop():
    """
    'Neustart' – roop-Variablen leeren, GPU-Cache usw.
    """
    import gc
    roop.globals.INPUT_FACESETS.clear()
    roop.globals.TARGET_FACES.clear()

    try:
        import torch
        torch.cuda.empty_cache()
    except:
        pass

    gc.collect()
    return "roop wurde neu initialisiert."


def create_zip_from_output():
    """
    Zipt den 'output/' Ordner (ohne vorhandenes 'output_files.zip') und
    triggert den Download in Google Colab.
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


def clear_output_folder():
    """
    Löscht alle Dateien/Unterordner im 'output/' Ordner,
    damit man ein neues Set starten kann.
    """
    if not os.path.exists(OUTPUT_PATH):
        return "Output-Ordner existiert nicht!"

    # wir löschen alles in OUTPUT_PATH
    for root, dirs, files_ in os.walk(OUTPUT_PATH):
        for f in files_:
            os.remove(os.path.join(root, f))
        for d in dirs:
            subdir = os.path.join(root, d)
            try:
                import shutil
                shutil.rmtree(subdir)
            except:
                pass

    return "Output-Ordner geleert!"


def run_unified():
    """
    EINE Gradio-App mit roop-Funktionalität + Admin-Funktionen (Reset roop,
    Download als Zip, Clear Output)
    """

    # 1) roop.globals.CFG laden, falls None
    if roop.globals.CFG is None:
        roop.globals.CFG = Settings("config.yaml")  # oder config_colab.yaml

    # 2) pre_check() => lädt fehlende onnx-Modelle herunter
    if not pre_check():
        print("Fehler: pre_check() fehlgeschlagen oder abgebrochen.")
        return

    # 3) Env
    prepare_environment()

    # 4) UI-Anzeige-Funktion
    set_display_ui(lambda msg: gr.Info(msg))

    # 5) ggf. GPU -> CPU
    if roop.globals.CFG.provider == "cuda" and not util.has_cuda_device():
        roop.globals.CFG.provider = "cpu"

    roop.globals.execution_providers = decode_execution_providers([roop.globals.CFG.provider])
    gputype = util.get_device()
    if gputype == 'cuda':
        util.print_cuda_info()

    print(f'Using provider {roop.globals.execution_providers} - Device:{gputype}')

    mycss = """
    span {color: var(--block-info-text-color)}
    #fixedheight {
        max-height: 238.4px;
        overflow-y: auto !important;
    }
    .image-container.svelte-1l6wqyv {height: 100%}
    """

    with gr.Blocks(
        title=f'{roop.metadata.name} {roop.metadata.version}',
        theme=roop.globals.CFG.selected_theme,
        css=mycss,
        delete_cache=(60, 86400)
    ) as unified_app:

        gr.Markdown(f"## {roop.metadata.name} {roop.metadata.version} - Unified Admin + roop")

        with gr.Tab("Admin"):
            gr.Markdown("### roop-Admin-Funktionen")
            with gr.Row():
                reset_btn = gr.Button("Neustart roop-Anwendung")
                reset_status = gr.Textbox("", label="Reset-Status", interactive=False, lines=1)
                reset_btn.click(fn=reset_roop, outputs=reset_status)

            with gr.Row():
                dl_btn = gr.Button("Download als ZIP")
                dl_status = gr.Textbox("", label="Download-Status", interactive=False, lines=1)
                dl_btn.click(fn=create_zip_from_output, outputs=dl_status)

            with gr.Row():
                clear_btn = gr.Button("Clear Output Folder")
                clear_status = gr.Textbox("", label="Clear-Status", interactive=False, lines=1)
                clear_btn.click(fn=clear_output_folder, outputs=clear_status)

        # roop-Tabs
        faceswap_tab()
        livecam_tab()
        facemgr_tab()
        extras_tab()
        settings_tab()

    # Ein Launch => .gradio.live
    unified_app.queue().launch(
        share=roop.globals.CFG.server_share,  # True/False laut config
        server_name=roop.globals.CFG.server_name if roop.globals.CFG.server_name else None,
        server_port=roop.globals.CFG.server_port if roop.globals.CFG.server_port > 0 else None,
        ssl_verify=False,
        show_error=True
    )


if __name__ == "__main__":
    run_unified()
