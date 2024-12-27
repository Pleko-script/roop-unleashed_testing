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

# Falls du sowas brauchst:
# from roop.ProcessMgr import ProcessMgr

# Standard-Flags
roop.globals.keep_fps = None
roop.globals.keep_frames = None
roop.globals.skip_audio = None
roop.globals.use_batch = None


def prepare_environment():
    """
    Legt output-, temp-Verzeichnisse an usw.
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
    'Neustart' - wir leeren z.B. globale roop-Variablen, GPU-Cache usw.
    Achtung: Dies beendet nicht den Python-Prozess, sondern räumt nur Variablen auf.
    """
    import gc
    # Beispiel: roop.globals.INPUT_FACESETS.clear(); roop.globals.TARGET_FACES.clear()
    roop.globals.INPUT_FACESETS.clear()
    roop.globals.TARGET_FACES.clear()

    # GPU-Cache leeren
    try:
        import torch
        torch.cuda.empty_cache()
    except:
        pass

    gc.collect()
    return "roop wurde neu initialisiert."


def run_unified():
    """
    EINE Gradio-App mit roop-Funktionalität + Admin-Funktionen.
    Kein Subprozess. Nur .launch(share=...) => ein .gradio.live.
    """

    # 1) roop.globals.CFG laden, wenn None
    if roop.globals.CFG is None:
        roop.globals.CFG = Settings("config.yaml")  # oder config_colab.yaml

    # 2) pre_check() => lädt fehlende onnx-Modelle herunter
    if not pre_check():
        print("Fehler: pre_check() fehlgeschlagen oder abgebrochen.")
        return

    # 3) Prepare environment
    prepare_environment()

    # 4) UI-Anzeige-Funktion
    set_display_ui(lambda msg: gr.Info(msg))

    # 5) evtl. GPU/CPU
    if roop.globals.CFG.provider == "cuda" and not util.has_cuda_device():
        roop.globals.CFG.provider = "cpu"

    roop.globals.execution_providers = decode_execution_providers([roop.globals.CFG.provider])
    gputype = util.get_device()
    if gputype == 'cuda':
        util.print_cuda_info()

    print(f'Using provider {roop.globals.execution_providers} - Device:{gputype}')

    # optionales CSS
    mycss = """
    span {color: var(--block-info-text-color)}
    #fixedheight {
        max-height: 238.4px;
        overflow-y: auto !important;
    }
    .image-container.svelte-1l6wqyv {height: 100%}
    """

    # 6) Ein einziges Gradio-Interface
    with gr.Blocks(
        title=f'{roop.metadata.name} {roop.metadata.version}',
        theme=roop.globals.CFG.selected_theme,
        css=mycss,
        delete_cache=(60, 86400)
    ) as unified_app:

        gr.Markdown(f"## {roop.metadata.name} {roop.metadata.version} - Unified Admin + roop")

        with gr.Tab("Admin"):
            gr.Markdown("### roop-Admin-Funktionen")
            reset_btn = gr.Button("Neustart roop-Anwendung")
            reset_status = gr.Textbox("", label="Status", interactive=False, lines=1)
            # Button klick => reset_roop()
            reset_btn.click(fn=reset_roop, outputs=reset_status)

        # 7) roop-Tabs
        faceswap_tab()
        livecam_tab()
        facemgr_tab()
        extras_tab()
        settings_tab()

    # 8) Nur ein queue().launch => ein .gradio.live
    unified_app.queue().launch(
        share=roop.globals.CFG.server_share,  # True/False laut config
        server_name=roop.globals.CFG.server_name if roop.globals.CFG.server_name else None,
        server_port=roop.globals.CFG.server_port if roop.globals.CFG.server_port > 0 else None,
        ssl_verify=False,
        show_error=True
    )


if __name__ == "__main__":
    run_unified()
