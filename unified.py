import os
import time
import gradio as gr
import roop.globals
import roop.metadata
import roop.utilities as util
import ui.globals as uii

# Falls nicht schon importiert:
from settings import Settings

# Importiere deine roop-Tabs:
from ui.tabs.faceswap_tab import faceswap_tab
from ui.tabs.livecam_tab import livecam_tab
from ui.tabs.facemgr_tab import facemgr_tab
from ui.tabs.extras_tab import extras_tab
from ui.tabs.settings_tab import settings_tab


def prepare_environment():
    """
    Output-, temp-Verzeichnisse anlegen usw.
    """
    # Hier wird roop.globals.CFG benötigt:
    roop.globals.output_path = os.path.abspath(os.path.join(os.getcwd(), "output"))
    os.makedirs(roop.globals.output_path, exist_ok=True)

    if not roop.globals.CFG.use_os_temp_folder:
        os.environ["TEMP"] = os.environ["TMP"] = os.path.abspath(os.path.join(os.getcwd(), "temp"))
    os.makedirs(os.environ["TEMP"], exist_ok=True)
    os.environ["GRADIO_TEMP_DIR"] = os.environ["TEMP"]
    os.environ['GRADIO_ANALYTICS_ENABLED'] = '0'


def reset_roop():
    """
    'Neustart': roop-Variablen leeren, GPU-Cache etc.
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

    return "roop wurde neu initialisiert!"


def run_unified():
    """
    Erzeugt EINE Gradio-App mit Admin-Tab + roop-Tabs.
    """
    # (A) roop.globals.CFG initialisieren, damit es nicht None ist:
    if roop.globals.CFG is None:
        roop.globals.CFG = Settings("config.yaml")  # oder config_colab.yaml
        # Falls du pre_check() etc. aus core.py brauchst, kannst du das hier anpassen.

    # (B) Environment vorbereiten
    prepare_environment()

    from roop.core import decode_execution_providers, set_display_ui
    set_display_ui(lambda msg: gr.Info(msg))

    # GPU/CPU-Check
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
            reset_btn = gr.Button("Neustart roop-Anwendung")
            reset_status = gr.Textbox("", label="Status", interactive=False, lines=1)
            reset_btn.click(fn=reset_roop, outputs=reset_status)

        # roop-Tabs
        faceswap_tab()
        livecam_tab()
        facemgr_tab()
        extras_tab()
        settings_tab()

    # EINE Launch-Aufruf => EINE .gradio.live
    unified_app.queue().launch(
        share=roop.globals.CFG.server_share,  # True/False je nach config
        server_name=roop.globals.CFG.server_name if roop.globals.CFG.server_name else None,
        server_port=roop.globals.CFG.server_port if roop.globals.CFG.server_port > 0 else None,
        ssl_verify=False,
        show_error=True
    )


if __name__ == "__main__":
    run_unified()
