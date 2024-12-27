#!/usr/bin/env python3
import os
import gc
import shutil
import zipfile
import gradio as gr

# roop-Module
import roop.globals
import roop.metadata
import roop.utilities as util
import ui.globals as uii

from settings import Settings
from roop.core import pre_check, decode_execution_providers, set_display_ui

# Deine Tabs:
from ui.tabs.faceswap_tab import faceswap_tab
from ui.tabs.livecam_tab import livecam_tab
from ui.tabs.facemgr_tab import facemgr_tab
from ui.tabs.extras_tab import extras_tab
from ui.tabs.settings_tab import settings_tab

OUTPUT_PATH = "output"

##############################################################################
# 1) Einfaches Logging-System:
#    - Wir sammeln Logs in LISTE, fügen per logger(msg) neue Zeilen hinzu.
#    - "poll_logs(console_value)" hängt neue Zeilen an.
##############################################################################
LOG_BUFFER = []

def logger(msg: str):
    """
    Statt print(...) => logger(...). 
    So sammeln wir Meldungen an einer Stelle, 
    die wir im Admin-Tab pollend darstellen.
    """
    LOG_BUFFER.append(msg + "\n")

def poll_logs(console_str):
    """
    Alle 2s gerufen: Nimmt alles aus LOG_BUFFER, 
    hängt es ans Ende des console_str (Textbox-Wert),
    und gibt console_str zurück.
    """
    if LOG_BUFFER:
        # logs zusammensetzen
        newlogs = "".join(LOG_BUFFER)
        console_str += newlogs
        LOG_BUFFER.clear()
    return console_str

##############################################################################
# 2) Admin-Funktionen
##############################################################################

def create_zip_for_download():
    """
    Erstellt 'output_files.zip' im OUTPUT_PATH
    und gibt den Pfad an Gradio zurück => Download-Link.
    """
    if not os.path.exists(OUTPUT_PATH):
        logger("create_zip_for_download: Kein output-Ordner!")
        return None

    zip_path = os.path.join(OUTPUT_PATH, "output_files.zip")
    try:
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
        logger(f"ZIP erstellt: {zip_path}")
        return zip_path
    except Exception as e:
        logger(f"ZIP-Fehler: {str(e)}")
        return None

def reset_roop():
    """
    Soft-Neustart: 
    - Leere roop-Globale, 
    - GPU-Cache, 
    - etc.
    """
    roop.globals.INPUT_FACESETS.clear()
    roop.globals.TARGET_FACES.clear()

    try:
        import torch
        torch.cuda.empty_cache()
    except:
        pass
    gc.collect()

    logger("roop: Soft-Reset durchgeführt.")
    return "roop wurde neu initialisiert."

def clear_output_folder():
    """
    Löscht den gesamten 'output'-Ordner und legt ihn neu an.
    """
    try:
        if os.path.isdir(OUTPUT_PATH):
            shutil.rmtree(OUTPUT_PATH)
        os.makedirs(OUTPUT_PATH, exist_ok=True)
        logger(f"Output-Folder '{OUTPUT_PATH}' wurde geleert.")
        return "Output-Folder wurde geleert."
    except Exception as e:
        logger(f"Fehler beim Clearen: {str(e)}")
        return f"Fehler beim Clearen: {str(e)}"

##############################################################################
# 3) Vorbereitungen (ENV)
##############################################################################

def prepare_environment():
    roop.globals.output_path = os.path.abspath(os.path.join(os.getcwd(), OUTPUT_PATH))
    os.makedirs(roop.globals.output_path, exist_ok=True)

    if not roop.globals.CFG.use_os_temp_folder:
        os.environ["TEMP"] = os.environ["TMP"] = os.path.abspath(os.path.join(os.getcwd(), "temp"))
    os.makedirs(os.environ["TEMP"], exist_ok=True)

    os.environ["GRADIO_TEMP_DIR"] = os.environ["TEMP"]
    os.environ['GRADIO_ANALYTICS_ENABLED'] = '0'


