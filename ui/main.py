import os
import time
import gradio as gr
import roop.globals
import roop.metadata
import roop.utilities as util
import ui.globals as uii

from ui.tabs.faceswap_tab import faceswap_tab
from ui.tabs.livecam_tab import livecam_tab
from ui.tabs.facemgr_tab import facemgr_tab
from ui.tabs.extras_tab import extras_tab
from ui.tabs.settings_tab import settings_tab


# Einige Default-Values werden von roop-Unleashed verwendet
roop.globals.keep_fps = None
roop.globals.keep_frames = None
roop.globals.skip_audio = None
roop.globals.use_batch = None


def prepare_environment():
    """
    Erzeugt das 'output'-Verzeichnis, setzt TEMP-Variablen etc.
    """
    roop.globals.output_path = os.path.abspath(os.path.join(os.getcwd(), "output"))
    os.makedirs(roop.globals.output_path, exist_ok=True)
    if not roop.globals.CFG.use_os_temp_folder:
        # Auf dem local Dir basierender temp-Folder
        os.environ["TEMP"] = os.environ["TMP"] = os.path.abspath(os.path.join(os.getcwd(), "temp"))
    os.makedirs(os.environ["TEMP"], exist_ok=True)
    os.environ["GRADIO_TEMP_DIR"] = os.environ["TEMP"]
    os.environ['GRADIO_ANALYTICS_ENABLED'] = '0'


def run():
    """
    Hier wird das Haupt-GUI (roop unleashed) gebaut und gestartet.
    Am Ende drucken wir den Link 'ROOPURL::<share_url>' für dein Admin-Interface.
    """
    from roop.core import decode_execution_providers, set_display_ui

    prepare_environment()
    set_display_ui(show_msg)

    # Falls "cuda" konfiguriert, aber keine GPU verfügbar => fallback CPU
    if roop.globals.CFG.provider == "cuda" and not util.has_cuda_device():
        roop.globals.CFG.provider = "cpu"

    roop.globals.execution_providers = decode_execution_providers([roop.globals.CFG.provider])
    gputype = util.get_device()
    if gputype == 'cuda':
        util.print_cuda_info()

    print(f'Using provider {roop.globals.execution_providers} - Device:{gputype}')

    run_server = True
    uii.ui_restart_server = False

    # Beispiel-CSS – kann man anpassen, falls gewünscht
    mycss = """
        span {color: var(--block-info-text-color)}
        #fixedheight {
            max-height: 238.4px;
            overflow-y: auto !important;
        }
        .image-container.svelte-1l6wqyv {height: 100%}
    """

    while run_server:
        server_name = roop.globals.CFG.server_name
        if not server_name:
            server_name = None

        server_port = roop.globals.CFG.server_port
        if server_port <= 0:
            server_port = None

        # Wenn in config.yaml "server_share: true" gesetzt ist => share=True
        ssl_verify = False if server_name == '0.0.0.0' else True

        with gr.Blocks(
            title=f'{roop.metadata.name} {roop.metadata.version}',
            theme=roop.globals.CFG.selected_theme,
            css=mycss,
            delete_cache=(60, 86400)
        ) as ui:
            with gr.Row(variant='compact'):
                gr.Markdown(
                    f"### [{roop.metadata.name} {roop.metadata.version}](https://github.com/C0untFloyd/roop-unleashed)"
                )
                # Versionen
                gr.HTML(util.create_version_html(), elem_id="versions")

            # Tabs aufbauen
            faceswap_tab()
            livecam_tab()
            facemgr_tab()
            extras_tab()
            settings_tab()

        launch_browser = roop.globals.CFG.launch_browser
        uii.ui_restart_server = False

        try:
            # Wichtig: Hier holen wir uns local_url, share_url
            local_url, share_url = ui.queue().launch(
                inbrowser=launch_browser,
                server_name=server_name,
                server_port=server_port,
                share=roop.globals.CFG.server_share,
                ssl_verify=ssl_verify,
                prevent_thread_lock=True,
                show_error=True
            )

            # **Zusatz**: Link in stdout ausgeben => "ROOPURL::<Link>"
            if share_url:
                print(f"ROOPURL::{share_url}")
            else:
                print("ROOPURL::(Kein Share-Link)")

        except Exception as e:
            print(f'Exception {e} when launching Gradio Server!')
            uii.ui_restart_server = True
            run_server = False

        try:
            # Warte im Sekundentakt, bis ui_restart_server getriggert wird
            while not uii.ui_restart_server:
                time.sleep(1.0)
        except (KeyboardInterrupt, OSError):
            print("Keyboard interruption in main thread... closing server.")
            run_server = False

        # UI schließen (gradio blocks)
        ui.close()


def show_msg(msg: str):
    """
    Für roop.core.set_display_ui: gibt Meldungen als gr.Info aus.
    """
    gr.Info(msg)
