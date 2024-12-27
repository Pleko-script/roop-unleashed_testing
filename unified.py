#!/usr/bin/env python3
import os
import gc
import zipfile
import gradio as gr

# roop-Module
import roop.globals
import roop.metadata
import roop.utilities as util
import ui.globals as uii

# Settings + core (für pre_check etc.)
from settings import Settings
from roop.core import pre_check, decode_execution_providers, set_display_ui

# Deine Tabs
from ui.tabs.faceswap_tab import faceswap_tab
from ui.tabs.livecam_tab import livecam_tab
from ui.tabs.facemgr_tab import facemgr_tab
from ui.tabs.extras_tab import extras_tab
from ui.tabs.settings_tab import settings_tab

OUTPUT_PATH = "output"

def create_zip_for_download():
    """
    Erstellt ein ZIP 'output_files.zip' aus dem 'output'-Ordner
    und gibt den Dateipfad zurück. Gradio legt daraus einen Download-Link an.
    """
    if not os.path.exists(OUTPUT_PATH):
        return None  # oder raise Exception("Output existiert nicht.")

    zip_path = os.path.join(OUTPUT_PATH, "output_files.zip")
    try:
        # Alte ZIP ggf. löschen:
        if os.path.isfile(zip_path):
            os.remove(zip_path)

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files_ in os.walk(OUTPUT_PATH):
                for f in files_:
                    if f == "output_files.zip":
                        continue
                    file_path = os.path.join(root, f)
                    arcname = os.path.relpath(file_path, OUTPUT_PATH)
                    zipf.write(file_path, arcname)
        # Für Gradio: Return den Pfad. Dann erzeugt Gradio ein Download-Link in der UI.
        return zip_path
    except Exception as e:
        # Falls was schief geht, return None (kein Downloadlink)
        return None


def reset_roop():
    """
    Soft-Neustart: Leert globale Listen, GPU-Cache etc.
    """
    # Beispiel: Leere roop-spezifische Globals
    roop.globals.INPUT_FACESETS.clear()
    roop.globals.TARGET_FACES.clear()

    # GPU-Cache
    try:
        import torch
        torch.cuda.empty_cache()
    except:
        pass
    gc.collect()

    return "roop wurde neu initialisiert."


def prepare_environment():
    """
    Legt Output- und Temp-Verzeichnisse an, basierend auf roop.globals.CFG.
    """
    roop.globals.output_path = os.path.abspath(os.path.join(os.getcwd(), "output"))
    os.makedirs(roop.globals.output_path, exist_ok=True)

    if not roop.globals.CFG.use_os_temp_folder:
        os.environ["TEMP"] = os.environ["TMP"] = os.path.abspath(os.path.join(os.getcwd(), "temp"))
    os.makedirs(os.environ["TEMP"], exist_ok=True)

    os.environ["GRADIO_TEMP_DIR"] = os.environ["TEMP"]
    os.environ['GRADIO_ANALYTICS_ENABLED'] = '0'


def run_unified():
    """
    Gesamt-Funktion, die (1) CFG + Model-Downloads vorbereitet,
    (2) ein Gradio-Interface mit Admin-Tab + roop-Tabs startet,
    (3) nur 1x .launch(share=...) => 1x .gradio.live.
    """
    # Falls roop.globals.CFG noch None ist => initialisieren
    if roop.globals.CFG is None:
        roop.globals.CFG = Settings("config.yaml")  # oder config_colab.yaml

    # Download fehlender Models:
    if not pre_check():
        print("Fehler: pre_check() fehlgeschlagen.")
        return

    # Env anlegen
    prepare_environment()

    # roop-Ausgabe in Gradio-Info umleiten
    set_display_ui(lambda msg: gr.Info(msg))

    # GPU/CPU Check
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

    # Unser EINZIGES Gradio-Interface
    with gr.Blocks(
        title=f'{roop.metadata.name} {roop.metadata.version}',
        theme=roop.globals.CFG.selected_theme,
        css=mycss,
        delete_cache=(60, 86400)
    ) as unified_app:

        gr.Markdown(f"## {roop.metadata.name} {roop.metadata.version} - Unified Admin + roop")

        # ADMIN-TAB
        with gr.Tab("Admin"):
            gr.Markdown("### roop-Admin-Funktionen")

            # 1) Reset roop
            btn_reset = gr.Button("Neustart roop-Anwendung")
            txt_reset = gr.Textbox("", label="Reset Status", interactive=False)
            btn_reset.click(fn=reset_roop, outputs=txt_reset)

            # 2) Download ZIP
            btn_zip = gr.Button("Download ZIP von 'output'")
            # => Wir geben an Gradio ein "File"-Objekt zurück => Download-Link
            file_zip = gr.File(label="ZIP zum Herunterladen", interactive=False)

            # Klick => create_zip_for_download => Pfad => Gradio macht Download-Link
            btn_zip.click(fn=create_zip_for_download, outputs=file_zip)

        # roop-Tabs
        faceswap_tab()
        livecam_tab()
        facemgr_tab()
        extras_tab()
        settings_tab()

    # Start => .gradio.live
    unified_app.queue().launch(
        share=roop.globals.CFG.server_share,  # True/False -> config.yaml
        server_name=roop.globals.CFG.server_name if roop.globals.CFG.server_name else None,
        server_port=roop.globals.CFG.server_port if roop.globals.CFG.server_port > 0 else None,
        ssl_verify=False,
        show_error=True
    )


if __name__ == "__main__":
    run_unified()