##############################################################################
# 4) Main-Funktion => Alle Tabs => .launch(share=...) 
##############################################################################

def run_unified():
    """
    Ein einziges Gradio-Interface mit:
    - Admin-Tab (Reset, Clear Output, Download ZIP, Log-Console)
    - roop Tabs (Faceswap, etc.)
    """
    # roop.globals.CFG laden
    if roop.globals.CFG is None:
        roop.globals.CFG = Settings("config.yaml")  # oder config_colab.yaml

    # Model-Downloads => pre_check()
    if not pre_check():
        print("Fehler: pre_check() fehlgeschlagen.")
        return

    # env
    prepare_environment()

    # roop-Ausgabe in Info => oder nutze 'logger' falls gewünscht
    set_display_ui(lambda msg: logger(msg))

    # GPU/CPU
    if roop.globals.CFG.provider == "cuda" and not util.has_cuda_device():
        roop.globals.CFG.provider = "cpu"

    from roop.core import decode_execution_providers
    roop.globals.execution_providers = decode_execution_providers([roop.globals.CFG.provider])
    gputype = util.get_device()
    if gputype == 'cuda':
        util.print_cuda_info()  # => prints => oder logger("...") via monkey-patch

    logger(f'Using provider {roop.globals.execution_providers} - Device:{gputype}')

    mycss = """
    span {color: var(--block-info-text-color)}
    #fixedheight {
        max-height: 238.4px;
        overflow-y: auto !important;
    }
    .image-container.svelte-1l6wqyv {height: 100%}
    """

    # EIN Blocks => EIN .launch => EIN .gradio.live
    with gr.Blocks(
        title=f'{roop.metadata.name} {roop.metadata.version}',
        theme=roop.globals.CFG.selected_theme,
        css=mycss,
        delete_cache=(60, 86400)
    ) as unified_app:

        gr.Markdown(f"## {roop.metadata.name} {roop.metadata.version} - Unified Admin + roop")

        # Admin-Tab
        with gr.Tab("Admin"):
            gr.Markdown("### roop-Admin-Funktionen")

            # Row 1: Reset-Button, Clear-Button
            with gr.Row():
                btn_reset = gr.Button("Neustart roop-Anwendung")
                txt_reset = gr.Textbox("", label="Reset Status", interactive=False)

                btn_clear = gr.Button("Clear Output-Folder")
                txt_clear = gr.Textbox("", label="Clear Status", interactive=False)

            btn_reset.click(fn=reset_roop, outputs=txt_reset)
            btn_clear.click(fn=clear_output_folder, outputs=txt_clear)

            # Row 2: Download ZIP
            with gr.Row():
                btn_zip = gr.Button("Download ZIP vom 'output'")
                file_zip = gr.File(label="ZIP-Download", interactive=False)
            btn_zip.click(fn=create_zip_for_download, outputs=file_zip)

            # Row 3: Konsole
            # - console => zeigt Logs an
            console = gr.Textbox(
                label="Konsole / Logs",
                value="",
                lines=10,
                max_lines=20,
                interactive=False
            )
            # Im Admin-Tab => load(...) => poll_logs alle 2 sek => console
            unified_app.load(fn=poll_logs, inputs=[console], outputs=[console], every=2)


        # roop-Tabs
        faceswap_tab()
        livecam_tab()
        facemgr_tab()
        extras_tab()
        settings_tab()

    # Start => .gradio.live => Kollege klickt => Admin => 
    #  - Reset roop, 
    #  - Clear output, 
    #  - Download zip, 
    #  - Logs
    unified_app.queue().launch(
        share=roop.globals.CFG.server_share,  # True/False laut config
        server_name=roop.globals.CFG.server_name if roop.globals.CFG.server_name else None,
        server_port=roop.globals.CFG.server_port if roop.globals.CFG.server_port > 0 else None,
        ssl_verify=False,
        show_error=True
    )


if __name__ == "__main__":
    run_unified()
