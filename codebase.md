# settings.py

```py
import yaml

class Settings:
    def __init__(self, config_file):
        self.config_file = config_file
        self.load()

    def default_get(_, data, name, default):
        value = default
        try:
            value = data.get(name, default)
        except:
            pass
        return value


    def load(self):
        try:
            with open(self.config_file, 'r') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
        except:
            data = None

        self.selected_theme = self.default_get(data, 'selected_theme', "Default")
        self.server_name = self.default_get(data, 'server_name', "")
        self.server_port = self.default_get(data, 'server_port', 0)
        self.server_share = self.default_get(data, 'server_share', False)
        self.output_image_format = self.default_get(data, 'output_image_format', 'png')
        self.output_video_format = self.default_get(data, 'output_video_format', 'mp4')
        self.output_video_codec = self.default_get(data, 'output_video_codec', 'libx264')
        self.video_quality = self.default_get(data, 'video_quality', 14)
        self.clear_output = self.default_get(data, 'clear_output', True)
        self.max_threads = self.default_get(data, 'max_threads', 2)
        self.memory_limit = self.default_get(data, 'memory_limit', 0)
        self.provider = self.default_get(data, 'provider', 'cuda')
        self.force_cpu = self.default_get(data, 'force_cpu', False)
        self.output_template = self.default_get(data, 'output_template', '{file}_{time}')
        self.use_os_temp_folder = self.default_get(data, 'use_os_temp_folder', False)
        self.output_show_video = self.default_get(data, 'output_show_video', True)
        self.launch_browser = self.default_get(data, 'launch_browser', True)





    def save(self):
        data = {
            'selected_theme': self.selected_theme,
            'server_name': self.server_name,
            'server_port': self.server_port,
            'server_share': self.server_share,
            'output_image_format' : self.output_image_format,
            'output_video_format' : self.output_video_format,
            'output_video_codec' : self.output_video_codec,
            'video_quality' : self.video_quality,
            'clear_output' : self.clear_output,
            'max_threads' : self.max_threads,
            'memory_limit' : self.memory_limit,
            'provider' : self.provider,
            'force_cpu' : self.force_cpu,
			'output_template' : self.output_template,
            'use_os_temp_folder' : self.use_os_temp_folder,
            'output_show_video' : self.output_show_video
        }
        with open(self.config_file, 'w') as f:
            yaml.dump(data, f)




```

# runMacOS.sh

```sh
#!/bin/bash

# Check if we are in the correct repository directory
if [ ! -f "run.py" ]; then
    echo "run.py not found!"
    exit 1
fi

# Create a hidden Python 3.11 virtual environment in the .venv folder
VENV_DIR=".venv"

# Check if Python 3.11 is installed
if ! brew list --versions python@3.11 >/dev/null; then
    echo "Python 3.11 is not installed. Please install it first."
    exit 1
fi

# Use Python 3.11 to create the virtual environment
echo "Creating a virtual environment using Python 3.11..."
python3.11 -m venv $VENV_DIR

# Activate the virtual environment
echo "Activating the virtual environment..."
source "$VENV_DIR/bin/activate"

# Check if the activation was successful
if [ "$VIRTUAL_ENV" != "" ]; then
    echo "Virtual environment activated successfully."
else
    echo "Failed to activate the virtual environment."
    exit 1
fi

# Install dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping dependency installation."
fi

# Run roop-unleashed. This can take a while - especially at first startup...
echo "Running the run.py script..."
python run.py

# Deactivate the virtual environment after execution
echo "Deactivating the virtual environment..."
deactivate
```

# run.py

```py
#!/usr/bin/env python3

from roop import core

if __name__ == '__main__':
    core.run()

```

# roop-unleashed.ipynb

```ipynb
{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "G9BdiCppV6AS"
      },
      "source": [
        "# Colab for roop-unleashed - Gradio version\n",
        "https://github.com/C0untFloyd/roop-unleashed\n"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "CanIXgLJgaOj"
      },
      "source": [
        "Install CUDA V11.8 on Google Cloud Compute"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "96GE4UgYg3Ej"
      },
      "outputs": [],
      "source": [
        "!apt-get -y update\n",
        "!apt-get -y install cuda-toolkit-11-8\n",
        "import os\n",
        "os.environ[\"LD_LIBRARY_PATH\"] += \":\" + \"/usr/local/cuda-11/lib64\"\n",
        "os.environ[\"LD_LIBRARY_PATH\"] += \":\" + \"/usr/local/cuda-11.8/lib64\""
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "0ZYRNb0AWLLW"
      },
      "source": [
        "Installing & preparing requirements"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "t1yPuhdySqCq"
      },
      "outputs": [],
      "source": [
        "!git clone https://github.com/C0untFloyd/roop-unleashed.git\n",
        "%cd roop-unleashed\n",
        "!mv config_colab.yaml config.yaml\n",
        "!pip install -r requirements.txt"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "u_4JQiSlV9Fi"
      },
      "source": [
        "Running roop-unleashed with default config"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "Is6U2huqSzLE"
      },
      "outputs": [],
      "source": [
        "!python run.py"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "UdQ1VHdI8lCf"
      },
      "source": [
        "### Download generated images folder\n",
        "(only needed if you want to zip the generated output)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 17
        },
        "id": "oYjWveAmw10X",
        "outputId": "5b4c3650-f951-434a-c650-5525a8a70c1e"
      },
      "outputs": [
        {
          "data": {
            "application/javascript": "\n    async function download(id, filename, size) {\n      if (!google.colab.kernel.accessAllowed) {\n        return;\n      }\n      const div = document.createElement('div');\n      const label = document.createElement('label');\n      label.textContent = `Downloading \"${filename}\": `;\n      div.appendChild(label);\n      const progress = document.createElement('progress');\n      progress.max = size;\n      div.appendChild(progress);\n      document.body.appendChild(div);\n\n      const buffers = [];\n      let downloaded = 0;\n\n      const channel = await google.colab.kernel.comms.open(id);\n      // Send a message to notify the kernel that we're ready.\n      channel.send({})\n\n      for await (const message of channel.messages) {\n        // Send a message to notify the kernel that we're ready.\n        channel.send({})\n        if (message.buffers) {\n          for (const buffer of message.buffers) {\n            buffers.push(buffer);\n            downloaded += buffer.byteLength;\n            progress.value = downloaded;\n          }\n        }\n      }\n      const blob = new Blob(buffers, {type: 'application/binary'});\n      const a = document.createElement('a');\n      a.href = window.URL.createObjectURL(blob);\n      a.download = filename;\n      div.appendChild(a);\n      a.click();\n      div.remove();\n    }\n  ",
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {},
          "output_type": "display_data"
        },
        {
          "data": {
            "application/javascript": "download(\"download_789eab11-93d2-4880-adf3-6aceee0cc5f9\", \"fake_output.zip.zip\", 80125)",
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {},
          "output_type": "display_data"
        }
      ],
      "source": [
        "import shutil\n",
        "import os\n",
        "from google.colab import files\n",
        "\n",
        "def zip_directory(directory_path, zip_path):\n",
        "    shutil.make_archive(zip_path, 'zip', directory_path)\n",
        "\n",
        "# Set the directory path you want to download\n",
        "directory_path = '/content/roop-unleashed/output'\n",
        "\n",
        "# Set the zip file name\n",
        "zip_filename = 'fake_output.zip'\n",
        "\n",
        "# Zip the directory\n",
        "zip_directory(directory_path, zip_filename)\n",
        "\n",
        "# Download the zip file\n",
        "files.download(zip_filename+'.zip')\n"
      ]
    }
  ],
  "metadata": {
    "accelerator": "GPU",
    "colab": {
      "collapsed_sections": [
        "UdQ1VHdI8lCf"
      ],
      "gpuType": "T4",
      "provenance": []
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}

```

# requirements.txt

```txt
--extra-index-url https://download.pytorch.org/whl/cu118

numpy==1.26.4
gradio==4.44.0
fastapi<0.113.0
opencv-python-headless==4.9.0.80
onnx==1.16.0
insightface==0.7.3
albucore==0.0.16
psutil==5.9.6
torch==2.1.2+cu118; sys_platform != 'darwin'
torch==2.1.2; sys_platform == 'darwin'
torchvision==0.16.2+cu118; sys_platform != 'darwin'
torchvision==0.16.2; sys_platform == 'darwin'
onnxruntime==1.17.1; sys_platform == 'darwin' and platform_machine != 'arm64'
onnxruntime-silicon==1.16.3; sys_platform == 'darwin' and platform_machine == 'arm64'
onnxruntime-gpu==1.17.1; sys_platform != 'darwin'
tqdm==4.66.4
ftfy
regex
pyvirtualcam

```

# README.md

```md
# roop-unleashed

[Changelog](#changelog) • [Usage](#usage) • [Wiki](https://github.com/C0untFloyd/roop-unleashed/wiki)


Uncensored Deepfakes for images and videos without training and an easy-to-use GUI.


![Screen](https://github.com/C0untFloyd/roop-unleashed/assets/131583554/6ee6860d-efbe-4337-8c62-a67598863637)

### Features

- Platform-independant Browser GUI
- Selection of multiple input/output faces in one go
- Many different swapping modes, first detected, face selections, by gender
- Batch processing of images/videos
- Masking of face occluders using text prompts or automatically
- Optional Face Upscaler/Restoration using different enhancers
- Preview swapping from different video frames
- Live Fake Cam using your webcam
- Extras Tab for cutting videos etc.
- Settings - storing configuration for next session
- Theme Support

and lots more...


## Disclaimer

This project is for technical and academic use only.
Users of this software are expected to use this software responsibly while abiding the local law. If a face of a real person is being used, users are suggested to get consent from the concerned person and clearly mention that it is a deepfake when posting content online. Developers of this software will not be responsible for actions of end-users.
**Please do not apply it to illegal and unethical scenarios.**

In the event of violation of the legal and ethical requirements of the user's country or region, this code repository is exempt from liability

### Installation

Please refer to the [wiki](https://github.com/C0untFloyd/roop-unleashed/wiki).

#### macOS Installation
Simply run the following command. It will check and install all dependencies if necessary.

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/PJF16/roop-unleashed/master/installer/macOSinstaller.sh)"`



### Usage

- Windows: run the `windows_run.bat` from the Installer.
- Linux: `python run.py`
- macOS: `sh runMacOS.sh`
- Dockerfile:
  \`\`\`shell
  docker build -t roop-unleashed . && docker run -t \
    -p 7860:7860 \
    -v ./config.yaml:/app/config.yaml \
    -v ./models:/app/models \
    -v ./temp:/app/temp \
    -v ./output:/app/output \
    roop-unleashed
  \`\`\`

<a target="_blank" href="https://colab.research.google.com/github/C0untFloyd/roop-unleashed/blob/main/roop-unleashed.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>
  

Additional commandline arguments are currently unsupported and settings should be done via the UI.

> Note: When you run this program for the first time, it will download some models roughly ~2Gb in size.




### Changelog

**28.9.2024** v4.3.1

- Bugfix: Several possible memory leaks
- Added different output modes, e.g. to virtual cam stream
- New swapping mode "All input faces"
- Average total fps displayed and setting for autorun


**16.9.2024** v4.2.8

- Bugfix: Starting roop-unleashed without NVIDIA gpu but cuda option enabled
- Bugfix: Target Faces couldn't be moved left/right
- Bugfix: Enhancement and upscaling working again in virtual cam
- Corrupt videos caught when adding to target files, displaying warning msg
- Source Files Component cleared after face detection to release temp files
- Added masking and mouth restore options to virtual cam


**9.9.2024** v4.2.3

- Hotfix for gradio pydantic issue with fastapi
- Upgraded to Gradio 4.43 hoping it will fix remaining issues
- Added new action when no face detected -> use last swapped
- Specified image format for image controls - opening new tabs on preview images possible again!
- Hardcoded image output format for livecam to jpeg - might be faster than previous webp
- Chain events to be only executed if previous was a success


**5.9.2024** v4.2.0

- Added ability to move input & target faces order
- New CLI Arguments override settings
- Small UI changes to faceswapping tab
- Added mask option and code for restoration of original mouth area
- Updated gradio to v4.42.0
- Added CLI Arguments --server_share and --cuda_device_id
- Added webp image support


**15.07.2024** v4.1.1

- Bugfix: Post-processing after swapping


**14.07.2024** v4.1.0

- Added subsample upscaling to increase swap resolution
- Upgraded gradio


**12.05.2024** v4.0.0

- Bugfix: Unnecessary init every frame in live-cam
- Bugfix: Installer downloading insightface package each run
- Added xseg masking to live-cam
- Added realesrganx2 to frame processors
- Upgraded some requirements
- Added subtypes and different model support to frame processors
- Allow frame processors to change resolutions of videos
- Different OpenCV Cap for MacOS Virtual Cam
- Added complete frame processing to extras tab
- Colorize, upscale and misc filters added


**22.04.2024** v3.9.0

- Bugfix: Face detection bounding box corrupt values at weird angles
- Rewrote mask previewing to work with every model
- Switching mask engines toggles text interactivity
- Clearing target files, resets face selection dropdown
- Massive rewrite of swapping architecture, needed for xseg implementation
- Added DFL Xseg Support for partial face occlusion
- Face masking only runs when there is a face detected
- Removed unnecessary toggle checkbox for text masking


**22.03.2024** v3.6.5

- Bugfix: Installer pulling latest update on first installation
- Bugfix: Regression issue, blurring/erosion missing from face swap
- Exposed erosion and blur amounts to UI
- Using same values for manual masking too


**20.03.2024** v3.6.3

- Bugfix: Workaround for Gradio Slider Change Bug
- Bugfix: CSS Styling to fix Gradio Image Height Bug
- Made face swapping mask offsets resolution independant
- Show offset mask as overlay
- Changed layout for masking


**18.03.2024** v3.6.0

- Updated to Gradio 4.21.0 - requiring many changes under the hood
- New manual masking (draw the mask yourself)
- Extras Tab, streamlined cutting/joining videos
- Re-added face selection by gender (on-demand loading, default turned off)
- Removed unnecessary activate live-cam option
- Added time info to preview frame and changed frame slider event to allow faster changes


**10.03.2024** v3.5.5

- Bugfix: Installer Path Env
- Bugfix: file attributes
- Video processing checks for presence of ffmpeg and displays warning if not found
- Removed gender + age detection to speed up processing. Option removed from UI
- Replaced restoreformer with restoreformer++
- Live Cam recoded to run separate from virtual cam and without blocking controls
- Swapping with only 1 target face allows selecting from several input faces



**08.01.2024** v3.5.0

- Bugfix: wrong access options when creating folders
- New auto rotation of horizontal faces, fixing bad landmark positions (expanded on ![PR 364](https://github.com/C0untFloyd/roop-unleashed/pull/364))
- Simple VR Option for stereo Images/Movies, best used in selected face mode
- Added RestoreFormer Enhancer - https://github.com/wzhouxiff/RestoreFormer
- Bumped up package versions for onnx/Torch etc.   


**16.10.2023** v3.3.4

**11.8.2023** v2.7.0

Initial Gradio Version - old TkInter Version now deprecated

- Re-added unified padding to face enhancers
- Fixed DMDNet for all resolutions
- Selecting target face now automatically switches swapping mode to selected
- GPU providers are correctly set using the GUI (needs restart currently)
- Local output folder can be opened from page
- Unfinished extras functions disabled for now
- Installer checks out specific commit, allowing to go back to first install
- Updated readme for new gradio version
- Updated Colab


# Acknowledgements

Lots of ideas, code or pre-trained models borrowed from the following projects:

https://github.com/deepinsight/insightface<br />
https://github.com/s0md3v/roop<br />
https://github.com/AUTOMATIC1111/stable-diffusion-webui<br /> 
https://github.com/Hillobar/Rope<br />
https://github.com/TencentARC/GFPGAN<br />   
https://github.com/kadirnar/codeformer-pip<br />
https://github.com/csxmli2016/DMDNet<br />
https://github.com/glucauze/sd-webui-faceswaplab<br />
https://github.com/ykk648/face_power<br />

<br />
<br />
Thanks to all developers!


```

# mypy.ini

```ini
[mypy]
check_untyped_defs = True
disallow_any_generics = True
disallow_untyped_calls = True
disallow_untyped_defs = True
ignore_missing_imports = True
strict_optional = False

```

# Dockerfile

```
FROM python:3.11

# making app folder
WORKDIR /app

# copying files
COPY . .

# installing requirements
RUN apt-get update 
RUN apt-get install ffmpeg -y
RUN pip install --upgrade pip 
RUN pip install -r ./requirements.txt 

# launching gradio app 
ENV GRADIO_SERVER_NAME="0.0.0.0"
EXPOSE 7860
ENTRYPOINT python ./run.py
```

# config_colab.yaml

```yaml
clear_output: true
force_cpu: false
max_threads: 3
memory_limit: 0
output_image_format: png
output_template: '{file}_{time}'
output_video_codec: libx264
output_video_format: mp4
provider: cuda
selected_theme: Default
server_name: ''
server_port: 0
server_share: true
video_quality: 14

```

# .gitignore

```
.vs
.idea
models
temp
__pycache__
*.pth
/start.bat
/env
.vscode
output
temp
config.yaml
run.bat
venv
start.sh
```

# .flake8

```
[flake8]
select = E3, E4, F
per-file-ignores = roop/core.py:E402
```

# .aidigestignore

```
LICENSE
.vs
.idea
models
temp
__pycache__
*.pth
/start.bat
/env
.vscode
output
temp
config.yaml
run.bat
venv
start.sh
```

# ui\main.py

```py
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

roop.globals.keep_fps = None
roop.globals.keep_frames = None
roop.globals.skip_audio = None
roop.globals.use_batch = None


def prepare_environment():
    roop.globals.output_path = os.path.abspath(os.path.join(os.getcwd(), "output"))
    os.makedirs(roop.globals.output_path, exist_ok=True)
    if not roop.globals.CFG.use_os_temp_folder:
        os.environ["TEMP"] = os.environ["TMP"] = os.path.abspath(os.path.join(os.getcwd(), "temp"))
    os.makedirs(os.environ["TEMP"], exist_ok=True)
    os.environ["GRADIO_TEMP_DIR"] = os.environ["TEMP"]
    os.environ['GRADIO_ANALYTICS_ENABLED'] = '0'

def run():
    from roop.core import decode_execution_providers, set_display_ui

    prepare_environment()

    set_display_ui(show_msg)
    if roop.globals.CFG.provider == "cuda" and util.has_cuda_device() == False:
       roop.globals.CFG.provider = "cpu"

    roop.globals.execution_providers = decode_execution_providers([roop.globals.CFG.provider])
    gputype = util.get_device()
    if gputype == 'cuda':
        util.print_cuda_info()
        
    print(f'Using provider {roop.globals.execution_providers} - Device:{gputype}')
    
    run_server = True
    uii.ui_restart_server = False
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
        if server_name is None or len(server_name) < 1:
            server_name = None
        server_port = roop.globals.CFG.server_port
        if server_port <= 0:
            server_port = None
        ssl_verify = False if server_name == '0.0.0.0' else True
        with gr.Blocks(title=f'{roop.metadata.name} {roop.metadata.version}', theme=roop.globals.CFG.selected_theme, css=mycss, delete_cache=(60, 86400)) as ui:
            with gr.Row(variant='compact'):
                    gr.Markdown(f"### [{roop.metadata.name} {roop.metadata.version}](https://github.com/C0untFloyd/roop-unleashed)")
                    gr.HTML(util.create_version_html(), elem_id="versions")
            faceswap_tab()
            livecam_tab()
            facemgr_tab()
            extras_tab()
            settings_tab()
        launch_browser = roop.globals.CFG.launch_browser

        uii.ui_restart_server = False
        try:
            ui.queue().launch(inbrowser=launch_browser, server_name=server_name, server_port=server_port, share=roop.globals.CFG.server_share, ssl_verify=ssl_verify, prevent_thread_lock=True, show_error=True)
        except Exception as e:
            print(f'Exception {e} when launching Gradio Server!')
            uii.ui_restart_server = True
            run_server = False
        try:
            while uii.ui_restart_server == False:
                time.sleep(1.0)

        except (KeyboardInterrupt, OSError):
            print("Keyboard interruption in main thread... closing server.")
            run_server = False
        ui.close()


def show_msg(msg: str):
    gr.Info(msg)


```

# ui\globals.py

```py
ui_restart_server = False

SELECTION_FACES_DATA = None
ui_SELECTED_INPUT_FACE_INDEX = 0

ui_selected_enhancer = None
ui_upscale = None
ui_blend_ratio = None
ui_input_thumbs = []
ui_target_thumbs = []
ui_camera_frame = None






```

# roop\__init__.py

```py

```

# roop\vr_util.py

```py
import cv2
import numpy as np

# VR Lense Distortion
# Taken from https://github.com/g0kuvonlange/vrswap


def get_perspective(img, FOV, THETA, PHI, height, width):
    #
    # THETA is left/right angle, PHI is up/down angle, both in degree
    #
    [orig_width, orig_height, _] = img.shape
    equ_h = orig_height
    equ_w = orig_width
    equ_cx = (equ_w - 1) / 2.0
    equ_cy = (equ_h - 1) / 2.0

    wFOV = FOV
    hFOV = float(height) / width * wFOV

    w_len = np.tan(np.radians(wFOV / 2.0))
    h_len = np.tan(np.radians(hFOV / 2.0))

    x_map = np.ones([height, width], np.float32)
    y_map = np.tile(np.linspace(-w_len, w_len, width), [height, 1])
    z_map = -np.tile(np.linspace(-h_len, h_len, height), [width, 1]).T

    D = np.sqrt(x_map**2 + y_map**2 + z_map**2)
    xyz = np.stack((x_map, y_map, z_map), axis=2) / np.repeat(
        D[:, :, np.newaxis], 3, axis=2
    )

    y_axis = np.array([0.0, 1.0, 0.0], np.float32)
    z_axis = np.array([0.0, 0.0, 1.0], np.float32)
    [R1, _] = cv2.Rodrigues(z_axis * np.radians(THETA))
    [R2, _] = cv2.Rodrigues(np.dot(R1, y_axis) * np.radians(-PHI))

    xyz = xyz.reshape([height * width, 3]).T
    xyz = np.dot(R1, xyz)
    xyz = np.dot(R2, xyz).T
    lat = np.arcsin(xyz[:, 2])
    lon = np.arctan2(xyz[:, 1], xyz[:, 0])

    lon = lon.reshape([height, width]) / np.pi * 180
    lat = -lat.reshape([height, width]) / np.pi * 180

    lon = lon / 180 * equ_cx + equ_cx
    lat = lat / 90 * equ_cy + equ_cy

    persp = cv2.remap(
        img,
        lon.astype(np.float32),
        lat.astype(np.float32),
        cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_WRAP,
    )
    return persp

```

# roop\virtualcam.py

```py
import cv2
import roop.globals
import ui.globals
import pyvirtualcam
import threading
import platform


cam_active = False
cam_thread = None
vcam = None

def virtualcamera(streamobs, use_xseg, use_mouthrestore, cam_num,width,height):
    from roop.ProcessOptions import ProcessOptions
    from roop.core import live_swap, get_processing_plugins

    global cam_active

    #time.sleep(2)
    print('Starting capture')
    cap = cv2.VideoCapture(cam_num, cv2.CAP_DSHOW if platform.system() != 'Darwin' else cv2.CAP_AVFOUNDATION)
    if not cap.isOpened():
        print("Cannot open camera")
        cap.release()
        del cap
        return

    pref_width = width
    pref_height = height
    pref_fps_in = 30
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, pref_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, pref_height)
    cap.set(cv2.CAP_PROP_FPS, pref_fps_in)
    cam_active = True

    # native format UYVY

    cam = None
    if streamobs:
        print('Detecting virtual cam devices')
        cam = pyvirtualcam.Camera(width=pref_width, height=pref_height, fps=pref_fps_in, fmt=pyvirtualcam.PixelFormat.BGR, print_fps=False)
    if cam:
        print(f'Using virtual camera: {cam.device}')
        print(f'Using {cam.native_fmt}')
    else:
        print(f'Not streaming to virtual camera!')
    subsample_size = roop.globals.subsample_size


    options = ProcessOptions(get_processing_plugins("mask_xseg" if use_xseg else None), roop.globals.distance_threshold, roop.globals.blend_ratio,
                              "all", 0, None, None, 1, subsample_size, False, use_mouthrestore)
    while cam_active:
        ret, frame = cap.read()
        if not ret:
            break

        if len(roop.globals.INPUT_FACESETS) > 0:
            frame = live_swap(frame, options)
        if cam:
            cam.send(frame)
            cam.sleep_until_next_frame()
        ui.globals.ui_camera_frame = frame

    if cam:
        cam.close()
    cap.release()
    print('Camera stopped')



def start_virtual_cam(streamobs, use_xseg, use_mouthrestore, cam_number, resolution):
    global cam_thread, cam_active

    if not cam_active:
        width, height = map(int, resolution.split('x'))
        cam_thread = threading.Thread(target=virtualcamera, args=[streamobs, use_xseg, use_mouthrestore, cam_number, width, height])
        cam_thread.start()



def stop_virtual_cam():
    global cam_active, cam_thread

    if cam_active:
        cam_active = False
        cam_thread.join()



```

# roop\util_ffmpeg.py

```py

import os
import subprocess
import roop.globals
import roop.utilities as util

from typing import List, Any

def run_ffmpeg(args: List[str]) -> bool:
    commands = ['ffmpeg', '-hide_banner', '-hwaccel', 'auto', '-y', '-loglevel', roop.globals.log_level]
    commands.extend(args)
    print ("Running ffmpeg")
    try:
        subprocess.check_output(commands, stderr=subprocess.STDOUT)
        return True
    except Exception as e:
        print("Running ffmpeg failed! Commandline:")
        print (" ".join(commands))
    return False



def cut_video(original_video: str, cut_video: str, start_frame: int, end_frame: int, reencode: bool):
    fps = util.detect_fps(original_video)
    start_time = start_frame / fps
    num_frames = end_frame - start_frame

    if reencode:
        run_ffmpeg(['-ss',  format(start_time, ".2f"), '-i', original_video, '-c:v', roop.globals.video_encoder, '-c:a', 'aac', '-frames:v', str(num_frames), cut_video])
    else:
        run_ffmpeg(['-ss',  format(start_time, ".2f"), '-i', original_video,  '-frames:v', str(num_frames), '-c:v' ,'copy','-c:a' ,'copy', cut_video])

def join_videos(videos: List[str], dest_filename: str, simple: bool):
    if simple:
        txtfilename = util.resolve_relative_path('../temp')
        txtfilename = os.path.join(txtfilename, 'joinvids.txt')
        with open(txtfilename, "w", encoding="utf-8") as f:
            for v in videos:
                 v = v.replace('\\', '/')
                 f.write(f"file {v}\n")
        commands = ['-f', 'concat', '-safe', '0', '-i', f'{txtfilename}', '-vcodec', 'copy', f'{dest_filename}']
        run_ffmpeg(commands)

    else:
        inputs = []
        filter = ''
        for i,v in enumerate(videos):
            inputs.append('-i')
            inputs.append(v)
            filter += f'[{i}:v:0][{i}:a:0]'
        run_ffmpeg([" ".join(inputs), '-filter_complex', f'"{filter}concat=n={len(videos)}:v=1:a=1[outv][outa]"', '-map', '"[outv]"', '-map', '"[outa]"', dest_filename])    

        #     filter += f'[{i}:v:0][{i}:a:0]'
        # run_ffmpeg([" ".join(inputs), '-filter_complex', f'"{filter}concat=n={len(videos)}:v=1:a=1[outv][outa]"', '-map', '"[outv]"', '-map', '"[outa]"', dest_filename])    



def extract_frames(target_path : str, trim_frame_start, trim_frame_end, fps : float) -> bool:
    util.create_temp(target_path)
    temp_directory_path = util.get_temp_directory_path(target_path)
    commands = ['-i', target_path, '-q:v', '1', '-pix_fmt', 'rgb24', ]
    if trim_frame_start is not None and trim_frame_end is not None:
        commands.extend([ '-vf', 'trim=start_frame=' + str(trim_frame_start) + ':end_frame=' + str(trim_frame_end) + ',fps=' + str(fps) ])
    commands.extend(['-vsync', '0', os.path.join(temp_directory_path, '%06d.' + roop.globals.CFG.output_image_format)])
    return run_ffmpeg(commands)


def create_video(target_path: str, dest_filename: str, fps: float = 24.0, temp_directory_path: str = None) -> None:
    if temp_directory_path is None:
        temp_directory_path = util.get_temp_directory_path(target_path)
    run_ffmpeg(['-r', str(fps), '-i', os.path.join(temp_directory_path, f'%06d.{roop.globals.CFG.output_image_format}'), '-c:v', roop.globals.video_encoder, '-crf', str(roop.globals.video_quality), '-pix_fmt', 'yuv420p', '-vf', 'colorspace=bt709:iall=bt601-6-625:fast=1', '-y', dest_filename])
    return dest_filename


def create_gif_from_video(video_path: str, gif_path):
    from roop.capturer import get_video_frame, release_video

    fps = util.detect_fps(video_path)
    frame = get_video_frame(video_path)
    release_video()

    scalex = frame.shape[0]
    scaley = frame.shape[1]

    if scalex >= scaley:
        scaley = -1
    else:
        scalex = -1

    run_ffmpeg(['-i', video_path, '-vf', f'fps={fps},scale={int(scalex)}:{int(scaley)}:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', '-loop', '0', gif_path])



def create_video_from_gif(gif_path: str, output_path):
    fps = util.detect_fps(gif_path)
    filter = """scale='trunc(in_w/2)*2':'trunc(in_h/2)*2',format=yuv420p,fps=10"""
    run_ffmpeg(['-i', gif_path, '-vf', f'"{filter}"', '-movflags', '+faststart', '-shortest', output_path])


def repair_video(original_video: str, final_video : str):
    run_ffmpeg(['-i', original_video, '-movflags', 'faststart', '-acodec', 'copy', '-vcodec', 'copy', final_video])


def restore_audio(intermediate_video: str, original_video: str, trim_frame_start, trim_frame_end, final_video : str) -> None:
	fps = util.detect_fps(original_video)
	commands = [ '-i', intermediate_video ]
	if trim_frame_start is None and trim_frame_end is None:
		commands.extend([ '-c:a', 'copy' ])
	else:
		# if trim_frame_start is not None:
		# 	start_time = trim_frame_start / fps
		# 	commands.extend([ '-ss', format(start_time, ".2f")])
		# else:
		# 	commands.extend([ '-ss', '0' ])
		# if trim_frame_end is not None:
		# 	end_time = trim_frame_end / fps
		# 	commands.extend([ '-to', format(end_time, ".2f")])
		# commands.extend([ '-c:a', 'aac' ])
		if trim_frame_start is not None:
			start_time = trim_frame_start / fps
			commands.extend([ '-ss', format(start_time, ".2f")])
		else:
			commands.extend([ '-ss', '0' ])
		if trim_frame_end is not None:
			end_time = trim_frame_end / fps
			commands.extend([ '-to', format(end_time, ".2f")])
		commands.extend([ '-i', original_video, "-c",  "copy" ])

	commands.extend([ '-map', '0:v:0', '-map', '1:a:0?', '-shortest', final_video ])
	run_ffmpeg(commands)

```

# roop\utilities.py

```py
import glob
import mimetypes
import os
import platform
import shutil
import ssl
import subprocess
import sys
import urllib
import torch
import gradio
import tempfile
import cv2
import zipfile
import traceback
import threading
import threading

from typing import Union, Any
from contextlib import nullcontext

from pathlib import Path
from typing import List, Any
from tqdm import tqdm
from scipy.spatial import distance

import roop.template_parser as template_parser

import roop.globals

TEMP_FILE = "temp.mp4"
TEMP_DIRECTORY = "temp"

THREAD_SEMAPHORE = threading.Semaphore()
NULL_CONTEXT  = nullcontext()


# monkey patch ssl for mac
if platform.system().lower() == "darwin":
    ssl._create_default_https_context = ssl._create_unverified_context


# https://github.com/facefusion/facefusion/blob/master/facefusion
def detect_fps(target_path: str) -> float:
    fps = 24.0
    cap = cv2.VideoCapture(target_path)
    if cap.isOpened():
        fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return fps


# Gradio wants Images in RGB
def convert_to_gradio(image):
    if image is None:
        return None
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def sort_filenames_ignore_path(filenames):
    """Sorts a list of filenames containing a complete path by their filename,
    while retaining their original path.

    Args:
      filenames: A list of filenames containing a complete path.

    Returns:
      A sorted list of filenames containing a complete path.
    """
    filename_path_tuples = [
        (os.path.split(filename)[1], filename) for filename in filenames
    ]
    sorted_filename_path_tuples = sorted(filename_path_tuples, key=lambda x: x[0])
    return [
        filename_path_tuple[1] for filename_path_tuple in sorted_filename_path_tuples
    ]


def sort_rename_frames(path: str):
    filenames = os.listdir(path)
    filenames.sort()
    for i in range(len(filenames)):
        of = os.path.join(path, filenames[i])
        newidx = i + 1
        new_filename = os.path.join(
            path, f"{newidx:06d}." + roop.globals.CFG.output_image_format
        )
        os.rename(of, new_filename)


def get_temp_frame_paths(target_path: str) -> List[str]:
    temp_directory_path = get_temp_directory_path(target_path)
    return glob.glob(
        (
            os.path.join(
                glob.escape(temp_directory_path),
                f"*.{roop.globals.CFG.output_image_format}",
            )
        )
    )


def get_temp_directory_path(target_path: str) -> str:
    target_name, _ = os.path.splitext(os.path.basename(target_path))
    target_directory_path = os.path.dirname(target_path)
    return os.path.join(target_directory_path, TEMP_DIRECTORY, target_name)


def get_temp_output_path(target_path: str) -> str:
    temp_directory_path = get_temp_directory_path(target_path)
    return os.path.join(temp_directory_path, TEMP_FILE)


def normalize_output_path(source_path: str, target_path: str, output_path: str) -> Any:
    if source_path and target_path:
        source_name, _ = os.path.splitext(os.path.basename(source_path))
        target_name, target_extension = os.path.splitext(os.path.basename(target_path))
        if os.path.isdir(output_path):
            return os.path.join(
                output_path, source_name + "-" + target_name + target_extension
            )
    return output_path


def get_destfilename_from_path(
    srcfilepath: str, destfilepath: str, extension: str
) -> str:
    fn, ext = os.path.splitext(os.path.basename(srcfilepath))
    if "." in extension:
        return os.path.join(destfilepath, f"{fn}{extension}")
    return os.path.join(destfilepath, f"{fn}{extension}{ext}")


def replace_template(file_path: str, index: int = 0) -> str:
    fn, ext = os.path.splitext(os.path.basename(file_path))

    # Remove the "__temp" placeholder that was used as a temporary filename
    fn = fn.replace("__temp", "")

    template = roop.globals.CFG.output_template
    replaced_filename = template_parser.parse(
        template, {"index": str(index), "file": fn}
    )

    return os.path.join(roop.globals.output_path, f"{replaced_filename}{ext}")


def create_temp(target_path: str) -> None:
    temp_directory_path = get_temp_directory_path(target_path)
    Path(temp_directory_path).mkdir(parents=True, exist_ok=True)


def move_temp(target_path: str, output_path: str) -> None:
    temp_output_path = get_temp_output_path(target_path)
    if os.path.isfile(temp_output_path):
        if os.path.isfile(output_path):
            os.remove(output_path)
        shutil.move(temp_output_path, output_path)


def clean_temp(target_path: str) -> None:
    temp_directory_path = get_temp_directory_path(target_path)
    parent_directory_path = os.path.dirname(temp_directory_path)
    if not roop.globals.keep_frames and os.path.isdir(temp_directory_path):
        shutil.rmtree(temp_directory_path)
    if os.path.exists(parent_directory_path) and not os.listdir(parent_directory_path):
        os.rmdir(parent_directory_path)


def delete_temp_frames(filename: str) -> None:
    dir = os.path.dirname(os.path.dirname(filename))
    shutil.rmtree(dir)


def has_image_extension(image_path: str) -> bool:
    return image_path.lower().endswith(("png", "jpg", "jpeg", "webp"))


def has_extension(filepath: str, extensions: List[str]) -> bool:
    return filepath.lower().endswith(tuple(extensions))


def is_image(image_path: str) -> bool:
    if image_path and os.path.isfile(image_path):
        if image_path.endswith(".webp"):
            return True
        mimetype, _ = mimetypes.guess_type(image_path)
        return bool(mimetype and mimetype.startswith("image/"))
    return False


def is_video(video_path: str) -> bool:
    if video_path and os.path.isfile(video_path):
        mimetype, _ = mimetypes.guess_type(video_path)
        return bool(mimetype and mimetype.startswith("video/"))
    return False


def conditional_download(download_directory_path: str, urls: List[str]) -> None:
    if not os.path.exists(download_directory_path):
        os.makedirs(download_directory_path)
    for url in urls:
        download_file_path = os.path.join(
            download_directory_path, os.path.basename(url)
        )
        if not os.path.exists(download_file_path):
            request = urllib.request.urlopen(url)  # type: ignore[attr-defined]
            total = int(request.headers.get("Content-Length", 0))
            with tqdm(
                total=total,
                desc=f"Downloading {url}",
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            ) as progress:
                urllib.request.urlretrieve(url, download_file_path, reporthook=lambda count, block_size, total_size: progress.update(block_size))  # type: ignore[attr-defined]


def get_local_files_from_folder(folder: str) -> List[str]:
    if not os.path.exists(folder) or not os.path.isdir(folder):
        return None
    files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f))
    ]
    return files


def resolve_relative_path(path: str) -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))


def get_device() -> str:
    if len(roop.globals.execution_providers) < 1:
        roop.globals.execution_providers = ["CPUExecutionProvider"]

    prov = roop.globals.execution_providers[0]
    if "CoreMLExecutionProvider" in prov:
        return "mps"
    if "CUDAExecutionProvider" in prov or "ROCMExecutionProvider" in prov:
        return "cuda"
    if "OpenVINOExecutionProvider" in prov:
        return "mkl"
    return "cpu"


def str_to_class(module_name, class_name) -> Any:
    from importlib import import_module

    class_ = None
    try:
        module_ = import_module(module_name)
        try:
            class_ = getattr(module_, class_name)()
        except AttributeError:
            print(f"Class {class_name} does not exist")
    except ImportError:
        print(f"Module {module_name} does not exist")
    return class_

def is_installed(name:str) -> bool:
    return shutil.which(name);

# Taken from https://stackoverflow.com/a/68842705
def get_platform() -> str:
    if sys.platform == "linux":
        try:
            proc_version = open("/proc/version").read()
            if "Microsoft" in proc_version:
                return "wsl"
        except:
            pass
    return sys.platform

def open_with_default_app(filename:str):
    if filename == None:
        return
    platform = get_platform()
    if platform == "darwin":
        subprocess.call(("open", filename))
    elif platform in ["win64", "win32"]:        os.startfile(filename.replace("/", "\\"))
    elif platform == "wsl":
        subprocess.call("cmd.exe /C start".split() + [filename])
    else:  # linux variants
        subprocess.call("xdg-open", filename)


def prepare_for_batch(target_files) -> str:
    print("Preparing temp files")
    tempfolder = os.path.join(tempfile.gettempdir(), "rooptmp")
    if os.path.exists(tempfolder):
        shutil.rmtree(tempfolder)
    Path(tempfolder).mkdir(parents=True, exist_ok=True)
    for f in target_files:
        newname = os.path.basename(f.name)
        shutil.move(f.name, os.path.join(tempfolder, newname))
    return tempfolder


def zip(files, zipname):
    with zipfile.ZipFile(zipname, "w") as zip_file:
        for f in files:
            zip_file.write(f, os.path.basename(f))


def unzip(zipfilename: str, target_path: str):
    with zipfile.ZipFile(zipfilename, "r") as zip_file:
        zip_file.extractall(target_path)


def mkdir_with_umask(directory):
    oldmask = os.umask(0)
    # mode needs octal
    os.makedirs(directory, mode=0o775, exist_ok=True)
    os.umask(oldmask)


def open_folder(path: str):
    platform = get_platform()
    try:
        if platform == "darwin":
            subprocess.call(("open", path))
        elif platform in ["win64", "win32"]:
            open_with_default_app(path)
        elif platform == "wsl":
            subprocess.call("cmd.exe /C start".split() + [path])
        else:  # linux variants
            subprocess.Popen(["xdg-open", path])
    except Exception as e:
        traceback.print_exc()
        pass
        # import webbrowser
        # webbrowser.open(url)


def create_version_html() -> str:
    python_version = ".".join([str(x) for x in sys.version_info[0:3]])
    versions_html = f"""
python: <span title="{sys.version}">{python_version}</span>
•
torch: {getattr(torch, '__long_version__',torch.__version__)}
•
gradio: {gradio.__version__}
"""
    return versions_html


def compute_cosine_distance(emb1, emb2) -> float:
    return distance.cosine(emb1, emb2)

def has_cuda_device():
    return torch.cuda is not None and torch.cuda.is_available()


def print_cuda_info():
    try:
        print(f'Number of CUDA devices: {torch.cuda.device_count()} Currently used Id: {torch.cuda.current_device()} Device Name: {torch.cuda.get_device_name(torch.cuda.current_device())}')
    except:
       print('No CUDA device found!')

def clean_dir(path: str):
    contents = os.listdir(path)
    for item in contents:
        item_path = os.path.join(path, item)
        try:
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except Exception as e:
            print(e)
            

def conditional_thread_semaphore() -> Union[Any, Any]:
    if 'DmlExecutionProvider' in roop.globals.execution_providers or 'ROCMExecutionProvider' in roop.globals.execution_providers:
        return THREAD_SEMAPHORE
    return NULL_CONTEXT

```

# roop\typing.py

```py
from typing import Any

from insightface.app.common import Face
from roop.FaceSet import FaceSet
import numpy

Face = Face
FaceSet = FaceSet
Frame = numpy.ndarray[Any, Any]

```

# roop\template_parser.py

```py
import re
from datetime import datetime

template_functions = {
    "timestamp": lambda data: str(int(datetime.now().timestamp())),
    "i": lambda data: data.get("index", False),
    "file": lambda data: data.get("file", False),
    "date": lambda data: datetime.now().strftime("%Y-%m-%d"),
    "time": lambda data: datetime.now().strftime("%H-%M-%S"),
}


def parse(text: str, data: dict):
    pattern = r"\{([^}]+)\}"

    matches = re.findall(pattern, text)

    for match in matches:
        replacement = template_functions[match](data)
        if replacement is not False:
            text = text.replace(f"{{{match}}}", replacement)

    return text

```

# roop\StreamWriter.py

```py
import threading
import time
import pyvirtualcam


class StreamWriter():
    FPS = 30
    VCam = None
    Active = False
    THREAD_LOCK_STREAM = threading.Lock()
    time_last_process = None
    timespan_min = 0.0
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.Close()

    def __init__(self, size, fps):
        self.time_last_process = time.perf_counter()
        self.FPS = fps
        self.timespan_min = 1.0 / fps
        print('Detecting virtual cam devices')
        self.VCam = pyvirtualcam.Camera(width=size[0], height=size[1], fps=fps, fmt=pyvirtualcam.PixelFormat.BGR, print_fps=False)
        if self.VCam is None:
             print("No virtual camera found!")
             return
        print(f'Using virtual camera: {self.VCam.device}')
        print(f'Using {self.VCam.native_fmt}')
        self.Active = True
         

    def LimitFrames(self):
        while True:
            current_time = time.perf_counter()
            time_passed = current_time - self.time_last_process
            if time_passed >= self.timespan_min:
                break

    # First version used a queue and threading. Surprisingly this
    # totally simple, blocking version is 10 times faster!
    def WriteToStream(self, frame):
        if self.VCam is None:
             return
        with self.THREAD_LOCK_STREAM:
            self.LimitFrames()
            self.VCam.send(frame)
            self.time_last_process = time.perf_counter()
             

    def Close(self):
        self.Active = False
        if self.VCam is None:
            self.VCam.close()
            self.VCam = None





```

# roop\ProcessOptions.py

```py
class ProcessOptions:

    def __init__(self, processordefines:dict, face_distance,  blend_ratio, swap_mode, selected_index, masking_text, imagemask, num_steps, subsample_size, show_face_area, restore_original_mouth, show_mask=False):
        self.processors = processordefines
        self.face_distance_threshold = face_distance
        self.blend_ratio = blend_ratio
        self.swap_mode = swap_mode
        self.selected_index = selected_index
        self.masking_text = masking_text
        self.imagemask = imagemask
        self.num_swap_steps = num_steps
        self.show_face_area_overlay = show_face_area
        self.show_face_masking = show_mask
        self.subsample_size = subsample_size
        self.restore_original_mouth = restore_original_mouth
        self.max_num_reuse_frame = 15
```

# roop\ProcessMgr.py

```py
import os
import cv2 
import numpy as np
import psutil

from roop.ProcessOptions import ProcessOptions

from roop.face_util import get_first_face, get_all_faces, rotate_anticlockwise, rotate_clockwise, clamp_cut_values
from roop.utilities import compute_cosine_distance, get_device, str_to_class
import roop.vr_util as vr

from typing import Any, List, Callable
from roop.typing import Frame, Face
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Thread, Lock
from queue import Queue
from tqdm import tqdm
from roop.ffmpeg_writer import FFMPEG_VideoWriter
from roop.StreamWriter import StreamWriter
import roop.globals



# Poor man's enum to be able to compare to int
class eNoFaceAction():
    USE_ORIGINAL_FRAME = 0
    RETRY_ROTATED = 1
    SKIP_FRAME = 2
    SKIP_FRAME_IF_DISSIMILAR = 3,
    USE_LAST_SWAPPED = 4



def create_queue(temp_frame_paths: List[str]) -> Queue[str]:
    queue: Queue[str] = Queue()
    for frame_path in temp_frame_paths:
        queue.put(frame_path)
    return queue


def pick_queue(queue: Queue[str], queue_per_future: int) -> List[str]:
    queues = []
    for _ in range(queue_per_future):
        if not queue.empty():
            queues.append(queue.get())
    return queues



class ProcessMgr():
    input_face_datas = []
    target_face_datas = []

    imagemask = None

    processors = []
    options : ProcessOptions = None
    
    num_threads = 1
    current_index = 0
    processing_threads = 1
    buffer_wait_time = 0.1

    lock = Lock()

    frames_queue = None
    processed_queue = None

    videowriter= None
    streamwriter = None

    progress_gradio = None
    total_frames = 0

    num_frames_no_face = 0
    last_swapped_frame = None

    output_to_file = None
    output_to_cam = None


    plugins =  { 
    'faceswap'          : 'FaceSwapInsightFace',
    'mask_clip2seg'     : 'Mask_Clip2Seg',
    'mask_xseg'         : 'Mask_XSeg',
    'codeformer'        : 'Enhance_CodeFormer',
    'gfpgan'            : 'Enhance_GFPGAN',
    'dmdnet'            : 'Enhance_DMDNet',
    'gpen'              : 'Enhance_GPEN',
    'restoreformer++'   : 'Enhance_RestoreFormerPPlus',
    'colorizer'         : 'Frame_Colorizer',
    'filter_generic'    : 'Frame_Filter',
    'removebg'          : 'Frame_Masking',
    'upscale'           : 'Frame_Upscale'
    }

    def __init__(self, progress):
        if progress is not None:
            self.progress_gradio = progress

    def reuseOldProcessor(self, name:str):
        for p in self.processors:
            if p.processorname == name:
                return p
            
        return None


    def initialize(self, input_faces, target_faces, options):
        self.input_face_datas = input_faces
        self.target_face_datas = target_faces
        self.num_frames_no_face = 0
        self.last_swapped_frame = None
        self.options = options
        devicename = get_device()

        roop.globals.g_desired_face_analysis=["landmark_3d_68", "landmark_2d_106","detection","recognition"]
        if options.swap_mode == "all_female" or options.swap_mode == "all_male":
            roop.globals.g_desired_face_analysis.append("genderage")

        for p in self.processors:
            newp = next((x for x in options.processors.keys() if x == p.processorname), None)
            if newp is None:
                p.Release()
                del p

        newprocessors = []
        for key, extoption in options.processors.items():
            p = self.reuseOldProcessor(key)
            if p is None:
                classname = self.plugins[key]
                module = 'roop.processors.' + classname
                p = str_to_class(module, classname)
            if p is not None:
                extoption.update({"devicename": devicename})
                p.Initialize(extoption)
                newprocessors.append(p)
            else:
                print(f"Not using {module}")
        self.processors = newprocessors



        if isinstance(self.options.imagemask, dict) and self.options.imagemask.get("layers") and len(self.options.imagemask["layers"]) > 0:
            self.options.imagemask  = self.options.imagemask.get("layers")[0]
            # Get rid of alpha
            self.options.imagemask = cv2.cvtColor(self.options.imagemask, cv2.COLOR_RGBA2GRAY)
            if np.any(self.options.imagemask):
                mo = self.input_face_datas[0].faces[0].mask_offsets
                self.options.imagemask = self.blur_area(self.options.imagemask, mo[4], mo[5])
                self.options.imagemask = self.options.imagemask.astype(np.float32) / 255
                self.options.imagemask = cv2.cvtColor(self.options.imagemask, cv2.COLOR_GRAY2RGB)
            else:
                self.options.imagemask = None

        self.options.frame_processing = False
        for p in self.processors:
            if p.type.startswith("frame_"):
                self.options.frame_processing = True

            
 



    def run_batch(self, source_files, target_files, threads:int = 1):
        progress_bar_format = '{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]'
        self.total_frames = len(source_files)
        self.num_threads = threads
        with tqdm(total=self.total_frames, desc='Processing', unit='frame', dynamic_ncols=True, bar_format=progress_bar_format) as progress:
            with ThreadPoolExecutor(max_workers=threads) as executor:
                futures = []
                queue = create_queue(source_files)
                queue_per_future = max(len(source_files) // threads, 1)
                while not queue.empty():
                    future = executor.submit(self.process_frames, source_files, target_files, pick_queue(queue, queue_per_future), lambda: self.update_progress(progress))
                    futures.append(future)
                for future in as_completed(futures):
                    future.result()


    def process_frames(self, source_files: List[str], target_files: List[str], current_files, update: Callable[[], None]) -> None:
        for f in current_files:
            if not roop.globals.processing:
                return
            
            # Decode the byte array into an OpenCV image
            temp_frame = cv2.imdecode(np.fromfile(f, dtype=np.uint8), cv2.IMREAD_COLOR)
            if temp_frame is not None:
                if self.options.frame_processing:
                    for p in self.processors:
                        frame = p.Run(temp_frame)
                    resimg = frame
                else:
                    resimg = self.process_frame(temp_frame)
                if resimg is not None:
                    i = source_files.index(f)
                    # Also let numpy write the file to support utf-8/16 filenames
                    cv2.imencode(f'.{roop.globals.CFG.output_image_format}',resimg)[1].tofile(target_files[i])
            if update:
                update()



    def read_frames_thread(self, cap, frame_start, frame_end, num_threads):
        num_frame = 0
        total_num = frame_end - frame_start
        if frame_start > 0:
            cap.set(cv2.CAP_PROP_POS_FRAMES,frame_start)

        while True and roop.globals.processing:
            ret, frame = cap.read()
            if not ret:
                break
                
            self.frames_queue[num_frame % num_threads].put(frame, block=True)
            num_frame += 1
            if num_frame == total_num:
                break

        for i in range(num_threads):
            self.frames_queue[i].put(None)



    def process_videoframes(self, threadindex, progress) -> None:
        while True:
            frame = self.frames_queue[threadindex].get()
            if frame is None:
                self.processing_threads -= 1
                self.processed_queue[threadindex].put((False, None))
                return
            else:
                if self.options.frame_processing:
                    for p in self.processors:
                        frame = p.Run(frame)
                    resimg = frame
                else:                            
                    resimg = self.process_frame(frame)
                self.processed_queue[threadindex].put((True, resimg))
                del frame
                progress()


    def write_frames_thread(self):
        nextindex = 0
        num_producers = self.num_threads
        
        while True:
            process, frame = self.processed_queue[nextindex % self.num_threads].get()
            nextindex += 1
            if frame is not None:
                if self.output_to_file:
                    self.videowriter.write_frame(frame)
                if self.output_to_cam:
                    self.streamwriter.WriteToStream(frame)
                del frame
            elif process == False:
                num_producers -= 1
                if num_producers < 1:
                    return
            


    def run_batch_inmem(self, output_method, source_video, target_video, frame_start, frame_end, fps, threads:int = 1):
        if len(self.processors) < 1:
            print("No processor defined!")
            return

        cap = cv2.VideoCapture(source_video)
        # frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_count = (frame_end - frame_start) + 1
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        processed_resolution = None
        for p in self.processors:
            if hasattr(p, 'getProcessedResolution'):
                processed_resolution = p.getProcessedResolution(width, height)
                print(f"Processed resolution: {processed_resolution}")
        if processed_resolution is not None:
            width = processed_resolution[0]
            height = processed_resolution[1]


        self.total_frames = frame_count
        self.num_threads = threads

        self.processing_threads = self.num_threads
        self.frames_queue = []
        self.processed_queue = []
        for _ in range(threads):
            self.frames_queue.append(Queue(1))
            self.processed_queue.append(Queue(1))

        self.output_to_file = output_method != "Virtual Camera"
        self.output_to_cam = output_method == "Virtual Camera" or output_method == "Both"

        if self.output_to_file:
            self.videowriter = FFMPEG_VideoWriter(target_video, (width, height), fps, codec=roop.globals.video_encoder, crf=roop.globals.video_quality, audiofile=None)
        if self.output_to_cam:
            self.streamwriter = StreamWriter((width, height), int(fps))

        readthread = Thread(target=self.read_frames_thread, args=(cap, frame_start, frame_end, threads))
        readthread.start()

        writethread = Thread(target=self.write_frames_thread)
        writethread.start()

        progress_bar_format = '{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]'
        with tqdm(total=self.total_frames, desc='Processing', unit='frames', dynamic_ncols=True, bar_format=progress_bar_format) as progress:
            with ThreadPoolExecutor(thread_name_prefix='swap_proc', max_workers=self.num_threads) as executor:
                futures = []
                
                for threadindex in range(threads):
                    future = executor.submit(self.process_videoframes, threadindex, lambda: self.update_progress(progress))
                    futures.append(future)
                
                for future in as_completed(futures):
                    future.result()
        # wait for the task to complete
        readthread.join()
        writethread.join()
        cap.release()
        if self.output_to_file:
            self.videowriter.close()
        if self.output_to_cam:
            self.streamwriter.Close()

        self.frames_queue.clear()
        self.processed_queue.clear()




    def update_progress(self, progress: Any = None) -> None:
        process = psutil.Process(os.getpid())
        memory_usage = process.memory_info().rss / 1024 / 1024 / 1024
        progress.set_postfix({
            'memory_usage': '{:.2f}'.format(memory_usage).zfill(5) + 'GB',
            'execution_threads': self.num_threads
        })
        progress.update(1)
        if self.progress_gradio is not None:
            self.progress_gradio((progress.n, self.total_frames), desc='Processing', total=self.total_frames, unit='frames')



    def process_frame(self, frame:Frame):
        if len(self.input_face_datas) < 1 and not self.options.show_face_masking:
            return frame
        temp_frame = frame.copy()
        num_swapped, temp_frame = self.swap_faces(frame, temp_frame)
        if num_swapped > 0:
            if roop.globals.no_face_action == eNoFaceAction.SKIP_FRAME_IF_DISSIMILAR:
                if len(self.input_face_datas) > num_swapped:
                    return None
            self.num_frames_no_face = 0
            self.last_swapped_frame = temp_frame.copy()
            return temp_frame
        if roop.globals.no_face_action == eNoFaceAction.USE_LAST_SWAPPED:
            if self.last_swapped_frame is not None and self.num_frames_no_face < self.options.max_num_reuse_frame:
                self.num_frames_no_face += 1
                return self.last_swapped_frame.copy()
            return frame

        elif roop.globals.no_face_action == eNoFaceAction.USE_ORIGINAL_FRAME:
            return frame
        if roop.globals.no_face_action == eNoFaceAction.SKIP_FRAME:
            #This only works with in-mem processing, as it simply skips the frame.
            #For 'extract frames' it simply leaves the unprocessed frame unprocessed and it gets used in the final output by ffmpeg.
            #If we could delete that frame here, that'd work but that might cause ffmpeg to fail unless the frames are renamed, and I don't think we have the info on what frame it actually is?????
            #alternatively, it could mark all the necessary frames for deletion, delete them at the end, then rename the remaining frames that might work?
            return None
        else:
            return self.retry_rotated(frame)

    def retry_rotated(self, frame):
        copyframe = frame.copy()
        copyframe = rotate_clockwise(copyframe)
        temp_frame = copyframe.copy()
        num_swapped, temp_frame = self.swap_faces(copyframe, temp_frame)
        if num_swapped > 0:
            return rotate_anticlockwise(temp_frame)
        
        copyframe = frame.copy()
        copyframe = rotate_anticlockwise(copyframe)
        temp_frame = copyframe.copy()
        num_swapped, temp_frame = self.swap_faces(copyframe, temp_frame)
        if num_swapped > 0:
            return rotate_clockwise(temp_frame)
        del copyframe
        return frame
        


    def swap_faces(self, frame, temp_frame):
        num_faces_found = 0

        if self.options.swap_mode == "first":
            face = get_first_face(frame)

            if face is None:
                return num_faces_found, frame
            
            num_faces_found += 1
            temp_frame = self.process_face(self.options.selected_index, face, temp_frame)
            del face

        else:
            faces = get_all_faces(frame)
            if faces is None:
                return num_faces_found, frame
            
            if self.options.swap_mode == "all":
                for face in faces:
                    num_faces_found += 1
                    temp_frame = self.process_face(self.options.selected_index, face, temp_frame)

            elif self.options.swap_mode == "all_input":
                for i,face in enumerate(faces):
                    num_faces_found += 1
                    if i < len(self.input_face_datas):
                        temp_frame = self.process_face(i, face, temp_frame)
                    else:
                        break
            
            elif self.options.swap_mode == "selected":
                num_targetfaces = len(self.target_face_datas) 
                use_index = num_targetfaces == 1
                for i,tf in enumerate(self.target_face_datas):
                    for face in faces:
                        if compute_cosine_distance(tf.embedding, face.embedding) <= self.options.face_distance_threshold:
                            if i < len(self.input_face_datas):
                                if use_index:
                                    temp_frame = self.process_face(self.options.selected_index, face, temp_frame)
                                else:
                                    temp_frame = self.process_face(i, face, temp_frame)
                                num_faces_found += 1
                            if not roop.globals.vr_mode and num_faces_found == num_targetfaces:
                                break
            elif self.options.swap_mode == "all_female" or self.options.swap_mode == "all_male":
                gender = 'F' if self.options.swap_mode == "all_female" else 'M'
                for face in faces:
                    if face.sex == gender:
                        num_faces_found += 1
                        temp_frame = self.process_face(self.options.selected_index, face, temp_frame)
            
            # might be slower but way more clean to release everything here
            for face in faces:
                del face
            faces.clear()



        if roop.globals.vr_mode and num_faces_found % 2 > 0:
            # stereo image, there has to be an even number of faces
            num_faces_found = 0
            return num_faces_found, frame
        if num_faces_found == 0:
            return num_faces_found, frame

        #maskprocessor = next((x for x in self.processors if x.type == 'mask'), None)

        if self.options.imagemask is not None and self.options.imagemask.shape == frame.shape:
            temp_frame = self.simple_blend_with_mask(temp_frame, frame, self.options.imagemask)
        return num_faces_found, temp_frame


    def rotation_action(self, original_face:Face, frame:Frame):
        (height, width) = frame.shape[:2]

        bounding_box_width = original_face.bbox[2] - original_face.bbox[0]
        bounding_box_height = original_face.bbox[3] - original_face.bbox[1]
        horizontal_face = bounding_box_width > bounding_box_height

        center_x = width // 2.0
        start_x = original_face.bbox[0]
        end_x = original_face.bbox[2]
        bbox_center_x = start_x + (bounding_box_width // 2.0)

        # need to leverage the array of landmarks as decribed here:
        # https://github.com/deepinsight/insightface/tree/master/alignment/coordinate_reg
        # basically, we should be able to check for the relative position of eyes and nose
        # then use that to determine which way the face is actually facing when in a horizontal position
        # and use that to determine the correct rotation_action

        forehead_x = original_face.landmark_2d_106[72][0]
        chin_x = original_face.landmark_2d_106[0][0]

        if horizontal_face:
            if chin_x < forehead_x:
                # this is someone lying down with their face like this (:
                return "rotate_anticlockwise"
            elif forehead_x < chin_x:
                # this is someone lying down with their face like this :)
                return "rotate_clockwise"
            if bbox_center_x >= center_x:
                # this is someone lying down with their face in the right hand side of the frame
                return "rotate_anticlockwise"
            if bbox_center_x < center_x:
                # this is someone lying down with their face in the left hand side of the frame
                return "rotate_clockwise"

        return None


    def auto_rotate_frame(self, original_face, frame:Frame):
        target_face = original_face
        original_frame = frame

        rotation_action = self.rotation_action(original_face, frame)

        if rotation_action == "rotate_anticlockwise":
            #face is horizontal, rotating frame anti-clockwise and getting face bounding box from rotated frame
            frame = rotate_anticlockwise(frame)
        elif rotation_action == "rotate_clockwise":
            #face is horizontal, rotating frame clockwise and getting face bounding box from rotated frame
            frame = rotate_clockwise(frame)

        return target_face, frame, rotation_action
    

    def auto_unrotate_frame(self, frame:Frame, rotation_action):
        if rotation_action == "rotate_anticlockwise":
            return rotate_clockwise(frame)
        elif rotation_action == "rotate_clockwise":
            return rotate_anticlockwise(frame)
        
        return frame



    def process_face(self,face_index, target_face:Face, frame:Frame):
        from roop.face_util import align_crop

        enhanced_frame = None
        if(len(self.input_face_datas) > 0):
            inputface = self.input_face_datas[face_index].faces[0]
        else:
            inputface = None

        rotation_action = None
        if roop.globals.autorotate_faces:
            # check for sideways rotation of face
            rotation_action = self.rotation_action(target_face, frame)
            if rotation_action is not None:
                (startX, startY, endX, endY) = target_face["bbox"].astype("int")
                width = endX - startX
                height = endY - startY
                offs = int(max(width,height) * 0.25)
                rotcutframe,startX, startY, endX, endY = self.cutout(frame, startX - offs, startY - offs, endX + offs, endY + offs)
                if rotation_action == "rotate_anticlockwise":
                    rotcutframe = rotate_anticlockwise(rotcutframe)
                elif rotation_action == "rotate_clockwise":
                    rotcutframe = rotate_clockwise(rotcutframe)
                # rotate image and re-detect face to correct wonky landmarks
                rotface = get_first_face(rotcutframe)
                if rotface is None:
                    rotation_action = None
                else:
                    saved_frame = frame.copy()
                    frame = rotcutframe
                    target_face = rotface



        # if roop.globals.vr_mode:
            # bbox = target_face.bbox
            # [orig_width, orig_height, _] = frame.shape

            # # Convert bounding box to ints
            # x1, y1, x2, y2 = map(int, bbox)

            # # Determine the center of the bounding box
            # x_center = (x1 + x2) / 2
            # y_center = (y1 + y2) / 2

            # # Normalize coordinates to range [-1, 1]
            # x_center_normalized = x_center / (orig_width / 2) - 1
            # y_center_normalized = y_center / (orig_width / 2) - 1

            # # Convert normalized coordinates to spherical (theta, phi)
            # theta = x_center_normalized * 180  # Theta ranges from -180 to 180 degrees
            # phi = -y_center_normalized * 90  # Phi ranges from -90 to 90 degrees

            # img = vr.GetPerspective(frame, 90, theta, phi, 1280, 1280)  # Generate perspective image


        """ Code ported/adapted from Facefusion which borrowed the idea from Rope:
            Kind of subsampling the cutout and aligned face image and faceswapping slices of it up to
            the desired output resolution. This works around the current resolution limitations without using enhancers.
        """
        model_output_size = 128
        subsample_size = self.options.subsample_size
        subsample_total = subsample_size // model_output_size
        aligned_img, M = align_crop(frame, target_face.kps, subsample_size)

        fake_frame = aligned_img
        target_face.matrix = M

        for p in self.processors:
            if p.type == 'swap':
                swap_result_frames = []
                subsample_frames = self.implode_pixel_boost(aligned_img, model_output_size, subsample_total)
                for sliced_frame in subsample_frames:
                    for _ in range(0,self.options.num_swap_steps):
                        sliced_frame = self.prepare_crop_frame(sliced_frame)
                        sliced_frame = p.Run(inputface, target_face, sliced_frame)
                        sliced_frame = self.normalize_swap_frame(sliced_frame)
                    swap_result_frames.append(sliced_frame)
                fake_frame = self.explode_pixel_boost(swap_result_frames, model_output_size, subsample_total, subsample_size)
                fake_frame = fake_frame.astype(np.uint8)
                scale_factor = 0.0
            elif p.type == 'mask':
                fake_frame = self.process_mask(p, aligned_img, fake_frame)
            else:
                enhanced_frame, scale_factor = p.Run(self.input_face_datas[face_index], target_face, fake_frame)

        upscale = 512
        orig_width = fake_frame.shape[1]
        if orig_width != upscale:
            fake_frame = cv2.resize(fake_frame, (upscale, upscale), cv2.INTER_CUBIC)
        mask_offsets = (0,0,0,0,1,20) if inputface is None else inputface.mask_offsets

        
        if enhanced_frame is None:
            scale_factor = int(upscale / orig_width)
            result = self.paste_upscale(fake_frame, fake_frame, target_face.matrix, frame, scale_factor, mask_offsets)
        else:
            result = self.paste_upscale(fake_frame, enhanced_frame, target_face.matrix, frame, scale_factor, mask_offsets)

        # Restore mouth before unrotating
        if self.options.restore_original_mouth:
            mouth_cutout, mouth_bb = self.create_mouth_mask(target_face, frame)
            result = self.apply_mouth_area(result, mouth_cutout, mouth_bb)

        if rotation_action is not None:
            fake_frame = self.auto_unrotate_frame(result, rotation_action)
            result = self.paste_simple(fake_frame, saved_frame, startX, startY)
        
        return result

        


    def cutout(self, frame:Frame, start_x, start_y, end_x, end_y):
        if start_x < 0:
            start_x = 0
        if start_y < 0:
            start_y = 0
        if end_x > frame.shape[1]:
            end_x = frame.shape[1]
        if end_y > frame.shape[0]:
            end_y = frame.shape[0]
        return frame[start_y:end_y, start_x:end_x], start_x, start_y, end_x, end_y

    def paste_simple(self, src:Frame, dest:Frame, start_x, start_y):
        end_x = start_x + src.shape[1]
        end_y = start_y + src.shape[0]

        start_x, end_x, start_y, end_y = clamp_cut_values(start_x, end_x, start_y, end_y, dest)
        dest[start_y:end_y, start_x:end_x] = src
        return dest
        
    def simple_blend_with_mask(self, image1, image2, mask):
        # Blend the images
        blended_image = image1.astype(np.float32) * (1.0 - mask) + image2.astype(np.float32) * mask
        return blended_image.astype(np.uint8)


    def paste_upscale(self, fake_face, upsk_face, M, target_img, scale_factor, mask_offsets):
        M_scale = M * scale_factor
        IM = cv2.invertAffineTransform(M_scale)

        face_matte = np.full((target_img.shape[0],target_img.shape[1]), 255, dtype=np.uint8)
        # Generate white square sized as a upsk_face
        img_matte = np.zeros((upsk_face.shape[0],upsk_face.shape[1]), dtype=np.uint8)

        w = img_matte.shape[1]
        h = img_matte.shape[0]

        top = int(mask_offsets[0] * h)
        bottom = int(h - (mask_offsets[1] * h))
        left = int(mask_offsets[2] * w)
        right = int(w - (mask_offsets[3] * w))
        img_matte[top:bottom,left:right] = 255

        # Transform white square back to target_img
        img_matte = cv2.warpAffine(img_matte, IM, (target_img.shape[1], target_img.shape[0]), flags=cv2.INTER_NEAREST, borderValue=0.0) 
        ##Blacken the edges of face_matte by 1 pixels (so the mask in not expanded on the image edges)
        img_matte[:1,:] = img_matte[-1:,:] = img_matte[:,:1] = img_matte[:,-1:] = 0

        img_matte = self.blur_area(img_matte, mask_offsets[4], mask_offsets[5])
        #Normalize images to float values and reshape
        img_matte = img_matte.astype(np.float32)/255
        face_matte = face_matte.astype(np.float32)/255
        img_matte = np.minimum(face_matte, img_matte)
        if self.options.show_face_area_overlay:
            # Additional steps for green overlay
            green_overlay = np.zeros_like(target_img)
            green_color = [0, 255, 0]  # RGB for green
            for i in range(3):  # Apply green color where img_matte is not zero
                green_overlay[:, :, i] = np.where(img_matte > 0, green_color[i], 0)        ##Transform upcaled face back to target_img
        img_matte = np.reshape(img_matte, [img_matte.shape[0],img_matte.shape[1],1]) 
        paste_face = cv2.warpAffine(upsk_face, IM, (target_img.shape[1], target_img.shape[0]), borderMode=cv2.BORDER_REPLICATE)
        if upsk_face is not fake_face:
            fake_face = cv2.warpAffine(fake_face, IM, (target_img.shape[1], target_img.shape[0]), borderMode=cv2.BORDER_REPLICATE)
            paste_face = cv2.addWeighted(paste_face, self.options.blend_ratio, fake_face, 1.0 - self.options.blend_ratio, 0)

        # Re-assemble image
        paste_face = img_matte * paste_face
        paste_face = paste_face + (1-img_matte) * target_img.astype(np.float32)
        if self.options.show_face_area_overlay:
            # Overlay the green overlay on the final image
            paste_face = cv2.addWeighted(paste_face.astype(np.uint8), 1 - 0.5, green_overlay, 0.5, 0)
        return paste_face.astype(np.uint8)


    def blur_area(self, img_matte, num_erosion_iterations, blur_amount):
        # Detect the affine transformed white area
        mask_h_inds, mask_w_inds = np.where(img_matte==255) 
        # Calculate the size (and diagonal size) of transformed white area width and height boundaries
        mask_h = np.max(mask_h_inds) - np.min(mask_h_inds) 
        mask_w = np.max(mask_w_inds) - np.min(mask_w_inds)
        mask_size = int(np.sqrt(mask_h*mask_w))
        # Calculate the kernel size for eroding img_matte by kernel (insightface empirical guess for best size was max(mask_size//10,10))
        # k = max(mask_size//12, 8)
        k = max(mask_size//(blur_amount // 2) , blur_amount // 2)
        kernel = np.ones((k,k),np.uint8)
        img_matte = cv2.erode(img_matte,kernel,iterations = num_erosion_iterations)
        #Calculate the kernel size for blurring img_matte by blur_size (insightface empirical guess for best size was max(mask_size//20, 5))
        # k = max(mask_size//24, 4) 
        k = max(mask_size//blur_amount, blur_amount//5) 
        kernel_size = (k, k)
        blur_size = tuple(2*i+1 for i in kernel_size)
        return cv2.GaussianBlur(img_matte, blur_size, 0)


    def prepare_crop_frame(self, swap_frame):
        model_type = 'inswapper'
        model_mean = [0.0, 0.0, 0.0]
        model_standard_deviation = [1.0, 1.0, 1.0]

        if model_type == 'ghost':
            swap_frame = swap_frame[:, :, ::-1] / 127.5 - 1
        else:
            swap_frame = swap_frame[:, :, ::-1] / 255.0
        swap_frame = (swap_frame - model_mean) / model_standard_deviation
        swap_frame = swap_frame.transpose(2, 0, 1)
        swap_frame = np.expand_dims(swap_frame, axis = 0).astype(np.float32)
        return swap_frame


    def normalize_swap_frame(self, swap_frame):
        model_type = 'inswapper'
        swap_frame = swap_frame.transpose(1, 2, 0)

        if model_type == 'ghost':
            swap_frame = (swap_frame * 127.5 + 127.5).round()
        else:
            swap_frame = (swap_frame * 255.0).round()
        swap_frame = swap_frame[:, :, ::-1]
        return swap_frame

    def implode_pixel_boost(self, aligned_face_frame, model_size, pixel_boost_total : int):
        subsample_frame = aligned_face_frame.reshape(model_size, pixel_boost_total, model_size, pixel_boost_total, 3)
        subsample_frame = subsample_frame.transpose(1, 3, 0, 2, 4).reshape(pixel_boost_total ** 2, model_size, model_size, 3)
        return subsample_frame


    def explode_pixel_boost(self, subsample_frame, model_size, pixel_boost_total, pixel_boost_size):
        final_frame = np.stack(subsample_frame, axis = 0).reshape(pixel_boost_total, pixel_boost_total, model_size, model_size, 3)
        final_frame = final_frame.transpose(2, 0, 3, 1, 4).reshape(pixel_boost_size, pixel_boost_size, 3)
        return final_frame

    def process_mask(self, processor, frame:Frame, target:Frame):
        img_mask = processor.Run(frame, self.options.masking_text)
        img_mask = cv2.resize(img_mask, (target.shape[1], target.shape[0]))
        img_mask = np.reshape(img_mask, [img_mask.shape[0],img_mask.shape[1],1])

        if self.options.show_face_masking:
            result = (1 - img_mask) * frame.astype(np.float32)
            return np.uint8(result)


        target = target.astype(np.float32)
        result = (1-img_mask) * target
        result += img_mask * frame.astype(np.float32)
        return np.uint8(result)


    # Code for mouth restoration adapted from https://github.com/iVideoGameBoss/iRoopDeepFaceCam
    
    def create_mouth_mask(self, face: Face, frame: Frame):
        mouth_cutout = None
        
        landmarks = face.landmark_2d_106
        if landmarks is not None:
            # Get mouth landmarks (indices 52 to 71 typically represent the outer mouth)
            mouth_points = landmarks[52:71].astype(np.int32)
            
            # Add padding to mouth area
            min_x, min_y = np.min(mouth_points, axis=0)
            max_x, max_y = np.max(mouth_points, axis=0)
            min_x = max(0, min_x - (15*6))
            min_y = max(0, min_y - 22)
            max_x = min(frame.shape[1], max_x + (15*6))
            max_y = min(frame.shape[0], max_y + (90*6))
            
            # Extract the mouth area from the frame using the calculated bounding box
            mouth_cutout = frame[min_y:max_y, min_x:max_x].copy()

        return mouth_cutout, (min_x, min_y, max_x, max_y)



    def create_feathered_mask(self, shape, feather_amount=30):
        mask = np.zeros(shape[:2], dtype=np.float32)
        center = (shape[1] // 2, shape[0] // 2)
        cv2.ellipse(mask, center, (shape[1] // 2 - feather_amount, shape[0] // 2 - feather_amount), 
                    0, 0, 360, 1, -1)
        mask = cv2.GaussianBlur(mask, (feather_amount*2+1, feather_amount*2+1), 0)
        return mask / np.max(mask)

    def apply_mouth_area(self, frame: np.ndarray, mouth_cutout: np.ndarray, mouth_box: tuple) -> np.ndarray:
        min_x, min_y, max_x, max_y = mouth_box
        box_width = max_x - min_x
        box_height = max_y - min_y
        

        # Resize the mouth cutout to match the mouth box size
        if mouth_cutout is None or box_width is None or box_height is None:
            return frame
        try:
            resized_mouth_cutout = cv2.resize(mouth_cutout, (box_width, box_height))
            
            # Extract the region of interest (ROI) from the target frame
            roi = frame[min_y:max_y, min_x:max_x]
            
            # Ensure the ROI and resized_mouth_cutout have the same shape
            if roi.shape != resized_mouth_cutout.shape:
                resized_mouth_cutout = cv2.resize(resized_mouth_cutout, (roi.shape[1], roi.shape[0]))
            
            # Apply color transfer from ROI to mouth cutout
            color_corrected_mouth = self.apply_color_transfer(resized_mouth_cutout, roi)
            
            # Create a feathered mask with increased feather amount
            feather_amount = min(30, box_width // 15, box_height // 15)
            mask = self.create_feathered_mask(resized_mouth_cutout.shape, feather_amount)
            
            # Blend the color-corrected mouth cutout with the ROI using the feathered mask
            mask = mask[:,:,np.newaxis]  # Add channel dimension to mask
            blended = (color_corrected_mouth * mask + roi * (1 - mask)).astype(np.uint8)
            
            # Place the blended result back into the frame
            frame[min_y:max_y, min_x:max_x] = blended
        except Exception as e:
            print(f'Error {e}')
            pass

        return frame

    def apply_color_transfer(self, source, target):
        """
        Apply color transfer from target to source image
        """
        source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
        target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")

        source_mean, source_std = cv2.meanStdDev(source)
        target_mean, target_std = cv2.meanStdDev(target)

        # Reshape mean and std to be broadcastable
        source_mean = source_mean.reshape(1, 1, 3)
        source_std = source_std.reshape(1, 1, 3)
        target_mean = target_mean.reshape(1, 1, 3)
        target_std = target_std.reshape(1, 1, 3)

        # Perform the color transfer
        source = (source - source_mean) * (target_std / source_std) + target_mean
        return cv2.cvtColor(np.clip(source, 0, 255).astype("uint8"), cv2.COLOR_LAB2BGR)



    def unload_models():
        pass


    def release_resources(self):
        for p in self.processors:
            p.Release()
        self.processors.clear()
        if self.videowriter is not None:
            self.videowriter.close()
        if self.streamwriter is not None:
            self.streamwriter.Close()


```

# roop\ProcessEntry.py

```py
class ProcessEntry:
    def __init__(self, filename: str, start: int, end: int, fps: float):
        self.filename = filename
        self.finalname = None
        self.startframe = start
        self.endframe = end
        self.fps = fps
```

# roop\metadata.py

```py
name = 'roop unleashed'
version = '4.3.3'

```

# roop\globals.py

```py
from settings import Settings
from typing import List

source_path = None
target_path = None
output_path = None
target_folder_path = None
startup_args = None

cuda_device_id = 0
frame_processors: List[str] = []
keep_fps = None
keep_frames = None
autorotate_faces = None
vr_mode = None
skip_audio = None
wait_after_extraction = None
many_faces = None
use_batch = None
source_face_index = 0
target_face_index = 0
face_position = None
video_encoder = None
video_quality = None
max_memory = None
execution_providers: List[str] = []
execution_threads = None
headless = None
log_level = 'error'
selected_enhancer = None
subsample_size = 128
face_swap_mode = None
blend_ratio = 0.5
distance_threshold = 0.65
default_det_size = True

no_face_action = 0

processing = False

g_current_face_analysis = None
g_desired_face_analysis = None

FACE_ENHANCER = None

INPUT_FACESETS = []
TARGET_FACES = []


IMAGE_CHAIN_PROCESSOR = None
VIDEO_CHAIN_PROCESSOR = None
BATCH_IMAGE_CHAIN_PROCESSOR = None

CFG: Settings = None



```

# roop\ffmpeg_writer.py

```py
"""
FFMPEG_Writer - write set of frames to video file

original from
https://github.com/Zulko/moviepy/blob/master/moviepy/video/io/ffmpeg_writer.py

removed unnecessary dependencies

The MIT License (MIT)

Copyright (c) 2015 Zulko
Copyright (c) 2023 Janvarev Vladislav
"""

import os
import subprocess as sp

PIPE = -1
STDOUT = -2
DEVNULL = -3

FFMPEG_BINARY = "ffmpeg"

class FFMPEG_VideoWriter:
    """ A class for FFMPEG-based video writing.

    A class to write videos using ffmpeg. ffmpeg will write in a large
    choice of formats.

    Parameters
    -----------

    filename
      Any filename like 'video.mp4' etc. but if you want to avoid
      complications it is recommended to use the generic extension
      '.avi' for all your videos.

    size
      Size (width,height) of the output video in pixels.

    fps
      Frames per second in the output video file.

    codec
      FFMPEG codec. It seems that in terms of quality the hierarchy is
      'rawvideo' = 'png' > 'mpeg4' > 'libx264'
      'png' manages the same lossless quality as 'rawvideo' but yields
      smaller files. Type ``ffmpeg -codecs`` in a terminal to get a list
      of accepted codecs.

      Note for default 'libx264': by default the pixel format yuv420p
      is used. If the video dimensions are not both even (e.g. 720x405)
      another pixel format is used, and this can cause problem in some
      video readers.

    audiofile
      Optional: The name of an audio file that will be incorporated
      to the video.

    preset
      Sets the time that FFMPEG will take to compress the video. The slower,
      the better the compression rate. Possibilities are: ultrafast,superfast,
      veryfast, faster, fast, medium (default), slow, slower, veryslow,
      placebo.

    bitrate
      Only relevant for codecs which accept a bitrate. "5000k" offers
      nice results in general.

    """

    def __init__(self, filename, size, fps, codec="libx265", crf=14, audiofile=None,
                 preset="medium", bitrate=None,
                 logfile=None, threads=None, ffmpeg_params=None):

        if logfile is None:
            logfile = sp.PIPE

        self.filename = filename
        self.codec = codec
        self.ext = self.filename.split(".")[-1]
        w = size[0] - 1 if size[0] % 2 != 0 else size[0]
        h = size[1] - 1 if size[1] % 2 != 0 else size[1]


        # order is important
        cmd = [
            FFMPEG_BINARY,
            '-hide_banner',
            '-hwaccel', 'auto',
            '-y',
            '-loglevel', 'error' if logfile == sp.PIPE else 'info',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-s', '%dx%d' % (size[0], size[1]),
            #'-pix_fmt', 'rgba' if withmask else 'rgb24',
            '-pix_fmt', 'bgr24',
            '-r', str(fps),
            '-an', '-i', '-' 
        ]

        if audiofile is not None:
            cmd.extend([
                '-i', audiofile,
                '-acodec', 'copy'
            ])

        cmd.extend([
            '-vcodec', codec,
            '-crf', str(crf)
            #'-preset', preset,
        ])
        if ffmpeg_params is not None:
            cmd.extend(ffmpeg_params)
        if bitrate is not None:
            cmd.extend([
                '-b', bitrate
            ])

        # scale to a resolution divisible by 2 if not even
        cmd.extend(['-vf', f'scale={w}:{h}' if w != size[0] or h != size[1] else 'colorspace=bt709:iall=bt601-6-625:fast=1'])

        if threads is not None:
            cmd.extend(["-threads", str(threads)])

        cmd.extend([
            '-pix_fmt', 'yuv420p',

        ])
        cmd.extend([
            filename
        ])

        test = str(cmd)
        print(test)

        popen_params = {"stdout": DEVNULL,
                        "stderr": logfile,
                        "stdin": sp.PIPE}

        # This was added so that no extra unwanted window opens on windows
        # when the child process is created
        if os.name == "nt":
            popen_params["creationflags"] = 0x08000000  # CREATE_NO_WINDOW
        
        self.proc = sp.Popen(cmd, **popen_params)


    def write_frame(self, img_array):
        """ Writes one frame in the file."""
        try:
            #if PY3:
            self.proc.stdin.write(img_array.tobytes())
            # else:
            #    self.proc.stdin.write(img_array.tostring())
        except IOError as err:
            _, ffmpeg_error = self.proc.communicate()
            error = (str(err) + ("\n\nroop unleashed error: FFMPEG encountered "
                                 "the following error while writing file %s:"
                                 "\n\n %s" % (self.filename, str(ffmpeg_error))))

            if b"Unknown encoder" in ffmpeg_error:

                error = error+("\n\nThe video export "
                  "failed because FFMPEG didn't find the specified "
                  "codec for video encoding (%s). Please install "
                  "this codec or change the codec when calling "
                  "write_videofile. For instance:\n"
                  "  >>> clip.write_videofile('myvid.webm', codec='libvpx')")%(self.codec)

            elif b"incorrect codec parameters ?" in ffmpeg_error:

                 error = error+("\n\nThe video export "
                  "failed, possibly because the codec specified for "
                  "the video (%s) is not compatible with the given "
                  "extension (%s). Please specify a valid 'codec' "
                  "argument in write_videofile. This would be 'libx264' "
                  "or 'mpeg4' for mp4, 'libtheora' for ogv, 'libvpx for webm. "
                  "Another possible reason is that the audio codec was not "
                  "compatible with the video codec. For instance the video "
                  "extensions 'ogv' and 'webm' only allow 'libvorbis' (default) as a"
                  "video codec."
                  )%(self.codec, self.ext)

            elif  b"encoder setup failed" in ffmpeg_error:

                error = error+("\n\nThe video export "
                  "failed, possibly because the bitrate you specified "
                  "was too high or too low for the video codec.")

            elif b"Invalid encoder type" in ffmpeg_error:

                error = error + ("\n\nThe video export failed because the codec "
                  "or file extension you provided is not a video")


            raise IOError(error)

    def close(self):
        if self.proc:
            self.proc.stdin.close()
            if self.proc.stderr is not None:
                self.proc.stderr.close()
            self.proc.wait()

        self.proc = None

    # Support the Context Manager protocol, to ensure that resources are cleaned up.

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()



    

```

# roop\face_util.py

```py
import threading
from typing import Any
import insightface

import roop.globals
from roop.typing import Frame, Face

import cv2
import numpy as np
from skimage import transform as trans
from roop.capturer import get_video_frame
from roop.utilities import resolve_relative_path, conditional_thread_semaphore

FACE_ANALYSER = None
#THREAD_LOCK_ANALYSER = threading.Lock()
#THREAD_LOCK_SWAPPER = threading.Lock()
FACE_SWAPPER = None


def get_face_analyser() -> Any:
    global FACE_ANALYSER

    with conditional_thread_semaphore():
        if FACE_ANALYSER is None or roop.globals.g_current_face_analysis != roop.globals.g_desired_face_analysis:
            model_path = resolve_relative_path('..')
            # removed genderage
            allowed_modules = roop.globals.g_desired_face_analysis
            roop.globals.g_current_face_analysis = roop.globals.g_desired_face_analysis
            if roop.globals.CFG.force_cpu:
                print("Forcing CPU for Face Analysis")
                FACE_ANALYSER = insightface.app.FaceAnalysis(
                    name="buffalo_l",
                    root=model_path, providers=["CPUExecutionProvider"],allowed_modules=allowed_modules
                )
            else:
                FACE_ANALYSER = insightface.app.FaceAnalysis(
                    name="buffalo_l", root=model_path, providers=roop.globals.execution_providers,allowed_modules=allowed_modules
                )
            FACE_ANALYSER.prepare(
                ctx_id=0,
                det_size=(640, 640) if roop.globals.default_det_size else (320, 320),
            )
    return FACE_ANALYSER


def get_first_face(frame: Frame) -> Any:
    try:
        faces = get_face_analyser().get(frame)
        return min(faces, key=lambda x: x.bbox[0])
    #   return sorted(faces, reverse=True, key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]))[0]
    except:
        return None


def get_all_faces(frame: Frame) -> Any:
    try:
        faces = get_face_analyser().get(frame)
        return sorted(faces, key=lambda x: x.bbox[0])
    except:
        return None


def extract_face_images(source_filename, video_info, extra_padding=-1.0):
    face_data = []
    source_image = None

    if video_info[0]:
        frame = get_video_frame(source_filename, video_info[1])
        if frame is not None:
            source_image = frame
        else:
            return face_data
    else:
        source_image = cv2.imdecode(np.fromfile(source_filename, dtype=np.uint8), cv2.IMREAD_COLOR)

    faces = get_all_faces(source_image)
    if faces is None:
        return face_data

    i = 0
    for face in faces:
        (startX, startY, endX, endY) = face["bbox"].astype("int")
        startX, endX, startY, endY = clamp_cut_values(startX, endX, startY, endY, source_image)
        if extra_padding > 0.0:
            if source_image.shape[:2] == (512, 512):
                i += 1
                face_data.append([face, source_image])
                continue

            found = False
            for i in range(1, 3):
                (startX, startY, endX, endY) = face["bbox"].astype("int")
                startX, endX, startY, endY = clamp_cut_values(startX, endX, startY, endY, source_image)
                cutout_padding = extra_padding
                # top needs extra room for detection
                padding = int((endY - startY) * cutout_padding)
                oldY = startY
                startY -= padding

                factor = 0.25 if i == 1 else 0.5
                cutout_padding = factor
                padding = int((endY - oldY) * cutout_padding)
                endY += padding
                padding = int((endX - startX) * cutout_padding)
                startX -= padding
                endX += padding
                startX, endX, startY, endY = clamp_cut_values(
                    startX, endX, startY, endY, source_image
                )
                face_temp = source_image[startY:endY, startX:endX]
                face_temp = resize_image_keep_content(face_temp)
                testfaces = get_all_faces(face_temp)
                if testfaces is not None and len(testfaces) > 0:
                    i += 1
                    face_data.append([testfaces[0], face_temp])
                    found = True
                    break

            if not found:
                print("No face found after resizing, this shouldn't happen!")
            continue

        face_temp = source_image[startY:endY, startX:endX]
        if face_temp.size < 1:
            continue

        i += 1
        face_data.append([face, face_temp])
    return face_data


def clamp_cut_values(startX, endX, startY, endY, image):
    if startX < 0:
        startX = 0
    if endX > image.shape[1]:
        endX = image.shape[1]
    if startY < 0:
        startY = 0
    if endY > image.shape[0]:
        endY = image.shape[0]
    return startX, endX, startY, endY



def face_offset_top(face: Face, offset):
    face["bbox"][1] += offset
    face["bbox"][3] += offset
    lm106 = face.landmark_2d_106
    add = np.full_like(lm106, [0, offset])
    face["landmark_2d_106"] = lm106 + add
    return face


def resize_image_keep_content(image, new_width=512, new_height=512):
    dim = None
    (h, w) = image.shape[:2]
    if h > w:
        r = new_height / float(h)
        dim = (int(w * r), new_height)
    else:
        # Calculate the ratio of the width and construct the dimensions
        r = new_width / float(w)
        dim = (new_width, int(h * r))
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    (h, w) = image.shape[:2]
    if h == new_height and w == new_width:
        return image
    resize_img = np.zeros(shape=(new_height, new_width, 3), dtype=image.dtype)
    offs = (new_width - w) if h == new_height else (new_height - h)
    startoffs = int(offs // 2) if offs % 2 == 0 else int(offs // 2) + 1
    offs = int(offs // 2)

    if h == new_height:
        resize_img[0:new_height, startoffs : new_width - offs] = image
    else:
        resize_img[startoffs : new_height - offs, 0:new_width] = image
    return resize_img


def rotate_image_90(image, rotate=True):
    if rotate:
        return np.rot90(image)
    else:
        return np.rot90(image, 1, (1, 0))


def rotate_anticlockwise(frame):
    return rotate_image_90(frame)


def rotate_clockwise(frame):
    return rotate_image_90(frame, False)


def rotate_image_180(image):
    return np.flip(image, 0)


# alignment code from insightface https://github.com/deepinsight/insightface/blob/master/python-package/insightface/utils/face_align.py

arcface_dst = np.array(
    [
        [38.2946, 51.6963],
        [73.5318, 51.5014],
        [56.0252, 71.7366],
        [41.5493, 92.3655],
        [70.7299, 92.2041],
    ],
    dtype=np.float32,
)


def estimate_norm(lmk, image_size=112):
    assert lmk.shape == (5, 2)
    if image_size % 112 == 0:
        ratio = float(image_size) / 112.0
        diff_x = 0
    elif image_size % 128 == 0:
        ratio = float(image_size) / 128.0
        diff_x = 8.0 * ratio
    elif image_size % 512 == 0:
        ratio = float(image_size) / 512.0
        diff_x = 32.0 * ratio

    dst = arcface_dst * ratio
    dst[:, 0] += diff_x
    tform = trans.SimilarityTransform()
    tform.estimate(lmk, dst)
    M = tform.params[0:2, :]
    return M



# aligned, M = norm_crop2(f[1], face.kps, 512)
def align_crop(img, landmark, image_size=112, mode="arcface"):
    M = estimate_norm(landmark, image_size)
    warped = cv2.warpAffine(img, M, (image_size, image_size), borderValue=0.0)
    return warped, M


def square_crop(im, S):
    if im.shape[0] > im.shape[1]:
        height = S
        width = int(float(im.shape[1]) / im.shape[0] * S)
        scale = float(S) / im.shape[0]
    else:
        width = S
        height = int(float(im.shape[0]) / im.shape[1] * S)
        scale = float(S) / im.shape[1]
    resized_im = cv2.resize(im, (width, height))
    det_im = np.zeros((S, S, 3), dtype=np.uint8)
    det_im[: resized_im.shape[0], : resized_im.shape[1], :] = resized_im
    return det_im, scale


def transform(data, center, output_size, scale, rotation):
    scale_ratio = scale
    rot = float(rotation) * np.pi / 180.0
    # translation = (output_size/2-center[0]*scale_ratio, output_size/2-center[1]*scale_ratio)
    t1 = trans.SimilarityTransform(scale=scale_ratio)
    cx = center[0] * scale_ratio
    cy = center[1] * scale_ratio
    t2 = trans.SimilarityTransform(translation=(-1 * cx, -1 * cy))
    t3 = trans.SimilarityTransform(rotation=rot)
    t4 = trans.SimilarityTransform(translation=(output_size / 2, output_size / 2))
    t = t1 + t2 + t3 + t4
    M = t.params[0:2]
    cropped = cv2.warpAffine(data, M, (output_size, output_size), borderValue=0.0)
    return cropped, M


def trans_points2d(pts, M):
    new_pts = np.zeros(shape=pts.shape, dtype=np.float32)
    for i in range(pts.shape[0]):
        pt = pts[i]
        new_pt = np.array([pt[0], pt[1], 1.0], dtype=np.float32)
        new_pt = np.dot(M, new_pt)
        # print('new_pt', new_pt.shape, new_pt)
        new_pts[i] = new_pt[0:2]

    return new_pts


def trans_points3d(pts, M):
    scale = np.sqrt(M[0][0] * M[0][0] + M[0][1] * M[0][1])
    # print(scale)
    new_pts = np.zeros(shape=pts.shape, dtype=np.float32)
    for i in range(pts.shape[0]):
        pt = pts[i]
        new_pt = np.array([pt[0], pt[1], 1.0], dtype=np.float32)
        new_pt = np.dot(M, new_pt)
        # print('new_pt', new_pt.shape, new_pt)
        new_pts[i][0:2] = new_pt[0:2]
        new_pts[i][2] = pts[i][2] * scale

    return new_pts


def trans_points(pts, M):
    if pts.shape[1] == 2:
        return trans_points2d(pts, M)
    else:
        return trans_points3d(pts, M)
    
def create_blank_image(width, height):
    img = np.zeros((height, width, 4), dtype=np.uint8)
    img[:] = [0,0,0,0]
    return img


```

# roop\FaceSet.py

```py
import numpy as np

class FaceSet:
    faces = []
    ref_images = []
    embedding_average = 'None'
    embeddings_backup = None

    def __init__(self):
        self.faces = []
        self.ref_images = []
        self.embeddings_backup = None

    def AverageEmbeddings(self):
        if len(self.faces) > 1 and self.embeddings_backup is None:
            self.embeddings_backup = self.faces[0]['embedding']
            embeddings = [face.embedding for face in self.faces]

            self.faces[0]['embedding'] = np.mean(embeddings, axis=0)
            # try median too?

```

# roop\core.py

```py
#!/usr/bin/env python3

import os
import sys
import shutil
# single thread doubles cuda performance - needs to be set before torch import
if any(arg.startswith('--execution-provider') for arg in sys.argv):
    os.environ['OMP_NUM_THREADS'] = '1'

import warnings
from typing import List
import platform
import signal
import torch
import onnxruntime
import pathlib
import argparse

from time import time

import roop.globals
import roop.metadata
import roop.utilities as util
import roop.util_ffmpeg as ffmpeg
import ui.main as main
from settings import Settings
from roop.face_util import extract_face_images
from roop.ProcessEntry import ProcessEntry
from roop.ProcessMgr import ProcessMgr
from roop.ProcessOptions import ProcessOptions
from roop.capturer import get_video_frame_total, release_video


clip_text = None

call_display_ui = None

process_mgr = None


if 'ROCMExecutionProvider' in roop.globals.execution_providers:
    del torch

warnings.filterwarnings('ignore', category=FutureWarning, module='insightface')
warnings.filterwarnings('ignore', category=UserWarning, module='torchvision')


def parse_args() -> None:
    signal.signal(signal.SIGINT, lambda signal_number, frame: destroy())
    roop.globals.headless = False

    program = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=100))
    program.add_argument('--server_share', help='Public server', dest='server_share', action='store_true', default=False)
    program.add_argument('--cuda_device_id', help='Index of the cuda gpu to use', dest='cuda_device_id', type=int, default=0)
    roop.globals.startup_args = program.parse_args()
    # Always enable all processors when using GUI
    roop.globals.frame_processors = ['face_swapper', 'face_enhancer']


def encode_execution_providers(execution_providers: List[str]) -> List[str]:
    return [execution_provider.replace('ExecutionProvider', '').lower() for execution_provider in execution_providers]


def decode_execution_providers(execution_providers: List[str]) -> List[str]:
    list_providers = [provider for provider, encoded_execution_provider in zip(onnxruntime.get_available_providers(), encode_execution_providers(onnxruntime.get_available_providers()))
            if any(execution_provider in encoded_execution_provider for execution_provider in execution_providers)]
    
    try:
        for i in range(len(list_providers)):
            if list_providers[i] == 'CUDAExecutionProvider':
                list_providers[i] = ('CUDAExecutionProvider', {'device_id': roop.globals.cuda_device_id})
                torch.cuda.set_device(roop.globals.cuda_device_id)
                break
    except:
        pass

    return list_providers
    


def suggest_max_memory() -> int:
    if platform.system().lower() == 'darwin':
        return 4
    return 16


def suggest_execution_providers() -> List[str]:
    return encode_execution_providers(onnxruntime.get_available_providers())


def suggest_execution_threads() -> int:
    if 'DmlExecutionProvider' in roop.globals.execution_providers:
        return 1
    if 'ROCMExecutionProvider' in roop.globals.execution_providers:
        return 1
    return 8


def limit_resources() -> None:
    # limit memory usage
    if roop.globals.max_memory:
        memory = roop.globals.max_memory * 1024 ** 3
        if platform.system().lower() == 'darwin':
            memory = roop.globals.max_memory * 1024 ** 6
        if platform.system().lower() == 'windows':
            import ctypes
            kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
            kernel32.SetProcessWorkingSetSize(-1, ctypes.c_size_t(memory), ctypes.c_size_t(memory))
        else:
            import resource
            resource.setrlimit(resource.RLIMIT_DATA, (memory, memory))



def release_resources() -> None:
    import gc
    global process_mgr

    if process_mgr is not None:
        process_mgr.release_resources()
        process_mgr = None

    gc.collect()
    # if 'CUDAExecutionProvider' in roop.globals.execution_providers and torch.cuda.is_available():
    #     with torch.cuda.device('cuda'):
    #         torch.cuda.empty_cache()
    #         torch.cuda.ipc_collect()


def pre_check() -> bool:
    if sys.version_info < (3, 9):
        update_status('Python version is not supported - please upgrade to 3.9 or higher.')
        return False
    
    download_directory_path = util.resolve_relative_path('../models')
    util.conditional_download(download_directory_path, ['https://huggingface.co/countfloyd/deepfake/resolve/main/inswapper_128.onnx'])
    util.conditional_download(download_directory_path, ['https://huggingface.co/countfloyd/deepfake/resolve/main/GFPGANv1.4.onnx'])
    util.conditional_download(download_directory_path, ['https://github.com/csxmli2016/DMDNet/releases/download/v1/DMDNet.pth'])
    util.conditional_download(download_directory_path, ['https://huggingface.co/countfloyd/deepfake/resolve/main/GPEN-BFR-512.onnx'])
    util.conditional_download(download_directory_path, ['https://huggingface.co/countfloyd/deepfake/resolve/main/restoreformer_plus_plus.onnx'])
    util.conditional_download(download_directory_path, ['https://huggingface.co/countfloyd/deepfake/resolve/main/xseg.onnx'])
    download_directory_path = util.resolve_relative_path('../models/CLIP')
    util.conditional_download(download_directory_path, ['https://huggingface.co/countfloyd/deepfake/resolve/main/rd64-uni-refined.pth'])
    download_directory_path = util.resolve_relative_path('../models/CodeFormer')
    util.conditional_download(download_directory_path, ['https://huggingface.co/countfloyd/deepfake/resolve/main/CodeFormerv0.1.onnx'])
    download_directory_path = util.resolve_relative_path('../models/Frame')
    util.conditional_download(download_directory_path, ['https://huggingface.co/countfloyd/deepfake/resolve/main/deoldify_artistic.onnx'])
    util.conditional_download(download_directory_path, ['https://huggingface.co/countfloyd/deepfake/resolve/main/deoldify_stable.onnx'])
    util.conditional_download(download_directory_path, ['https://huggingface.co/countfloyd/deepfake/resolve/main/isnet-general-use.onnx'])
    util.conditional_download(download_directory_path, ['https://huggingface.co/countfloyd/deepfake/resolve/main/real_esrgan_x4.onnx'])
    util.conditional_download(download_directory_path, ['https://huggingface.co/countfloyd/deepfake/resolve/main/real_esrgan_x2.onnx'])
    util.conditional_download(download_directory_path, ['https://huggingface.co/countfloyd/deepfake/resolve/main/lsdir_x4.onnx'])

    if not shutil.which('ffmpeg'):
       update_status('ffmpeg is not installed.')
    return True

def set_display_ui(function):
    global call_display_ui

    call_display_ui = function


def update_status(message: str) -> None:
    global call_display_ui

    print(message)
    if call_display_ui is not None:
        call_display_ui(message)




def start() -> None:
    if roop.globals.headless:
        print('Headless mode currently unsupported - starting UI!')
        # faces = extract_face_images(roop.globals.source_path,  (False, 0))
        # roop.globals.INPUT_FACES.append(faces[roop.globals.source_face_index])
        # faces = extract_face_images(roop.globals.target_path,  (False, util.has_image_extension(roop.globals.target_path)))
        # roop.globals.TARGET_FACES.append(faces[roop.globals.target_face_index])
        # if 'face_enhancer' in roop.globals.frame_processors:
        #     roop.globals.selected_enhancer = 'GFPGAN'
       
    batch_process_regular(None, False, None)


def get_processing_plugins(masking_engine):
    processors = {  "faceswap": {}}
    if masking_engine is not None:
        processors.update({masking_engine: {}})
    
    if roop.globals.selected_enhancer == 'GFPGAN':
        processors.update({"gfpgan": {}})
    elif roop.globals.selected_enhancer == 'Codeformer':
        processors.update({"codeformer": {}})
    elif roop.globals.selected_enhancer == 'DMDNet':
        processors.update({"dmdnet": {}})
    elif roop.globals.selected_enhancer == 'GPEN':
        processors.update({"gpen": {}})
    elif roop.globals.selected_enhancer == 'Restoreformer++':
        processors.update({"restoreformer++": {}})
    return processors


def live_swap(frame, options):
    global process_mgr

    if frame is None:
        return frame

    if process_mgr is None:
        process_mgr = ProcessMgr(None)
    
#    if len(roop.globals.INPUT_FACESETS) <= selected_index:
#        selected_index = 0
    process_mgr.initialize(roop.globals.INPUT_FACESETS, roop.globals.TARGET_FACES, options)
    newframe = process_mgr.process_frame(frame)
    if newframe is None:
        return frame
    return newframe


def batch_process_regular(output_method, files:list[ProcessEntry], masking_engine:str, new_clip_text:str, use_new_method, imagemask, restore_original_mouth, num_swap_steps, progress, selected_index = 0) -> None:
    global clip_text, process_mgr

    release_resources()
    limit_resources()
    if process_mgr is None:
        process_mgr = ProcessMgr(progress)
    mask = imagemask["layers"][0] if imagemask is not None else None
    if len(roop.globals.INPUT_FACESETS) <= selected_index:
        selected_index = 0
    options = ProcessOptions(get_processing_plugins(masking_engine), roop.globals.distance_threshold, roop.globals.blend_ratio,
                              roop.globals.face_swap_mode, selected_index, new_clip_text, mask, num_swap_steps,
                              roop.globals.subsample_size, False, restore_original_mouth)
    process_mgr.initialize(roop.globals.INPUT_FACESETS, roop.globals.TARGET_FACES, options)
    batch_process(output_method, files, use_new_method)
    return

def batch_process_with_options(files:list[ProcessEntry], options, progress):
    global clip_text, process_mgr

    release_resources()
    limit_resources()
    if process_mgr is None:
        process_mgr = ProcessMgr(progress)
    process_mgr.initialize(roop.globals.INPUT_FACESETS, roop.globals.TARGET_FACES, options)
    roop.globals.keep_frames = False
    roop.globals.wait_after_extraction = False
    roop.globals.skip_audio = False
    batch_process("Files", files, True)



def batch_process(output_method, files:list[ProcessEntry], use_new_method) -> None:
    global clip_text, process_mgr

    roop.globals.processing = True

    # limit threads for some providers
    max_threads = suggest_execution_threads()
    if max_threads == 1:
        roop.globals.execution_threads = 1

    imagefiles:list[ProcessEntry] = []
    videofiles:list[ProcessEntry] = []
           
    update_status('Sorting videos/images')


    for index, f in enumerate(files):
        fullname = f.filename
        if util.has_image_extension(fullname):
            destination = util.get_destfilename_from_path(fullname, roop.globals.output_path, f'.{roop.globals.CFG.output_image_format}')
            destination = util.replace_template(destination, index=index)
            pathlib.Path(os.path.dirname(destination)).mkdir(parents=True, exist_ok=True)
            f.finalname = destination
            imagefiles.append(f)

        elif util.is_video(fullname) or util.has_extension(fullname, ['gif']):
            destination = util.get_destfilename_from_path(fullname, roop.globals.output_path, f'__temp.{roop.globals.CFG.output_video_format}')
            f.finalname = destination
            videofiles.append(f)



    if(len(imagefiles) > 0):
        update_status('Processing image(s)')
        origimages = []
        fakeimages = []
        for f in imagefiles:
            origimages.append(f.filename)
            fakeimages.append(f.finalname)

        process_mgr.run_batch(origimages, fakeimages, roop.globals.execution_threads)
        origimages.clear()
        fakeimages.clear()

    if(len(videofiles) > 0):
        for index,v in enumerate(videofiles):
            if not roop.globals.processing:
                end_processing('Processing stopped!')
                return
            fps = v.fps if v.fps > 0 else util.detect_fps(v.filename)
            if v.endframe == 0:
                v.endframe = get_video_frame_total(v.filename)

            is_streaming_only = output_method == "Virtual Camera"
            if is_streaming_only == False:
                update_status(f'Creating {os.path.basename(v.finalname)} with {fps} FPS...')

            start_processing = time()
            if is_streaming_only == False and roop.globals.keep_frames or not use_new_method:
                util.create_temp(v.filename)
                update_status('Extracting frames...')
                ffmpeg.extract_frames(v.filename,v.startframe,v.endframe, fps)
                if not roop.globals.processing:
                    end_processing('Processing stopped!')
                    return

                temp_frame_paths = util.get_temp_frame_paths(v.filename)
                process_mgr.run_batch(temp_frame_paths, temp_frame_paths, roop.globals.execution_threads)
                if not roop.globals.processing:
                    end_processing('Processing stopped!')
                    return
                if roop.globals.wait_after_extraction:
                    extract_path = os.path.dirname(temp_frame_paths[0])
                    util.open_folder(extract_path)
                    input("Press any key to continue...")
                    print("Resorting frames to create video")
                    util.sort_rename_frames(extract_path)                                    
                
                ffmpeg.create_video(v.filename, v.finalname, fps)
                if not roop.globals.keep_frames:
                    util.delete_temp_frames(temp_frame_paths[0])
            else:
                if util.has_extension(v.filename, ['gif']):
                    skip_audio = True
                else:
                    skip_audio = roop.globals.skip_audio
                process_mgr.run_batch_inmem(output_method, v.filename, v.finalname, v.startframe, v.endframe, fps,roop.globals.execution_threads)
                
            if not roop.globals.processing:
                end_processing('Processing stopped!')
                return
            
            video_file_name = v.finalname
            if os.path.isfile(video_file_name):
                destination = ''
                if util.has_extension(v.filename, ['gif']):
                    gifname = util.get_destfilename_from_path(v.filename, roop.globals.output_path, '.gif')
                    destination = util.replace_template(gifname, index=index)
                    pathlib.Path(os.path.dirname(destination)).mkdir(parents=True, exist_ok=True)

                    update_status('Creating final GIF')
                    ffmpeg.create_gif_from_video(video_file_name, destination)
                    if os.path.isfile(destination):
                        os.remove(video_file_name)
                else:
                    skip_audio = roop.globals.skip_audio
                    destination = util.replace_template(video_file_name, index=index)
                    pathlib.Path(os.path.dirname(destination)).mkdir(parents=True, exist_ok=True)

                    if not skip_audio:
                        ffmpeg.restore_audio(video_file_name, v.filename, v.startframe, v.endframe, destination)
                        if os.path.isfile(destination):
                            os.remove(video_file_name)
                    else:
                        shutil.move(video_file_name, destination)

            elif is_streaming_only == False:
                update_status(f'Failed processing {os.path.basename(v.finalname)}!')
            elapsed_time = time() - start_processing
            average_fps = (v.endframe - v.startframe) / elapsed_time
            update_status(f'\nProcessing {os.path.basename(destination)} took {elapsed_time:.2f} secs, {average_fps:.2f} frames/s')
    end_processing('Finished')


def end_processing(msg:str):
    update_status(msg)
    roop.globals.target_folder_path = None
    release_resources()


def destroy() -> None:
    if roop.globals.target_path:
        util.clean_temp(roop.globals.target_path)
    release_resources()        
    sys.exit()


def run() -> None:
    parse_args()
    if not pre_check():
        return
    roop.globals.CFG = Settings('config.yaml')
    roop.globals.cuda_device_id = roop.globals.startup_args.cuda_device_id
    roop.globals.execution_threads = roop.globals.CFG.max_threads
    roop.globals.video_encoder = roop.globals.CFG.output_video_codec
    roop.globals.video_quality = roop.globals.CFG.video_quality
    roop.globals.max_memory = roop.globals.CFG.memory_limit if roop.globals.CFG.memory_limit > 0 else None
    if roop.globals.startup_args.server_share:
        roop.globals.CFG.server_share = True
    main.run()

```

# roop\capturer.py

```py
from typing import Optional
import cv2
import numpy as np

from roop.typing import Frame

current_video_path = None
current_frame_total = 0
current_capture = None

def get_image_frame(filename: str):
    try:
        return cv2.imdecode(np.fromfile(filename, dtype=np.uint8), cv2.IMREAD_COLOR)
    except:
        print(f"Exception reading {filename}")
    return None

    
def get_video_frame(video_path: str, frame_number: int = 0) -> Optional[Frame]:
    global current_video_path, current_capture, current_frame_total

    if video_path != current_video_path:
        release_video()
        current_capture = cv2.VideoCapture(video_path)
        current_video_path = video_path
        current_frame_total = current_capture.get(cv2.CAP_PROP_FRAME_COUNT)

    current_capture.set(cv2.CAP_PROP_POS_FRAMES, min(current_frame_total, frame_number - 1))
    has_frame, frame = current_capture.read()
    if has_frame:
        return frame
    return None

def release_video():
    global current_capture    

    if current_capture is not None:
        current_capture.release()
        current_capture = None
        

def get_video_frame_total(video_path: str) -> int:
    capture = cv2.VideoCapture(video_path)
    video_frame_total = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    capture.release()
    return video_frame_total

```

# installer\windows_run.bat

```bat
@echo off

REM No CLI arguments supported anymore
set COMMANDLINE_ARGS=

cd /D "%~dp0"

echo "%CD%"| findstr /C:" " >nul && echo This script relies on Miniconda which can not be silently installed under a path with spaces. && goto end

set PATH=%PATH%;%SystemRoot%\system32

@rem config
set INSTALL_DIR=%cd%\installer_files
set CONDA_ROOT_PREFIX=%cd%\installer_files\conda
set INSTALL_ENV_DIR=%cd%\installer_files\env
set MINICONDA_DOWNLOAD_URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
set FFMPEG_DOWNLOAD_URL=https://github.com/GyanD/codexffmpeg/releases/download/2023-06-21-git-1bcb8a7338/ffmpeg-2023-06-21-git-1bcb8a7338-essentials_build.zip
set INSTALL_FFMPEG_DIR=%cd%\installer_files\ffmpeg
set INSIGHTFACE_PACKAGE_URL=https://github.com/C0untFloyd/roop-unleashed/releases/download/3.6.6/insightface-0.7.3-cp310-cp310-win_amd64.whl
set INSIGHTFACE_PACKAGE_PATH=%INSTALL_DIR%\insightface-0.7.3-cp310-cp310-win_amd64.whl

set conda_exists=F
set ffmpeg_exists=F

@rem figure out whether git and conda needs to be installed
call "%CONDA_ROOT_PREFIX%\_conda.exe" --version >nul 2>&1
if "%ERRORLEVEL%" EQU "0" set conda_exists=T

@rem Check if FFmpeg is already in PATH
where ffmpeg >nul 2>&1
if "%ERRORLEVEL%" EQU "0" (
    echo FFmpeg is already installed.
    set ffmpeg_exists=T
)

@rem (if necessary) install git and conda into a contained environment

@rem download conda
if "%conda_exists%" == "F" (
    echo Downloading Miniconda from %MINICONDA_DOWNLOAD_URL% to %INSTALL_DIR%\miniconda_installer.exe
    mkdir "%INSTALL_DIR%"
    call curl -Lk "%MINICONDA_DOWNLOAD_URL%" > "%INSTALL_DIR%\miniconda_installer.exe" || ( echo. && echo Miniconda failed to download. && goto end )
    echo Installing Miniconda to %CONDA_ROOT_PREFIX%
    start /wait "" "%INSTALL_DIR%\miniconda_installer.exe" /InstallationType=JustMe /NoShortcuts=1 /AddToPath=0 /RegisterPython=0 /NoRegistry=1 /S /D=%CONDA_ROOT_PREFIX%

    @rem test the conda binary
    echo Miniconda version:
    call "%CONDA_ROOT_PREFIX%\_conda.exe" --version || ( echo. && echo Miniconda not found. && goto end )
)

@rem create the installer env
if not exist "%INSTALL_ENV_DIR%" (
    echo Creating Conda Environment
    call "%CONDA_ROOT_PREFIX%\_conda.exe" create --no-shortcuts -y -k --prefix "%INSTALL_ENV_DIR%" python=3.10 || ( echo. && echo ERROR: Conda environment creation failed. && goto end )
    @rem check if conda environment was actually created
    if not exist "%INSTALL_ENV_DIR%\python.exe" ( echo. && echo ERROR: Conda environment is empty. && goto end )
    @rem activate installer env
    call "%CONDA_ROOT_PREFIX%\condabin\conda.bat" activate "%INSTALL_ENV_DIR%" || ( echo. && echo ERROR: Miniconda hook not found. && goto end )
    @rem Download insightface package
    echo Downloading insightface package from %INSIGHTFACE_PACKAGE_URL% to %INSIGHTFACE_PACKAGE_PATH%
    call curl -Lk "%INSIGHTFACE_PACKAGE_URL%" > "%INSIGHTFACE_PACKAGE_PATH%" || ( echo. && echo ERROR: Insightface package failed to download. && goto end )
    @rem install insightface package using pip
    echo Installing insightface package
    call pip install "%INSIGHTFACE_PACKAGE_PATH%" || ( echo. && echo ERROR: Insightface package installation failed. && goto end )
)

@rem Download and install FFmpeg if not already installed
if "%ffmpeg_exists%" == "F" (
    if not exist "%INSTALL_FFMPEG_DIR%" (
        echo Downloading ffmpeg from %FFMPEG_DOWNLOAD_URL% to %INSTALL_DIR%
        call curl -Lk "%FFMPEG_DOWNLOAD_URL%" > "%INSTALL_DIR%\ffmpeg.zip" || ( echo. && echo ffmpeg failed to download. && goto end )
        call powershell -command "Expand-Archive -Force '%INSTALL_DIR%\ffmpeg.zip' '%INSTALL_DIR%\'"
        cd "%INSTALL_DIR%"
        move ffmpeg-* ffmpeg
        setx PATH "%INSTALL_FFMPEG_DIR%\bin\;%PATH%"
        echo To use videos, you need to restart roop after this installation.
        cd ..
    )
) else (
    echo Skipping FFmpeg installation as it is already available.
)

@rem setup installer env
@rem check if conda environment was actually created
if not exist "%INSTALL_ENV_DIR%\python.exe" ( echo. && echo ERROR: Conda environment is empty. && goto end )
@rem activate installer env
call "%CONDA_ROOT_PREFIX%\condabin\conda.bat" activate "%INSTALL_ENV_DIR%" || ( echo. && echo ERROR: Miniconda hook not found. && goto end )
echo Launching roop unleashed
call python installer.py %COMMANDLINE_ARGS%

echo.
echo Done!

:end
pause

```

# installer\macOSinstaller.sh

```sh
#!/bin/bash

# This script checks and installs all dependencies which are needed to run roop-unleashed. After that, it clones the repo.
# Execute this easily with /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/PJF16/roop-unleashed/master/installer/macOSinstaller.sh)

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "Starting check and installation process of dependencies for roop-unleashed"

# Check if Homebrew is installed
if ! command_exists brew; then
    echo "Homebrew is not installed. Starting installation..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew is already installed."
fi

# Update Homebrew
echo "Updating Homebrew..."
brew update

# Check if Python 3.11 is installed
if brew list --versions python@3.11 >/dev/null; then
    echo "Python 3.11 is already installed."
else
    echo "Python 3.11 is not installed. Installing it now..."
    brew install python@3.11
fi

# Check if python-tk@3.11 is installed
if brew list --versions python-tk@3.11 >/dev/null; then
    echo "python-tk@3.11 is already installed."
else
    echo "python-tk@3.11 is not installed. Installing it now..."
    brew install python-tk@3.11
fi

# Check if ffmpeg is installed
if command_exists ffmpeg; then
    echo "ffmpeg is already installed."
else
    echo "ffmpeg is not installed. Installing it now..."
    brew install ffmpeg
fi

# Check if git is installed
if command_exists git; then
    echo "git is already installed."
else
    echo "git is not installed. Installing it now..."
    brew install git
fi

# Clone the repository
REPO_URL="https://github.com/C0untFloyd/roop-unleashed.git"
REPO_NAME="roop-unleashed"

echo "Cloning the repository $REPO_URL..."
git clone $REPO_URL

# Check if the repository was cloned successfully
if [ -d "$REPO_NAME" ]; then
    echo "Repository cloned successfully. Changing into directory $REPO_NAME..."
    cd "$REPO_NAME"
else
    echo "Failed to clone the repository."
fi

echo "Check and installation process completed."


```

# installer\installer.py

```py
import argparse
import glob
import os
import shutil
import site
import subprocess
import sys


script_dir = os.getcwd()


def run_cmd(cmd, capture_output=False, env=None):
    # Run shell commands
    return subprocess.run(cmd, shell=True, capture_output=capture_output, env=env)


def check_env():
    # If we have access to conda, we are probably in an environment
    conda_not_exist = run_cmd("conda", capture_output=True).returncode
    if conda_not_exist:
        print("Conda is not installed. Exiting...")
        sys.exit()
    
    # Ensure this is a new environment and not the base environment
    if os.environ["CONDA_DEFAULT_ENV"] == "base":
        print("Create an environment for this project and activate it. Exiting...")
        sys.exit()


def install_dependencies():
    global MY_PATH

    # Install Git and clone repo
    run_cmd("conda install -y -k git")
    run_cmd("git clone https://github.com/C0untFloyd/roop-unleashed.git")
    os.chdir(MY_PATH)
    run_cmd("git checkout 5bfafdc97a0c47b46ec83e6530a57399aaad75d7")
    # Installs dependencies from requirements.txt
    run_cmd("python -m pip install -r requirements.txt")



def update_dependencies():
    global MY_PATH
    
    os.chdir(MY_PATH)
	# do a hard reset for to update even if there are local changes
    run_cmd("git fetch --all")
    run_cmd("git reset --hard origin/main")
    run_cmd("git pull")
    # Installs/Updates dependencies from all requirements.txt
    run_cmd("python -m pip install -r requirements.txt")


def start_app():
    global MY_PATH
    
    os.chdir(MY_PATH)
    # forward commandline arguments
    sys.argv.pop(0)
    args = ' '.join(sys.argv)
    print("Launching App")
    run_cmd(f'python run.py {args}')


if __name__ == "__main__":
    global MY_PATH
    
    MY_PATH = "roop-unleashed"

    
    # Verifies we are in a conda environment
    check_env()

    # If webui has already been installed, skip and run
    if not os.path.exists(MY_PATH):
        install_dependencies()
    else:
        # moved update from batch to here, because of batch limitations
        updatechoice = input("Check for Updates? [y/n]").lower()
        if updatechoice == "y":
           update_dependencies()

    # Run the model with webui
    os.chdir(script_dir)
    start_app()

```

# docs\screenshot.png

This is a binary file of the type: Image

# clip\__init__.py

```py
from .clip import *

```

# clip\vitseg.py

```py
import math
from posixpath import basename, dirname, join
# import clip
from clip.model import convert_weights
import torch
import json
from torch import nn
from torch.nn import functional as nnf
from torch.nn.modules import activation
from torch.nn.modules.activation import ReLU
from torchvision import transforms

normalize = transforms.Normalize(mean=(0.48145466, 0.4578275, 0.40821073), std=(0.26862954, 0.26130258, 0.27577711))

from torchvision.models import ResNet


def process_prompts(conditional, prompt_list, conditional_map):
    # DEPRECATED
            
    # randomly sample a synonym
    words = [conditional_map[int(i)] for i in conditional]
    words = [syns[torch.multinomial(torch.ones(len(syns)), 1, replacement=True).item()] for syns in words]
    words = [w.replace('_', ' ') for w in words]

    if prompt_list is not None:
        prompt_indices = torch.multinomial(torch.ones(len(prompt_list)), len(words), replacement=True)
        prompts = [prompt_list[i] for i in prompt_indices]
    else:
        prompts = ['a photo of {}'] * (len(words))

    return [promt.format(w) for promt, w in zip(prompts, words)]


class VITDenseBase(nn.Module):
    
    def rescaled_pos_emb(self, new_size):
        assert len(new_size) == 2

        a = self.model.positional_embedding[1:].T.view(1, 768, *self.token_shape)
        b = nnf.interpolate(a, new_size, mode='bicubic', align_corners=False).squeeze(0).view(768, new_size[0]*new_size[1]).T
        return torch.cat([self.model.positional_embedding[:1], b])

    def visual_forward(self, x_inp, extract_layers=(), skip=False, mask=None):
        
        with torch.no_grad():

            x_inp = nnf.interpolate(x_inp, (384, 384))

            x = self.model.patch_embed(x_inp)
            cls_token = self.model.cls_token.expand(x.shape[0], -1, -1)  # stole cls_tokens impl from Phil Wang, thanks
            if self.model.dist_token is None:
                x = torch.cat((cls_token, x), dim=1)
            else:
                x = torch.cat((cls_token, self.model.dist_token.expand(x.shape[0], -1, -1), x), dim=1)
            x = self.model.pos_drop(x + self.model.pos_embed)

            activations = []
            for i, block in enumerate(self.model.blocks):
                x = block(x)

                if i in extract_layers:
                    # permute to be compatible with CLIP
                    activations += [x.permute(1,0,2)]                

            x = self.model.norm(x)
            x = self.model.head(self.model.pre_logits(x[:, 0]))

            # again for CLIP compatibility
            # x = x.permute(1, 0, 2)

        return x, activations, None

    def sample_prompts(self, words, prompt_list=None):

        prompt_list = prompt_list if prompt_list is not None else self.prompt_list

        prompt_indices = torch.multinomial(torch.ones(len(prompt_list)), len(words), replacement=True)
        prompts = [prompt_list[i] for i in prompt_indices]
        return [promt.format(w) for promt, w in zip(prompts, words)]

    def get_cond_vec(self, conditional, batch_size):
        # compute conditional from a single string
        if conditional is not None and type(conditional) == str:
            cond = self.compute_conditional(conditional)
            cond = cond.repeat(batch_size, 1)

        # compute conditional from string list/tuple
        elif conditional is not None and type(conditional) in {list, tuple} and type(conditional[0]) == str:
            assert len(conditional) == batch_size
            cond = self.compute_conditional(conditional)

        # use conditional directly
        elif conditional is not None and type(conditional) == torch.Tensor and conditional.ndim == 2:
            cond = conditional

        # compute conditional from image
        elif conditional is not None and type(conditional) == torch.Tensor:
            with torch.no_grad():
                cond, _, _ = self.visual_forward(conditional)
        else:
            raise ValueError('invalid conditional')
        return cond   

    def compute_conditional(self, conditional):
        import clip

        dev = next(self.parameters()).device

        if type(conditional) in {list, tuple}:
            text_tokens = clip.tokenize(conditional).to(dev)
            cond = self.clip_model.encode_text(text_tokens)
        else:
            if conditional in self.precomputed_prompts:
                cond = self.precomputed_prompts[conditional].float().to(dev)
            else:
                text_tokens = clip.tokenize([conditional]).to(dev)
                cond = self.clip_model.encode_text(text_tokens)[0]
        
        return cond


class VITDensePredT(VITDenseBase):

    def __init__(self, extract_layers=(3, 6, 9), cond_layer=0, reduce_dim=128, n_heads=4, prompt='fixed', 
                 depth=3, extra_blocks=0, reduce_cond=None, fix_shift=False,
                 learn_trans_conv_only=False, refine=None, limit_to_clip_only=False, upsample=False, 
                 add_calibration=False, process_cond=None, not_pretrained=False):
        super().__init__()
        # device = 'cpu'

        self.extract_layers = extract_layers
        self.cond_layer = cond_layer
        self.limit_to_clip_only = limit_to_clip_only
        self.process_cond = None
        
        if add_calibration:
            self.calibration_conds = 1

        self.upsample_proj = nn.Conv2d(reduce_dim, 1, kernel_size=1) if upsample else None

        self.add_activation1 = True

        import timm 
        self.model = timm.create_model('vit_base_patch16_384', pretrained=True)
        self.model.head = nn.Linear(768, 512 if reduce_cond is None else reduce_cond)

        for p in self.model.parameters():
            p.requires_grad_(False)

        import clip
        self.clip_model, _ = clip.load('ViT-B/16', device='cpu', jit=False)
        # del self.clip_model.visual
        
        
        self.token_shape = (14, 14)

        # conditional
        if reduce_cond is not None:
            self.reduce_cond = nn.Linear(512, reduce_cond)
            for p in self.reduce_cond.parameters():
                p.requires_grad_(False)
        else:
            self.reduce_cond = None

        # self.film = AVAILABLE_BLOCKS['film'](512, 128)
        self.film_mul = nn.Linear(512 if reduce_cond is None else reduce_cond, reduce_dim)
        self.film_add = nn.Linear(512 if reduce_cond is None else reduce_cond, reduce_dim)
        
        # DEPRECATED
        # self.conditional_map = {c['id']: c['synonyms'] for c in json.load(open(cond_map))}
        
        assert len(self.extract_layers) == depth

        self.reduces = nn.ModuleList([nn.Linear(768, reduce_dim) for _ in range(depth)])
        self.blocks = nn.ModuleList([nn.TransformerEncoderLayer(d_model=reduce_dim, nhead=n_heads) for _ in range(len(self.extract_layers))])
        self.extra_blocks = nn.ModuleList([nn.TransformerEncoderLayer(d_model=reduce_dim, nhead=n_heads) for _ in range(extra_blocks)])

        trans_conv_ks = (16, 16)
        self.trans_conv = nn.ConvTranspose2d(reduce_dim, 1, trans_conv_ks, stride=trans_conv_ks)

        # refinement and trans conv

        if learn_trans_conv_only:
            for p in self.parameters():
                p.requires_grad_(False)
            
            for p in self.trans_conv.parameters():
                p.requires_grad_(True)

        if prompt == 'fixed':
            self.prompt_list = ['a photo of a {}.']
        elif prompt == 'shuffle':
            self.prompt_list = ['a photo of a {}.', 'a photograph of a {}.', 'an image of a {}.', '{}.']
        elif prompt == 'shuffle+':
            self.prompt_list = ['a photo of a {}.', 'a photograph of a {}.', 'an image of a {}.', '{}.',
                                'a cropped photo of a {}.', 'a good photo of a {}.', 'a photo of one {}.',
                                'a bad photo of a {}.', 'a photo of the {}.']
        elif prompt == 'shuffle_clip':
            from models.clip_prompts import imagenet_templates
            self.prompt_list = imagenet_templates

        if process_cond is not None:
            if process_cond == 'clamp' or process_cond[0] == 'clamp':

                val = process_cond[1] if type(process_cond) in {list, tuple} else 0.2

                def clamp_vec(x):
                    return torch.clamp(x, -val, val)

                self.process_cond = clamp_vec

            elif process_cond.endswith('.pth'):
                
                shift = torch.load(process_cond)
                def add_shift(x):
                    return x + shift.to(x.device)

                self.process_cond = add_shift

        import pickle
        precomp = pickle.load(open('precomputed_prompt_vectors.pickle', 'rb'))
        self.precomputed_prompts = {k: torch.from_numpy(v) for k, v in precomp.items()}


    def forward(self, inp_image, conditional=None, return_features=False, mask=None):

        assert type(return_features) == bool

        # inp_image = inp_image.to(self.model.positional_embedding.device)

        if mask is not None:
            raise ValueError('mask not supported')

        # x_inp = normalize(inp_image)
        x_inp = inp_image

        bs, dev = inp_image.shape[0], x_inp.device

        inp_image_size = inp_image.shape[2:]

        cond = self.get_cond_vec(conditional, bs)

        visual_q, activations, _ = self.visual_forward(x_inp, extract_layers=[0] + list(self.extract_layers))

        activation1 = activations[0]
        activations = activations[1:]

        a = None
        for i, (activation, block, reduce) in enumerate(zip(activations[::-1], self.blocks, self.reduces)):
            
            if a is not None:
                a = reduce(activation) + a
            else:
                a = reduce(activation)

            if i == self.cond_layer:
                if self.reduce_cond is not None:
                    cond = self.reduce_cond(cond)
                
                a = self.film_mul(cond) * a + self.film_add(cond)

            a = block(a)

        for block in self.extra_blocks:
            a = a + block(a)

        a = a[1:].permute(1, 2, 0) # rm cls token and -> BS, Feats, Tokens

        size = int(math.sqrt(a.shape[2]))

        a = a.view(bs, a.shape[1], size, size)

        if self.trans_conv is not None:
            a = self.trans_conv(a)

        if self.upsample_proj is not None:
            a = self.upsample_proj(a)
            a = nnf.interpolate(a, x_inp.shape[2:], mode='bilinear')

        a = nnf.interpolate(a, inp_image_size)

        if return_features:
            return a, visual_q, cond, [activation1] + activations
        else:
            return a,

```

# clip\simple_tokenizer.py

```py
import gzip
import html
import os
from functools import lru_cache

import ftfy
import regex as re


@lru_cache()
def default_bpe():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "bpe_simple_vocab_16e6.txt.gz")


@lru_cache()
def bytes_to_unicode():
    """
    Returns list of utf-8 byte and a corresponding list of unicode strings.
    The reversible bpe codes work on unicode strings.
    This means you need a large # of unicode characters in your vocab if you want to avoid UNKs.
    When you're at something like a 10B token dataset you end up needing around 5K for decent coverage.
    This is a signficant percentage of your normal, say, 32K bpe vocab.
    To avoid that, we want lookup tables between utf-8 bytes and unicode strings.
    And avoids mapping to whitespace/control characters the bpe code barfs on.
    """
    bs = list(range(ord("!"), ord("~")+1))+list(range(ord("¡"), ord("¬")+1))+list(range(ord("®"), ord("ÿ")+1))
    cs = bs[:]
    n = 0
    for b in range(2**8):
        if b not in bs:
            bs.append(b)
            cs.append(2**8+n)
            n += 1
    cs = [chr(n) for n in cs]
    return dict(zip(bs, cs))


def get_pairs(word):
    """Return set of symbol pairs in a word.
    Word is represented as tuple of symbols (symbols being variable-length strings).
    """
    pairs = set()
    prev_char = word[0]
    for char in word[1:]:
        pairs.add((prev_char, char))
        prev_char = char
    return pairs


def basic_clean(text):
    text = ftfy.fix_text(text)
    text = html.unescape(html.unescape(text))
    return text.strip()


def whitespace_clean(text):
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


class SimpleTokenizer(object):
    def __init__(self, bpe_path: str = default_bpe()):
        self.byte_encoder = bytes_to_unicode()
        self.byte_decoder = {v: k for k, v in self.byte_encoder.items()}
        merges = gzip.open(bpe_path).read().decode("utf-8").split('\n')
        merges = merges[1:49152-256-2+1]
        merges = [tuple(merge.split()) for merge in merges]
        vocab = list(bytes_to_unicode().values())
        vocab = vocab + [v+'</w>' for v in vocab]
        for merge in merges:
            vocab.append(''.join(merge))
        vocab.extend(['<|startoftext|>', '<|endoftext|>'])
        self.encoder = dict(zip(vocab, range(len(vocab))))
        self.decoder = {v: k for k, v in self.encoder.items()}
        self.bpe_ranks = dict(zip(merges, range(len(merges))))
        self.cache = {'<|startoftext|>': '<|startoftext|>', '<|endoftext|>': '<|endoftext|>'}
        self.pat = re.compile(r"""<\|startoftext\|>|<\|endoftext\|>|'s|'t|'re|'ve|'m|'ll|'d|[\p{L}]+|[\p{N}]|[^\s\p{L}\p{N}]+""", re.IGNORECASE)

    def bpe(self, token):
        if token in self.cache:
            return self.cache[token]
        word = tuple(token[:-1]) + ( token[-1] + '</w>',)
        pairs = get_pairs(word)

        if not pairs:
            return token+'</w>'

        while True:
            bigram = min(pairs, key = lambda pair: self.bpe_ranks.get(pair, float('inf')))
            if bigram not in self.bpe_ranks:
                break
            first, second = bigram
            new_word = []
            i = 0
            while i < len(word):
                try:
                    j = word.index(first, i)
                    new_word.extend(word[i:j])
                    i = j
                except:
                    new_word.extend(word[i:])
                    break

                if word[i] == first and i < len(word)-1 and word[i+1] == second:
                    new_word.append(first+second)
                    i += 2
                else:
                    new_word.append(word[i])
                    i += 1
            new_word = tuple(new_word)
            word = new_word
            if len(word) == 1:
                break
            else:
                pairs = get_pairs(word)
        word = ' '.join(word)
        self.cache[token] = word
        return word

    def encode(self, text):
        bpe_tokens = []
        text = whitespace_clean(basic_clean(text)).lower()
        for token in re.findall(self.pat, text):
            token = ''.join(self.byte_encoder[b] for b in token.encode('utf-8'))
            bpe_tokens.extend(self.encoder[bpe_token] for bpe_token in self.bpe(token).split(' '))
        return bpe_tokens

    def decode(self, tokens):
        text = ''.join([self.decoder[token] for token in tokens])
        text = bytearray([self.byte_decoder[c] for c in text]).decode('utf-8', errors="replace").replace('</w>', ' ')
        return text

```

# clip\model.py

```py
from collections import OrderedDict
from typing import Tuple, Union

import numpy as np
import torch
import torch.nn.functional as F
from torch import nn


class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, inplanes, planes, stride=1):
        super().__init__()

        # all conv layers have stride 1. an avgpool is performed after the second convolution when stride > 1
        self.conv1 = nn.Conv2d(inplanes, planes, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.relu1 = nn.ReLU(inplace=True)

        self.conv2 = nn.Conv2d(planes, planes, 3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.relu2 = nn.ReLU(inplace=True)

        self.avgpool = nn.AvgPool2d(stride) if stride > 1 else nn.Identity()

        self.conv3 = nn.Conv2d(planes, planes * self.expansion, 1, bias=False)
        self.bn3 = nn.BatchNorm2d(planes * self.expansion)
        self.relu3 = nn.ReLU(inplace=True)

        self.downsample = None
        self.stride = stride

        if stride > 1 or inplanes != planes * Bottleneck.expansion:
            # downsampling layer is prepended with an avgpool, and the subsequent convolution has stride 1
            self.downsample = nn.Sequential(OrderedDict([
                ("-1", nn.AvgPool2d(stride)),
                ("0", nn.Conv2d(inplanes, planes * self.expansion, 1, stride=1, bias=False)),
                ("1", nn.BatchNorm2d(planes * self.expansion))
            ]))

    def forward(self, x: torch.Tensor):
        identity = x

        out = self.relu1(self.bn1(self.conv1(x)))
        out = self.relu2(self.bn2(self.conv2(out)))
        out = self.avgpool(out)
        out = self.bn3(self.conv3(out))

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu3(out)
        return out


class AttentionPool2d(nn.Module):
    def __init__(self, spacial_dim: int, embed_dim: int, num_heads: int, output_dim: int = None):
        super().__init__()
        self.positional_embedding = nn.Parameter(torch.randn(spacial_dim ** 2 + 1, embed_dim) / embed_dim ** 0.5)
        self.k_proj = nn.Linear(embed_dim, embed_dim)
        self.q_proj = nn.Linear(embed_dim, embed_dim)
        self.v_proj = nn.Linear(embed_dim, embed_dim)
        self.c_proj = nn.Linear(embed_dim, output_dim or embed_dim)
        self.num_heads = num_heads

    def forward(self, x):
        x = x.flatten(start_dim=2).permute(2, 0, 1)  # NCHW -> (HW)NC
        x = torch.cat([x.mean(dim=0, keepdim=True), x], dim=0)  # (HW+1)NC
        x = x + self.positional_embedding[:, None, :].to(x.dtype)  # (HW+1)NC
        x, _ = F.multi_head_attention_forward(
            query=x[:1], key=x, value=x,
            embed_dim_to_check=x.shape[-1],
            num_heads=self.num_heads,
            q_proj_weight=self.q_proj.weight,
            k_proj_weight=self.k_proj.weight,
            v_proj_weight=self.v_proj.weight,
            in_proj_weight=None,
            in_proj_bias=torch.cat([self.q_proj.bias, self.k_proj.bias, self.v_proj.bias]),
            bias_k=None,
            bias_v=None,
            add_zero_attn=False,
            dropout_p=0,
            out_proj_weight=self.c_proj.weight,
            out_proj_bias=self.c_proj.bias,
            use_separate_proj_weight=True,
            training=self.training,
            need_weights=False
        )
        return x.squeeze(0)


class ModifiedResNet(nn.Module):
    """
    A ResNet class that is similar to torchvision's but contains the following changes:
    - There are now 3 "stem" convolutions as opposed to 1, with an average pool instead of a max pool.
    - Performs anti-aliasing strided convolutions, where an avgpool is prepended to convolutions with stride > 1
    - The final pooling layer is a QKV attention instead of an average pool
    """

    def __init__(self, layers, output_dim, heads, input_resolution=224, width=64):
        super().__init__()
        self.output_dim = output_dim
        self.input_resolution = input_resolution

        # the 3-layer stem
        self.conv1 = nn.Conv2d(3, width // 2, kernel_size=3, stride=2, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(width // 2)
        self.relu1 = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(width // 2, width // 2, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(width // 2)
        self.relu2 = nn.ReLU(inplace=True)
        self.conv3 = nn.Conv2d(width // 2, width, kernel_size=3, padding=1, bias=False)
        self.bn3 = nn.BatchNorm2d(width)
        self.relu3 = nn.ReLU(inplace=True)
        self.avgpool = nn.AvgPool2d(2)

        # residual layers
        self._inplanes = width  # this is a *mutable* variable used during construction
        self.layer1 = self._make_layer(width, layers[0])
        self.layer2 = self._make_layer(width * 2, layers[1], stride=2)
        self.layer3 = self._make_layer(width * 4, layers[2], stride=2)
        self.layer4 = self._make_layer(width * 8, layers[3], stride=2)

        embed_dim = width * 32  # the ResNet feature dimension
        self.attnpool = AttentionPool2d(input_resolution // 32, embed_dim, heads, output_dim)

    def _make_layer(self, planes, blocks, stride=1):
        layers = [Bottleneck(self._inplanes, planes, stride)]

        self._inplanes = planes * Bottleneck.expansion
        for _ in range(1, blocks):
            layers.append(Bottleneck(self._inplanes, planes))

        return nn.Sequential(*layers)

    def forward(self, x):
        def stem(x):
            x = self.relu1(self.bn1(self.conv1(x)))
            x = self.relu2(self.bn2(self.conv2(x)))
            x = self.relu3(self.bn3(self.conv3(x)))
            x = self.avgpool(x)
            return x

        x = x.type(self.conv1.weight.dtype)
        x = stem(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.attnpool(x)

        return x


class LayerNorm(nn.LayerNorm):
    """Subclass torch's LayerNorm to handle fp16."""

    def forward(self, x: torch.Tensor):
        orig_type = x.dtype
        ret = super().forward(x.type(torch.float32))
        return ret.type(orig_type)


class QuickGELU(nn.Module):
    def forward(self, x: torch.Tensor):
        return x * torch.sigmoid(1.702 * x)


class ResidualAttentionBlock(nn.Module):
    def __init__(self, d_model: int, n_head: int, attn_mask: torch.Tensor = None):
        super().__init__()

        self.attn = nn.MultiheadAttention(d_model, n_head)
        self.ln_1 = LayerNorm(d_model)
        self.mlp = nn.Sequential(OrderedDict([
            ("c_fc", nn.Linear(d_model, d_model * 4)),
            ("gelu", QuickGELU()),
            ("c_proj", nn.Linear(d_model * 4, d_model))
        ]))
        self.ln_2 = LayerNorm(d_model)
        self.attn_mask = attn_mask

    def attention(self, x: torch.Tensor):
        self.attn_mask = self.attn_mask.to(dtype=x.dtype, device=x.device) if self.attn_mask is not None else None
        return self.attn(x, x, x, need_weights=False, attn_mask=self.attn_mask)[0]

    def forward(self, x: torch.Tensor):
        x = x + self.attention(self.ln_1(x))
        x = x + self.mlp(self.ln_2(x))
        return x


class Transformer(nn.Module):
    def __init__(self, width: int, layers: int, heads: int, attn_mask: torch.Tensor = None):
        super().__init__()
        self.width = width
        self.layers = layers
        self.resblocks = nn.Sequential(*[ResidualAttentionBlock(width, heads, attn_mask) for _ in range(layers)])

    def forward(self, x: torch.Tensor):
        return self.resblocks(x)


class VisionTransformer(nn.Module):
    def __init__(self, input_resolution: int, patch_size: int, width: int, layers: int, heads: int, output_dim: int):
        super().__init__()
        self.input_resolution = input_resolution
        self.output_dim = output_dim
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=width, kernel_size=patch_size, stride=patch_size, bias=False)

        scale = width ** -0.5
        self.class_embedding = nn.Parameter(scale * torch.randn(width))
        self.positional_embedding = nn.Parameter(scale * torch.randn((input_resolution // patch_size) ** 2 + 1, width))
        self.ln_pre = LayerNorm(width)

        self.transformer = Transformer(width, layers, heads)

        self.ln_post = LayerNorm(width)
        self.proj = nn.Parameter(scale * torch.randn(width, output_dim))

    def forward(self, x: torch.Tensor):
        x = self.conv1(x)  # shape = [*, width, grid, grid]
        x = x.reshape(x.shape[0], x.shape[1], -1)  # shape = [*, width, grid ** 2]
        x = x.permute(0, 2, 1)  # shape = [*, grid ** 2, width]
        x = torch.cat([self.class_embedding.to(x.dtype) + torch.zeros(x.shape[0], 1, x.shape[-1], dtype=x.dtype, device=x.device), x], dim=1)  # shape = [*, grid ** 2 + 1, width]
        x = x + self.positional_embedding.to(x.dtype)
        x = self.ln_pre(x)

        x = x.permute(1, 0, 2)  # NLD -> LND
        x = self.transformer(x)
        x = x.permute(1, 0, 2)  # LND -> NLD

        x = self.ln_post(x[:, 0, :])

        if self.proj is not None:
            x = x @ self.proj

        return x


class CLIP(nn.Module):
    def __init__(self,
                 embed_dim: int,
                 # vision
                 image_resolution: int,
                 vision_layers: Union[Tuple[int, int, int, int], int],
                 vision_width: int,
                 vision_patch_size: int,
                 # text
                 context_length: int,
                 vocab_size: int,
                 transformer_width: int,
                 transformer_heads: int,
                 transformer_layers: int
                 ):
        super().__init__()

        self.context_length = context_length

        if isinstance(vision_layers, (tuple, list)):
            vision_heads = vision_width * 32 // 64
            self.visual = ModifiedResNet(
                layers=vision_layers,
                output_dim=embed_dim,
                heads=vision_heads,
                input_resolution=image_resolution,
                width=vision_width
            )
        else:
            vision_heads = vision_width // 64
            self.visual = VisionTransformer(
                input_resolution=image_resolution,
                patch_size=vision_patch_size,
                width=vision_width,
                layers=vision_layers,
                heads=vision_heads,
                output_dim=embed_dim
            )

        self.transformer = Transformer(
            width=transformer_width,
            layers=transformer_layers,
            heads=transformer_heads,
            attn_mask=self.build_attention_mask()
        )

        self.vocab_size = vocab_size
        self.token_embedding = nn.Embedding(vocab_size, transformer_width)
        self.positional_embedding = nn.Parameter(torch.empty(self.context_length, transformer_width))
        self.ln_final = LayerNorm(transformer_width)

        self.text_projection = nn.Parameter(torch.empty(transformer_width, embed_dim))
        self.logit_scale = nn.Parameter(torch.ones([]) * np.log(1 / 0.07))

        self.initialize_parameters()

    def initialize_parameters(self):
        nn.init.normal_(self.token_embedding.weight, std=0.02)
        nn.init.normal_(self.positional_embedding, std=0.01)

        if isinstance(self.visual, ModifiedResNet):
            if self.visual.attnpool is not None:
                std = self.visual.attnpool.c_proj.in_features ** -0.5
                nn.init.normal_(self.visual.attnpool.q_proj.weight, std=std)
                nn.init.normal_(self.visual.attnpool.k_proj.weight, std=std)
                nn.init.normal_(self.visual.attnpool.v_proj.weight, std=std)
                nn.init.normal_(self.visual.attnpool.c_proj.weight, std=std)

            for resnet_block in [self.visual.layer1, self.visual.layer2, self.visual.layer3, self.visual.layer4]:
                for name, param in resnet_block.named_parameters():
                    if name.endswith("bn3.weight"):
                        nn.init.zeros_(param)

        proj_std = (self.transformer.width ** -0.5) * ((2 * self.transformer.layers) ** -0.5)
        attn_std = self.transformer.width ** -0.5
        fc_std = (2 * self.transformer.width) ** -0.5
        for block in self.transformer.resblocks:
            nn.init.normal_(block.attn.in_proj_weight, std=attn_std)
            nn.init.normal_(block.attn.out_proj.weight, std=proj_std)
            nn.init.normal_(block.mlp.c_fc.weight, std=fc_std)
            nn.init.normal_(block.mlp.c_proj.weight, std=proj_std)

        if self.text_projection is not None:
            nn.init.normal_(self.text_projection, std=self.transformer.width ** -0.5)

    def build_attention_mask(self):
        # lazily create causal attention mask, with full attention between the vision tokens
        # pytorch uses additive attention mask; fill with -inf
        mask = torch.empty(self.context_length, self.context_length)
        mask.fill_(float("-inf"))
        mask.triu_(1)  # zero out the lower diagonal
        return mask

    @property
    def dtype(self):
        return self.visual.conv1.weight.dtype

    def encode_image(self, image):
        return self.visual(image.type(self.dtype))

    def encode_text(self, text):
        x = self.token_embedding(text).type(self.dtype)  # [batch_size, n_ctx, d_model]

        x = x + self.positional_embedding.type(self.dtype)
        x = x.permute(1, 0, 2)  # NLD -> LND
        x = self.transformer(x)
        x = x.permute(1, 0, 2)  # LND -> NLD
        x = self.ln_final(x).type(self.dtype)

        # x.shape = [batch_size, n_ctx, transformer.width]
        # take features from the eot embedding (eot_token is the highest number in each sequence)
        x = x[torch.arange(x.shape[0]), text.argmax(dim=-1)] @ self.text_projection

        return x

    def forward(self, image, text):
        image_features = self.encode_image(image)
        text_features = self.encode_text(text)

        # normalized features
        image_features = image_features / image_features.norm(dim=1, keepdim=True)
        text_features = text_features / text_features.norm(dim=1, keepdim=True)

        # cosine similarity as logits
        logit_scale = self.logit_scale.exp()
        logits_per_image = logit_scale * image_features @ text_features.t()
        logits_per_text = logits_per_image.t()

        # shape = [global_batch_size, global_batch_size]
        return logits_per_image, logits_per_text


def convert_weights(model: nn.Module):
    """Convert applicable model parameters to fp16"""

    def _convert_weights_to_fp16(l):
        if isinstance(l, (nn.Conv1d, nn.Conv2d, nn.Linear)):
            l.weight.data = l.weight.data.half()
            if l.bias is not None:
                l.bias.data = l.bias.data.half()

        if isinstance(l, nn.MultiheadAttention):
            for attr in [*[f"{s}_proj_weight" for s in ["in", "q", "k", "v"]], "in_proj_bias", "bias_k", "bias_v"]:
                tensor = getattr(l, attr)
                if tensor is not None:
                    tensor.data = tensor.data.half()

        for name in ["text_projection", "proj"]:
            if hasattr(l, name):
                attr = getattr(l, name)
                if attr is not None:
                    attr.data = attr.data.half()

    model.apply(_convert_weights_to_fp16)


def build_model(state_dict: dict):
    vit = "visual.proj" in state_dict

    if vit:
        vision_width = state_dict["visual.conv1.weight"].shape[0]
        vision_layers = len([k for k in state_dict.keys() if k.startswith("visual.") and k.endswith(".attn.in_proj_weight")])
        vision_patch_size = state_dict["visual.conv1.weight"].shape[-1]
        grid_size = round((state_dict["visual.positional_embedding"].shape[0] - 1) ** 0.5)
        image_resolution = vision_patch_size * grid_size
    else:
        counts: list = [len(set(k.split(".")[2] for k in state_dict if k.startswith(f"visual.layer{b}"))) for b in [1, 2, 3, 4]]
        vision_layers = tuple(counts)
        vision_width = state_dict["visual.layer1.0.conv1.weight"].shape[0]
        output_width = round((state_dict["visual.attnpool.positional_embedding"].shape[0] - 1) ** 0.5)
        vision_patch_size = None
        assert output_width ** 2 + 1 == state_dict["visual.attnpool.positional_embedding"].shape[0]
        image_resolution = output_width * 32

    embed_dim = state_dict["text_projection"].shape[1]
    context_length = state_dict["positional_embedding"].shape[0]
    vocab_size = state_dict["token_embedding.weight"].shape[0]
    transformer_width = state_dict["ln_final.weight"].shape[0]
    transformer_heads = transformer_width // 64
    transformer_layers = len(set(k.split(".")[2] for k in state_dict if k.startswith("transformer.resblocks")))

    model = CLIP(
        embed_dim,
        image_resolution, vision_layers, vision_width, vision_patch_size,
        context_length, vocab_size, transformer_width, transformer_heads, transformer_layers
    )

    for key in ["input_resolution", "context_length", "vocab_size"]:
        if key in state_dict:
            del state_dict[key]

    convert_weights(model)
    model.load_state_dict(state_dict)
    return model.eval()

```

# clip\clipseg.py

```py
import math
from os.path import basename, dirname, join, isfile
import torch
from torch import nn
from torch.nn import functional as nnf
from torch.nn.modules.activation import ReLU


def get_prompt_list(prompt):
    if prompt == 'plain':
        return ['{}']    
    elif prompt == 'fixed':
        return ['a photo of a {}.']
    elif prompt == 'shuffle':
        return ['a photo of a {}.', 'a photograph of a {}.', 'an image of a {}.', '{}.']
    elif prompt == 'shuffle+':
        return ['a photo of a {}.', 'a photograph of a {}.', 'an image of a {}.', '{}.',
                            'a cropped photo of a {}.', 'a good photo of a {}.', 'a photo of one {}.',
                            'a bad photo of a {}.', 'a photo of the {}.']
    else:
        raise ValueError('Invalid value for prompt')        


def forward_multihead_attention(x, b, with_aff=False, attn_mask=None):
    """ 
    Simplified version of multihead attention (taken from torch source code but without tons of if clauses). 
    The mlp and layer norm come from CLIP.
    x: input.
    b: multihead attention module. 
    """

    x_ = b.ln_1(x)
    q, k, v = nnf.linear(x_, b.attn.in_proj_weight, b.attn.in_proj_bias).chunk(3, dim=-1)
    tgt_len, bsz, embed_dim = q.size()

    head_dim = embed_dim // b.attn.num_heads
    scaling = float(head_dim) ** -0.5

    q = q.contiguous().view(tgt_len, bsz * b.attn.num_heads, b.attn.head_dim).transpose(0, 1)
    k = k.contiguous().view(-1, bsz * b.attn.num_heads, b.attn.head_dim).transpose(0, 1)
    v = v.contiguous().view(-1, bsz * b.attn.num_heads, b.attn.head_dim).transpose(0, 1)

    q = q * scaling

    attn_output_weights = torch.bmm(q, k.transpose(1, 2)) #  n_heads * batch_size, tokens^2, tokens^2
    if attn_mask is not None:


        attn_mask_type, attn_mask = attn_mask
        n_heads = attn_output_weights.size(0) // attn_mask.size(0)
        attn_mask = attn_mask.repeat(n_heads, 1)
        
        if attn_mask_type == 'cls_token':
            # the mask only affects similarities compared to the readout-token.
            attn_output_weights[:, 0, 1:] = attn_output_weights[:, 0, 1:] * attn_mask[None,...]
            # attn_output_weights[:, 0, 0] = 0*attn_output_weights[:, 0, 0]

        if attn_mask_type == 'all':
            # print(attn_output_weights.shape, attn_mask[:, None].shape)
            attn_output_weights[:, 1:, 1:] = attn_output_weights[:, 1:, 1:] * attn_mask[:, None]
        
    
    attn_output_weights = torch.softmax(attn_output_weights, dim=-1)

    attn_output = torch.bmm(attn_output_weights, v)
    attn_output = attn_output.transpose(0, 1).contiguous().view(tgt_len, bsz, embed_dim)
    attn_output = b.attn.out_proj(attn_output)

    x = x + attn_output
    x = x + b.mlp(b.ln_2(x))

    if with_aff:
        return x, attn_output_weights
    else:
        return x


class CLIPDenseBase(nn.Module):

    def __init__(self, version, reduce_cond, reduce_dim, prompt, n_tokens):
        super().__init__()

        import clip

        # prec = torch.FloatTensor
        self.clip_model, _ = clip.load(version, device='cpu', jit=False)
        self.model = self.clip_model.visual

        # if not None, scale conv weights such that we obtain n_tokens.
        self.n_tokens = n_tokens

        for p in self.clip_model.parameters():
            p.requires_grad_(False)

        # conditional
        if reduce_cond is not None:
            self.reduce_cond = nn.Linear(512, reduce_cond)
            for p in self.reduce_cond.parameters():
                p.requires_grad_(False)
        else:
            self.reduce_cond = None        

        self.film_mul = nn.Linear(512 if reduce_cond is None else reduce_cond, reduce_dim)
        self.film_add = nn.Linear(512 if reduce_cond is None else reduce_cond, reduce_dim)
        
        self.reduce = nn.Linear(768, reduce_dim)

        self.prompt_list = get_prompt_list(prompt)     

        # precomputed prompts
        import pickle
        if isfile('precomputed_prompt_vectors.pickle'):
            precomp = pickle.load(open('precomputed_prompt_vectors.pickle', 'rb'))
            self.precomputed_prompts = {k: torch.from_numpy(v) for k, v in precomp.items()}        
        else:
            self.precomputed_prompts = dict()
    
    def rescaled_pos_emb(self, new_size):
        assert len(new_size) == 2

        a = self.model.positional_embedding[1:].T.view(1, 768, *self.token_shape)
        b = nnf.interpolate(a, new_size, mode='bicubic', align_corners=False).squeeze(0).view(768, new_size[0]*new_size[1]).T
        return torch.cat([self.model.positional_embedding[:1], b])

    def visual_forward(self, x_inp, extract_layers=(), skip=False, mask=None):
        

        with torch.no_grad():

            inp_size = x_inp.shape[2:]

            if self.n_tokens is not None:
                stride2 = x_inp.shape[2] // self.n_tokens
                conv_weight2 = nnf.interpolate(self.model.conv1.weight, (stride2, stride2), mode='bilinear', align_corners=True)
                x = nnf.conv2d(x_inp, conv_weight2, bias=self.model.conv1.bias, stride=stride2, dilation=self.model.conv1.dilation)
            else:
                x = self.model.conv1(x_inp)  # shape = [*, width, grid, grid]

            x = x.reshape(x.shape[0], x.shape[1], -1)  # shape = [*, width, grid ** 2]
            x = x.permute(0, 2, 1)  # shape = [*, grid ** 2, width]

            x = torch.cat([self.model.class_embedding.to(x.dtype) + torch.zeros(x.shape[0], 1, x.shape[-1], dtype=x.dtype, device=x.device), x], dim=1)  # shape = [*, grid ** 2 + 1, width]

            standard_n_tokens = 50 if self.model.conv1.kernel_size[0] == 32 else 197

            if x.shape[1] != standard_n_tokens:
                new_shape = int(math.sqrt(x.shape[1]-1))
                x = x + self.rescaled_pos_emb((new_shape, new_shape)).to(x.dtype)[None,:,:]
            else:
                x = x + self.model.positional_embedding.to(x.dtype)

            x = self.model.ln_pre(x)

            x = x.permute(1, 0, 2)  # NLD -> LND

            activations, affinities = [], []
            for i, res_block in enumerate(self.model.transformer.resblocks):
                
                if mask is not None:
                    mask_layer, mask_type, mask_tensor = mask
                    if mask_layer == i or mask_layer == 'all':
                        # import ipdb; ipdb.set_trace()
                        size = int(math.sqrt(x.shape[0] - 1))
                        
                        attn_mask = (mask_type, nnf.interpolate(mask_tensor.unsqueeze(1).float(), (size, size)).view(mask_tensor.shape[0], size * size))
                        
                    else:
                        attn_mask = None
                else:
                    attn_mask = None

                x, aff_per_head = forward_multihead_attention(x, res_block, with_aff=True, attn_mask=attn_mask)

                if i in extract_layers:
                    affinities += [aff_per_head]

                    #if self.n_tokens is not None:
                    #    activations += [nnf.interpolate(x, inp_size, mode='bilinear', align_corners=True)]
                    #else:
                    activations += [x]

                if len(extract_layers) > 0 and i == max(extract_layers) and skip:
                    print('early skip')
                    break
                
            x = x.permute(1, 0, 2)  # LND -> NLD
            x = self.model.ln_post(x[:, 0, :])

            if self.model.proj is not None:
                x = x @ self.model.proj

            return x, activations, affinities

    def sample_prompts(self, words, prompt_list=None):

        prompt_list = prompt_list if prompt_list is not None else self.prompt_list

        prompt_indices = torch.multinomial(torch.ones(len(prompt_list)), len(words), replacement=True)
        prompts = [prompt_list[i] for i in prompt_indices]
        return [promt.format(w) for promt, w in zip(prompts, words)]

    def get_cond_vec(self, conditional, batch_size):
        # compute conditional from a single string
        if conditional is not None and type(conditional) == str:
            cond = self.compute_conditional(conditional)
            cond = cond.repeat(batch_size, 1)

        # compute conditional from string list/tuple
        elif conditional is not None and type(conditional) in {list, tuple} and type(conditional[0]) == str:
            assert len(conditional) == batch_size
            cond = self.compute_conditional(conditional)

        # use conditional directly
        elif conditional is not None and type(conditional) == torch.Tensor and conditional.ndim == 2:
            cond = conditional

        # compute conditional from image
        elif conditional is not None and type(conditional) == torch.Tensor:
            with torch.no_grad():
                cond, _, _ = self.visual_forward(conditional)
        else:
            raise ValueError('invalid conditional')
        return cond   

    def compute_conditional(self, conditional):
        import clip

        dev = next(self.parameters()).device

        if type(conditional) in {list, tuple}:
            text_tokens = clip.tokenize(conditional).to(dev)
            cond = self.clip_model.encode_text(text_tokens)
        else:
            if conditional in self.precomputed_prompts:
                cond = self.precomputed_prompts[conditional].float().to(dev)
            else:
                text_tokens = clip.tokenize([conditional]).to(dev)
                cond = self.clip_model.encode_text(text_tokens)[0]
        
        if self.shift_vector is not None:
            return cond + self.shift_vector
        else:
            return cond


def clip_load_untrained(version):
    assert version == 'ViT-B/16'
    from clip.model import CLIP
    from clip.clip import _MODELS, _download
    model = torch.jit.load(_download(_MODELS['ViT-B/16'])).eval()
    state_dict = model.state_dict()

    vision_width = state_dict["visual.conv1.weight"].shape[0]
    vision_layers = len([k for k in state_dict.keys() if k.startswith("visual.") and k.endswith(".attn.in_proj_weight")])
    vision_patch_size = state_dict["visual.conv1.weight"].shape[-1]
    grid_size = round((state_dict["visual.positional_embedding"].shape[0] - 1) ** 0.5)
    image_resolution = vision_patch_size * grid_size
    embed_dim = state_dict["text_projection"].shape[1]
    context_length = state_dict["positional_embedding"].shape[0]
    vocab_size = state_dict["token_embedding.weight"].shape[0]
    transformer_width = state_dict["ln_final.weight"].shape[0]
    transformer_heads = transformer_width // 64
    transformer_layers = len(set(k.split(".")[2] for k in state_dict if k.startswith(f"transformer.resblocks")))

    return CLIP(embed_dim, image_resolution, vision_layers, vision_width, vision_patch_size, 
        context_length, vocab_size, transformer_width, transformer_heads, transformer_layers)    


class CLIPDensePredT(CLIPDenseBase):

    def __init__(self, version='ViT-B/32', extract_layers=(3, 6, 9), cond_layer=0, reduce_dim=128, n_heads=4, prompt='fixed', 
                 extra_blocks=0, reduce_cond=None, fix_shift=False,
                 learn_trans_conv_only=False,  limit_to_clip_only=False, upsample=False, 
                 add_calibration=False, rev_activations=False, trans_conv=None, n_tokens=None, complex_trans_conv=False):
        
        super().__init__(version, reduce_cond, reduce_dim, prompt, n_tokens)
        # device = 'cpu'

        self.extract_layers = extract_layers
        self.cond_layer = cond_layer
        self.limit_to_clip_only = limit_to_clip_only
        self.process_cond = None
        self.rev_activations = rev_activations
        
        depth = len(extract_layers)

        if add_calibration:
            self.calibration_conds = 1

        self.upsample_proj = nn.Conv2d(reduce_dim, 1, kernel_size=1) if upsample else None

        self.add_activation1 = True

        self.version = version
        
        self.token_shape = {'ViT-B/32': (7, 7), 'ViT-B/16': (14, 14)}[version]

        if fix_shift:
            # self.shift_vector = nn.Parameter(torch.load(join(dirname(basename(__file__)), 'clip_text_shift_vector.pth')), requires_grad=False)
            self.shift_vector = nn.Parameter(torch.load(join(dirname(basename(__file__)), 'shift_text_to_vis.pth')), requires_grad=False)
            # self.shift_vector = nn.Parameter(-1*torch.load(join(dirname(basename(__file__)), 'shift2.pth')), requires_grad=False)
        else:
            self.shift_vector = None

        if trans_conv is None:
            trans_conv_ks = {'ViT-B/32': (32, 32), 'ViT-B/16': (16, 16)}[version]
        else:
            # explicitly define transposed conv kernel size
            trans_conv_ks = (trans_conv, trans_conv)

        if not complex_trans_conv:
            self.trans_conv = nn.ConvTranspose2d(reduce_dim, 1, trans_conv_ks, stride=trans_conv_ks)
        else:
            assert trans_conv_ks[0] == trans_conv_ks[1]

            tp_kernels = (trans_conv_ks[0] // 4, trans_conv_ks[0] // 4)

            self.trans_conv = nn.Sequential(
                nn.Conv2d(reduce_dim, reduce_dim, kernel_size=3, padding=1),
                nn.ReLU(),
                nn.ConvTranspose2d(reduce_dim, reduce_dim // 2, kernel_size=tp_kernels[0], stride=tp_kernels[0]),
                nn.ReLU(),
                nn.ConvTranspose2d(reduce_dim // 2, 1, kernel_size=tp_kernels[1], stride=tp_kernels[1]),               
            )

#        self.trans_conv = nn.ConvTranspose2d(reduce_dim, 1, trans_conv_ks, stride=trans_conv_ks)
        
        assert len(self.extract_layers) == depth

        self.reduces = nn.ModuleList([nn.Linear(768, reduce_dim) for _ in range(depth)])
        self.blocks = nn.ModuleList([nn.TransformerEncoderLayer(d_model=reduce_dim, nhead=n_heads) for _ in range(len(self.extract_layers))])
        self.extra_blocks = nn.ModuleList([nn.TransformerEncoderLayer(d_model=reduce_dim, nhead=n_heads) for _ in range(extra_blocks)])
        
        # refinement and trans conv

        if learn_trans_conv_only:
            for p in self.parameters():
                p.requires_grad_(False)
            
            for p in self.trans_conv.parameters():
                p.requires_grad_(True)

        self.prompt_list = get_prompt_list(prompt)


    def forward(self, inp_image, conditional=None, return_features=False, mask=None):

        assert type(return_features) == bool

        inp_image = inp_image.to(self.model.positional_embedding.device)

        if mask is not None:
            raise ValueError('mask not supported')

        # x_inp = normalize(inp_image)
        x_inp = inp_image

        bs, dev = inp_image.shape[0], x_inp.device

        cond = self.get_cond_vec(conditional, bs)

        visual_q, activations, _ = self.visual_forward(x_inp, extract_layers=[0] + list(self.extract_layers))

        activation1 = activations[0]
        activations = activations[1:]

        _activations = activations[::-1] if not self.rev_activations else activations

        a = None
        for i, (activation, block, reduce) in enumerate(zip(_activations, self.blocks, self.reduces)):
            
            if a is not None:
                a = reduce(activation) + a
            else:
                a = reduce(activation)

            if i == self.cond_layer:
                if self.reduce_cond is not None:
                    cond = self.reduce_cond(cond)
                
                a = self.film_mul(cond) * a + self.film_add(cond)

            a = block(a)

        for block in self.extra_blocks:
            a = a + block(a)

        a = a[1:].permute(1, 2, 0) # rm cls token and -> BS, Feats, Tokens

        size = int(math.sqrt(a.shape[2]))

        a = a.view(bs, a.shape[1], size, size)

        a = self.trans_conv(a)

        if self.n_tokens is not None:
            a = nnf.interpolate(a, x_inp.shape[2:], mode='bilinear', align_corners=True) 

        if self.upsample_proj is not None:
            a = self.upsample_proj(a)
            a = nnf.interpolate(a, x_inp.shape[2:], mode='bilinear')

        if return_features:
            return a, visual_q, cond, [activation1] + activations
        else:
            return a,



class CLIPDensePredTMasked(CLIPDensePredT):

    def __init__(self, version='ViT-B/32', extract_layers=(3, 6, 9), cond_layer=0, reduce_dim=128, n_heads=4, 
                 prompt='fixed', extra_blocks=0, reduce_cond=None, fix_shift=False, learn_trans_conv_only=False, 
                 refine=None, limit_to_clip_only=False, upsample=False, add_calibration=False, n_tokens=None):

        super().__init__(version=version, extract_layers=extract_layers, cond_layer=cond_layer, reduce_dim=reduce_dim, 
                         n_heads=n_heads, prompt=prompt, extra_blocks=extra_blocks, reduce_cond=reduce_cond, 
                         fix_shift=fix_shift, learn_trans_conv_only=learn_trans_conv_only,
                         limit_to_clip_only=limit_to_clip_only, upsample=upsample, add_calibration=add_calibration,
                         n_tokens=n_tokens)

    def visual_forward_masked(self, img_s, seg_s):
        return super().visual_forward(img_s, mask=('all', 'cls_token', seg_s))

    def forward(self, img_q, cond_or_img_s, seg_s=None, return_features=False):

        if seg_s is None:
            cond = cond_or_img_s
        else:
            img_s = cond_or_img_s

            with torch.no_grad():
                cond, _, _ = self.visual_forward_masked(img_s, seg_s)

        return super().forward(img_q, cond, return_features=return_features)



class CLIPDenseBaseline(CLIPDenseBase):

    def __init__(self, version='ViT-B/32', cond_layer=0, 
                extract_layer=9, reduce_dim=128, reduce2_dim=None, prompt='fixed', 
                 reduce_cond=None, limit_to_clip_only=False, n_tokens=None):
        
        super().__init__(version, reduce_cond, reduce_dim, prompt, n_tokens)
        device = 'cpu'

        # self.cond_layer = cond_layer
        self.extract_layer = extract_layer
        self.limit_to_clip_only = limit_to_clip_only
        self.shift_vector = None

        self.token_shape = {'ViT-B/32': (7, 7), 'ViT-B/16': (14, 14)}[version]
        
        assert reduce2_dim is not None

        self.reduce2 = nn.Sequential(
            nn.Linear(reduce_dim, reduce2_dim),
            nn.ReLU(),
            nn.Linear(reduce2_dim, reduce_dim)
        )
        
        trans_conv_ks = {'ViT-B/32': (32, 32), 'ViT-B/16': (16, 16)}[version]
        self.trans_conv = nn.ConvTranspose2d(reduce_dim, 1, trans_conv_ks, stride=trans_conv_ks)


    def forward(self, inp_image, conditional=None, return_features=False):

        inp_image = inp_image.to(self.model.positional_embedding.device)

        # x_inp = normalize(inp_image)
        x_inp = inp_image

        bs, dev = inp_image.shape[0], x_inp.device

        cond = self.get_cond_vec(conditional, bs)

        visual_q, activations, affinities = self.visual_forward(x_inp, extract_layers=[self.extract_layer])

        a = activations[0]
        a = self.reduce(a)
        a = self.film_mul(cond) * a + self.film_add(cond)

        if self.reduce2 is not None:
            a = self.reduce2(a)

        # the original model would execute a transformer block here

        a = a[1:].permute(1, 2, 0) # rm cls token and -> BS, Feats, Tokens

        size = int(math.sqrt(a.shape[2]))

        a = a.view(bs, a.shape[1], size, size)
        a = self.trans_conv(a)

        if return_features:
            return a, visual_q, cond, activations
        else:
            return a,


class CLIPSegMultiLabel(nn.Module):

    def __init__(self, model) -> None:
        super().__init__()

        from third_party.JoEm.data_loader import get_seen_idx, get_unseen_idx, VOC

        self.pascal_classes = VOC

        from clip.clipseg import CLIPDensePredT
        from general_utils import load_model
        # self.clipseg = load_model('rd64-vit16-neg0.2-phrasecut', strict=False)
        self.clipseg = load_model(model, strict=False)
        
        self.clipseg.eval()

    def forward(self, x):

        bs = x.shape[0]
        out = torch.ones(21, bs, 352, 352).to(x.device) * -10

        for class_id, class_name in enumerate(self.pascal_classes):
        
            fac = 3 if class_name == 'background' else 1

            with torch.no_grad():
                pred = torch.sigmoid(self.clipseg(x, class_name)[0][:,0]) * fac

            out[class_id] += pred


        out = out.permute(1, 0, 2, 3)

        return out

        # construct output tensor
                    

```

# clip\clip.py

```py
import hashlib
import os
import urllib
import warnings
from typing import Any, Union, List

import torch
from PIL import Image
from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize
from tqdm import tqdm

from .model import build_model
from .simple_tokenizer import SimpleTokenizer as _Tokenizer

try:
    from torchvision.transforms import InterpolationMode
    BICUBIC = InterpolationMode.BICUBIC
except ImportError:
    BICUBIC = Image.BICUBIC



__all__ = ["available_models", "load", "tokenize"]
_tokenizer = _Tokenizer()

_MODELS = {
    "RN50": "https://openaipublic.azureedge.net/clip/models/afeb0e10f9e5a86da6080e35cf09123aca3b358a0c3e3b6c78a7b63bc04b6762/RN50.pt",
    "RN101": "https://openaipublic.azureedge.net/clip/models/8fa8567bab74a42d41c5915025a8e4538c3bdbe8804a470a72f30b0d94fab599/RN101.pt",
    "RN50x4": "https://openaipublic.azureedge.net/clip/models/7e526bd135e493cef0776de27d5f42653e6b4c8bf9e0f653bb11773263205fdd/RN50x4.pt",
    "RN50x16": "https://openaipublic.azureedge.net/clip/models/52378b407f34354e150460fe41077663dd5b39c54cd0bfd2b27167a4a06ec9aa/RN50x16.pt",
    "RN50x64": "https://openaipublic.azureedge.net/clip/models/be1cfb55d75a9666199fb2206c106743da0f6468c9d327f3e0d0a543a9919d9c/RN50x64.pt",
    "ViT-B/32": "https://openaipublic.azureedge.net/clip/models/40d365715913c9da98579312b702a82c18be219cc2a73407c4526f58eba950af/ViT-B-32.pt",
    "ViT-B/16": "https://openaipublic.azureedge.net/clip/models/5806e77cd80f8b59890b7e101eabd078d9fb84e6937f9e85e4ecb61988df416f/ViT-B-16.pt",
    "ViT-L/14": "https://openaipublic.azureedge.net/clip/models/b8cca3fd41ae0c99ba7e8951adf17d267cdb84cd88be6f7c2e0eca1737a03836/ViT-L-14.pt",
    "ViT-L/14@336px": "https://openaipublic.azureedge.net/clip/models/3035c92b350959924f9f00213499208652fc7ea050643e8b385c2dac08641f02/ViT-L-14-336px.pt",
}


def _download(url: str, root: str):
    os.makedirs(root, exist_ok=True)
    filename = os.path.basename(url)

    expected_sha256 = url.split("/")[-2]
    download_target = os.path.join(root, filename)

    if os.path.exists(download_target) and not os.path.isfile(download_target):
        raise RuntimeError(f"{download_target} exists and is not a regular file")

    if os.path.isfile(download_target):
        if hashlib.sha256(open(download_target, "rb").read()).hexdigest() == expected_sha256:
            return download_target
        else:
            warnings.warn(f"{download_target} exists, but the SHA256 checksum does not match; re-downloading the file")

    with urllib.request.urlopen(url) as source, open(download_target, "wb") as output:
        with tqdm(total=int(source.info().get("Content-Length")), ncols=80, unit='iB', unit_scale=True, unit_divisor=1024) as loop:
            while True:
                buffer = source.read(8192)
                if not buffer:
                    break

                output.write(buffer)
                loop.update(len(buffer))

    if hashlib.sha256(open(download_target, "rb").read()).hexdigest() != expected_sha256:
        raise RuntimeError("Model has been downloaded but the SHA256 checksum does not not match")

    return download_target


def _convert_image_to_rgb(image):
    return image.convert("RGB")


def _transform(n_px):
    return Compose([
        Resize(n_px, interpolation=BICUBIC),
        CenterCrop(n_px),
        _convert_image_to_rgb,
        ToTensor(),
        Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711)),
    ])


def available_models() -> List[str]:
    """Returns the names of available CLIP models"""
    return list(_MODELS.keys())


def load(name: str, device: Union[str, torch.device] = "cuda" if torch.cuda.is_available() else "cpu", jit: bool = False, download_root: str = None):
    """Load a CLIP model

    Parameters
    ----------
    name : str
        A model name listed by `clip.available_models()`, or the path to a model checkpoint containing the state_dict

    device : Union[str, torch.device]
        The device to put the loaded model

    jit : bool
        Whether to load the optimized JIT model or more hackable non-JIT model (default).

    download_root: str
        path to download the model files; by default, it uses "~/.cache/clip"

    Returns
    -------
    model : torch.nn.Module
        The CLIP model

    preprocess : Callable[[PIL.Image], torch.Tensor]
        A torchvision transform that converts a PIL image into a tensor that the returned model can take as its input
    """
    if name in _MODELS:
        model_path = _download(_MODELS[name], download_root or os.path.expanduser("~/.cache/clip"))
    elif os.path.isfile(name):
        model_path = name
    else:
        raise RuntimeError(f"Model {name} not found; available models = {available_models()}")

    with open(model_path, 'rb') as opened_file:
        try:
            # loading JIT archive
            model = torch.jit.load(opened_file, map_location=device if jit else "cpu").eval()
            state_dict = None
        except RuntimeError:
            # loading saved state dict
            if jit:
                warnings.warn(f"File {model_path} is not a JIT archive. Loading as a state dict instead")
                jit = False
            state_dict = torch.load(opened_file, map_location="cpu")

    if not jit:
        model = build_model(state_dict or model.state_dict()).to(device)
        if str(device) == "cpu":
            model.float()
        return model, _transform(model.visual.input_resolution)

    # patch the device names
    device_holder = torch.jit.trace(lambda: torch.ones([]).to(torch.device(device)), example_inputs=[])
    device_node = [n for n in device_holder.graph.findAllNodes("prim::Constant") if "Device" in repr(n)][-1]

    def _node_get(node: torch._C.Node, key: str):
        """Gets attributes of a node which is polymorphic over return type.
        
        From https://github.com/pytorch/pytorch/pull/82628
        """
        sel = node.kindOf(key)
        return getattr(node, sel)(key)

    def patch_device(module):
        try:
            graphs = [module.graph] if hasattr(module, "graph") else []
        except RuntimeError:
            graphs = []

        if hasattr(module, "forward1"):
            graphs.append(module.forward1.graph)

        for graph in graphs:
            for node in graph.findAllNodes("prim::Constant"):
                if "value" in node.attributeNames() and str(_node_get(node, "value")).startswith("cuda"):
                    node.copyAttributes(device_node)

    model.apply(patch_device)
    patch_device(model.encode_image)
    patch_device(model.encode_text)

    # patch dtype to float32 on CPU
    if str(device) == "cpu":
        float_holder = torch.jit.trace(lambda: torch.ones([]).float(), example_inputs=[])
        float_input = list(float_holder.graph.findNode("aten::to").inputs())[1]
        float_node = float_input.node()

        def patch_float(module):
            try:
                graphs = [module.graph] if hasattr(module, "graph") else []
            except RuntimeError:
                graphs = []

            if hasattr(module, "forward1"):
                graphs.append(module.forward1.graph)

            for graph in graphs:
                for node in graph.findAllNodes("aten::to"):
                    inputs = list(node.inputs())
                    for i in [1, 2]:  # dtype can be the second or third argument to aten::to()
                        if _node_get(inputs[i].node(), "value") == 5:
                            inputs[i].node().copyAttributes(float_node)

        model.apply(patch_float)
        patch_float(model.encode_image)
        patch_float(model.encode_text)

        model.float()

    return model, _transform(model.input_resolution.item())


def tokenize(texts: Union[str, List[str]], context_length: int = 77, truncate: bool = False) -> Union[torch.IntTensor, torch.LongTensor]:
    """
    Returns the tokenized representation of given input string(s)

    Parameters
    ----------
    texts : Union[str, List[str]]
        An input string or a list of input strings to tokenize

    context_length : int
        The context length to use; all CLIP models use 77 as the context length

    truncate: bool
        Whether to truncate the text in case its encoding is longer than the context length

    Returns
    -------
    A two-dimensional tensor containing the resulting tokens, shape = [number of input strings, context_length].
    We return LongTensor when torch version is <1.8.0, since older index_select requires indices to be long.
    """
    if isinstance(texts, str):
        texts = [texts]

    sot_token = _tokenizer.encoder["<|startoftext|>"]
    eot_token = _tokenizer.encoder["<|endoftext|>"]
    all_tokens = [[sot_token] + _tokenizer.encode(text) + [eot_token] for text in texts]
    #if packaging.version.parse(torch.__version__) < packaging.version.parse("1.8.0"):
    #    result = torch.zeros(len(all_tokens), context_length, dtype=torch.long)
    #else:
    result = torch.zeros(len(all_tokens), context_length, dtype=torch.int)

    for i, tokens in enumerate(all_tokens):
        if len(tokens) > context_length:
            if truncate:
                tokens = tokens[:context_length]
                tokens[-1] = eot_token
            else:
                raise RuntimeError(f"Input {texts[i]} is too long for context length {context_length}")
        result[i, :len(tokens)] = torch.tensor(tokens)

    return result

```

# clip\bpe_simple_vocab_16e6.txt.gz

This is a binary file of the type: Binary

# ui\tabs\settings_tab.py

```py
import shutil
import os
import gradio as gr
import roop.globals
import ui.globals
from roop.utilities import clean_dir

available_themes = ["Default", "gradio/glass", "gradio/monochrome", "gradio/seafoam", "gradio/soft", "gstaff/xkcd", "freddyaboulton/dracula_revamped", "ysharma/steampunk"]
image_formats = ['jpg','png', 'webp']
video_formats = ['avi','mkv', 'mp4', 'webm']
video_codecs = ['libx264', 'libx265', 'libvpx-vp9', 'h264_nvenc', 'hevc_nvenc']
providerlist = None

settings_controls = []

def settings_tab():
    from roop.core import suggest_execution_providers
    global providerlist

    providerlist = suggest_execution_providers()
    with gr.Tab("⚙ Settings"):
        with gr.Row():
            with gr.Column():
                themes = gr.Dropdown(available_themes, label="Theme", info="Change needs complete restart", value=roop.globals.CFG.selected_theme)
            with gr.Column():
                settings_controls.append(gr.Checkbox(label="Public Server", value=roop.globals.CFG.server_share, elem_id='server_share', interactive=True))
                settings_controls.append(gr.Checkbox(label='Clear output folder before each run', value=roop.globals.CFG.clear_output, elem_id='clear_output', interactive=True))
                output_template = gr.Textbox(label="Filename Output Template", info="(file extension is added automatically)", lines=1, placeholder='{file}_{time}', value=roop.globals.CFG.output_template)
            with gr.Column():
                input_server_name = gr.Textbox(label="Server Name", lines=1, info="Leave blank to run locally", value=roop.globals.CFG.server_name)
            with gr.Column():
                input_server_port = gr.Number(label="Server Port", precision=0, info="Leave at 0 to use default", value=roop.globals.CFG.server_port)
        with gr.Row():
            with gr.Column():
                settings_controls.append(gr.Dropdown(providerlist, label="Provider", value=roop.globals.CFG.provider, elem_id='provider', interactive=True))
                chk_det_size = gr.Checkbox(label="Use default Det-Size", value=True, elem_id='default_det_size', interactive=True)
                settings_controls.append(gr.Checkbox(label="Force CPU for Face Analyser", value=roop.globals.CFG.force_cpu, elem_id='force_cpu', interactive=True))
                max_threads = gr.Slider(1, 32, value=roop.globals.CFG.max_threads, label="Max. Number of Threads", info='default: 3', step=1.0, interactive=True)
            with gr.Column():
                memory_limit = gr.Slider(0, 128, value=roop.globals.CFG.memory_limit, label="Max. Memory to use (Gb)", info='0 meaning no limit', step=1.0, interactive=True)
                settings_controls.append(gr.Dropdown(image_formats, label="Image Output Format", info='default: png', value=roop.globals.CFG.output_image_format, elem_id='output_image_format', interactive=True))
            with gr.Column():
                settings_controls.append(gr.Dropdown(video_codecs, label="Video Codec", info='default: libx264', value=roop.globals.CFG.output_video_codec, elem_id='output_video_codec', interactive=True))
                settings_controls.append(gr.Dropdown(video_formats, label="Video Output Format", info='default: mp4', value=roop.globals.CFG.output_video_format, elem_id='output_video_format', interactive=True))
                video_quality = gr.Slider(0, 100, value=roop.globals.CFG.video_quality, label="Video Quality (crf)", info='default: 14', step=1.0, interactive=True)
            with gr.Column():
                with gr.Group():
                    settings_controls.append(gr.Checkbox(label='Use OS temp folder', value=roop.globals.CFG.use_os_temp_folder, elem_id='use_os_temp_folder', interactive=True))
                    settings_controls.append(gr.Checkbox(label='Show video in browser (re-encodes output)', value=roop.globals.CFG.output_show_video, elem_id='output_show_video', interactive=True))
                button_apply_restart = gr.Button("Restart Server", variant='primary')
                button_clean_temp = gr.Button("Clean temp folder")
                button_apply_settings = gr.Button("Apply Settings")

    chk_det_size.select(fn=on_option_changed)

    # Settings
    for s in settings_controls:
        s.select(fn=on_settings_changed)
    max_threads.input(fn=lambda a,b='max_threads':on_settings_changed_misc(a,b), inputs=[max_threads])
    memory_limit.input(fn=lambda a,b='memory_limit':on_settings_changed_misc(a,b), inputs=[memory_limit])
    video_quality.input(fn=lambda a,b='video_quality':on_settings_changed_misc(a,b), inputs=[video_quality])

    # button_clean_temp.click(fn=clean_temp, outputs=[bt_srcfiles, input_faces, target_faces, bt_destfiles])
    button_clean_temp.click(fn=clean_temp)
    button_apply_settings.click(apply_settings, inputs=[themes, input_server_name, input_server_port, output_template])
    button_apply_restart.click(restart)


def on_option_changed(evt: gr.SelectData):
    attribname = evt.target.elem_id
    if isinstance(evt.target, gr.Checkbox):
        if hasattr(roop.globals, attribname):
            setattr(roop.globals, attribname, evt.selected)
            return
    elif isinstance(evt.target, gr.Dropdown):
        if hasattr(roop.globals, attribname):
            setattr(roop.globals, attribname, evt.value)
            return
    raise gr.Error(f'Unhandled Setting for {evt.target}')


def on_settings_changed_misc(new_val, attribname):
    if hasattr(roop.globals.CFG, attribname):
        setattr(roop.globals.CFG, attribname, new_val)
    else:
        print("Didn't find attrib!")
        


def on_settings_changed(evt: gr.SelectData):
    attribname = evt.target.elem_id
    if isinstance(evt.target, gr.Checkbox):
        if hasattr(roop.globals.CFG, attribname):
            setattr(roop.globals.CFG, attribname, evt.selected)
            return
    elif isinstance(evt.target, gr.Dropdown):
        if hasattr(roop.globals.CFG, attribname):
            setattr(roop.globals.CFG, attribname, evt.value)
            return
            
    raise gr.Error(f'Unhandled Setting for {evt.target}')

def clean_temp():
    from ui.main import prepare_environment
    
    ui.globals.ui_input_thumbs.clear()
    roop.globals.INPUT_FACESETS.clear()
    roop.globals.TARGET_FACES.clear()
    ui.globals.ui_target_thumbs = []
    if not roop.globals.CFG.use_os_temp_folder:
        clean_dir(os.environ["TEMP"])
    prepare_environment()
    gr.Info('Temp Files removed')
    return None,None,None,None


def apply_settings(themes, input_server_name, input_server_port, output_template):
    from ui.main import show_msg

    roop.globals.CFG.selected_theme = themes
    roop.globals.CFG.server_name = input_server_name
    roop.globals.CFG.server_port = input_server_port
    roop.globals.CFG.output_template = output_template
    roop.globals.CFG.save()
    show_msg('Settings saved')


def restart():
    ui.globals.ui_restart_server = True

```

# ui\tabs\livecam_tab.py

```py
import gradio as gr
import roop.globals
import ui.globals


camera_frame = None

def livecam_tab():
    with gr.Tab("🎥 Live Cam"):
        with gr.Row(variant='panel'):
            gr.Markdown("""
                        This feature will allow you to use your physical webcam and apply the selected faces to the stream. 
                        You can also forward the stream to a virtual camera, which can be used in video calls or streaming software.<br />
                        Supported are: v4l2loopback (linux), OBS Virtual Camera (macOS/Windows) and unitycapture (Windows).<br />
                        **Please note:** to change the face or any other settings you need to stop and restart a running live cam.
            """)

        with gr.Row(variant='panel'):
            with gr.Column():
                bt_start = gr.Button("▶ Start", variant='primary')
            with gr.Column():
                bt_stop = gr.Button("⏹ Stop", variant='secondary', interactive=False)
            with gr.Column():
                camera_num = gr.Slider(0, 8, value=0, label="Camera Number", step=1.0, interactive=True)
                cb_obs = gr.Checkbox(label="Forward stream to virtual camera", interactive=True)
            with gr.Column():
                dd_reso = gr.Dropdown(choices=["640x480","1280x720", "1920x1080"], value="1280x720", label="Fake Camera Resolution", interactive=True)
                cb_xseg = gr.Checkbox(label="Use DFL Xseg masking", interactive=True, value=True)
                cb_mouthrestore = gr.Checkbox(label="Restore original mouth area", interactive=True, value=False)

        with gr.Row():
            fake_cam_image = gr.Image(label='Fake Camera Output', interactive=False, format="jpeg")

    start_event = bt_start.click(fn=start_cam,  inputs=[cb_obs, cb_xseg, cb_mouthrestore, camera_num, dd_reso, ui.globals.ui_selected_enhancer, ui.globals.ui_blend_ratio, ui.globals.ui_upscale],outputs=[bt_start, bt_stop,fake_cam_image])
    bt_stop.click(fn=stop_swap, cancels=[start_event], outputs=[bt_start, bt_stop], queue=False)


def start_cam(stream_to_obs, use_xseg, use_mouthrestore, cam, reso, enhancer, blend_ratio, upscale):
    from roop.virtualcam import start_virtual_cam
    from roop.utilities import convert_to_gradio

    roop.globals.selected_enhancer = enhancer
    roop.globals.blend_ratio = blend_ratio
    roop.globals.subsample_size = int(upscale[:3])
    start_virtual_cam(stream_to_obs, use_xseg, use_mouthrestore, cam, reso)
    while True:
        yield gr.Button(interactive=False), gr.Button(interactive=True), convert_to_gradio(ui.globals.ui_camera_frame)
        

def stop_swap():
    from roop.virtualcam import stop_virtual_cam
    stop_virtual_cam()
    return gr.Button(interactive=True), gr.Button(interactive=False)
    




```

# ui\tabs\faceswap_tab.py

```py
import os
import shutil
import pathlib
import gradio as gr
import roop.utilities as util
import roop.globals
import ui.globals
from roop.face_util import extract_face_images, create_blank_image
from roop.capturer import get_video_frame, get_video_frame_total, get_image_frame
from roop.ProcessEntry import ProcessEntry
from roop.ProcessOptions import ProcessOptions
from roop.FaceSet import FaceSet
from roop.utilities import clean_dir

last_image = None


IS_INPUT = True
SELECTED_FACE_INDEX = 0

SELECTED_INPUT_FACE_INDEX = 0
SELECTED_TARGET_FACE_INDEX = 0

input_faces = None
target_faces = None
face_selection = None
previewimage = None

selected_preview_index = 0

is_processing = False            

list_files_process : list[ProcessEntry] = []
no_face_choices = ["Use untouched original frame","Retry rotated", "Skip Frame", "Skip Frame if no similar face", "Use last swapped"]
swap_choices = ["First found", "All input faces", "All female", "All male", "All faces", "Selected face"]

current_video_fps = 50

manual_masking = False


def faceswap_tab():
    global no_face_choices, previewimage

    with gr.Tab("🎭 Face Swap"):
        with gr.Row(variant='panel'):
            with gr.Column(scale=2):
                with gr.Row():
                    input_faces = gr.Gallery(label="Input faces gallery", allow_preview=False, preview=False, height=138, columns=64, object_fit="scale-down", interactive=False)
                    target_faces = gr.Gallery(label="Target faces gallery", allow_preview=False, preview=False, height=138, columns=64, object_fit="scale-down", interactive=False)
                with gr.Row():
                    bt_move_left_input = gr.Button("⬅ Move left", size='sm')
                    bt_move_right_input = gr.Button("➡ Move right", size='sm')
                    bt_move_left_target = gr.Button("⬅ Move left", size='sm')
                    bt_move_right_target = gr.Button("➡ Move right", size='sm')
                with gr.Row():
                    bt_remove_selected_input_face = gr.Button("❌ Remove selected", size='sm')
                    bt_clear_input_faces = gr.Button("💥 Clear all", variant='stop', size='sm')
                    bt_remove_selected_target_face = gr.Button("❌ Remove selected", size='sm')
                    bt_add_local = gr.Button('Add local files from', size='sm')

                with gr.Row():
                    with gr.Column(scale=2):
                        with gr.Accordion(label="Advanced Masking", open=False):
                            chk_showmaskoffsets = gr.Checkbox(
                                label="Show mask overlay in preview",
                                value=False,
                                interactive=True,
                            )
                            chk_restoreoriginalmouth = gr.Checkbox(
                                label="Restore original mouth area",
                                value=False,
                                interactive=True,
                            )
                            mask_top = gr.Slider(
                                0,
                                1.0,
                                value=0,
                                label="Offset Face Top",
                                step=0.01,
                                interactive=True,
                            )
                            mask_bottom = gr.Slider(
                                0,
                                1.0,
                                value=0,
                                label="Offset Face Bottom",
                                step=0.01,
                                interactive=True,
                            )
                            mask_left = gr.Slider(
                                0,
                                1.0,
                                value=0,
                                label="Offset Face Left",
                                step=0.01,
                                interactive=True,
                            )
                            mask_right = gr.Slider(
                                0,
                                1.0,
                                value=0,
                                label="Offset Face Right",
                                step=0.01,
                                interactive=True,
                            )
                            mask_erosion = gr.Slider(
                                1.0,
                                3.0,
                                value=1.0,
                                label="Erosion Iterations",
                                step=1.00,
                                interactive=True,
                            )
                            mask_blur = gr.Slider(
                                10.0,
                                50.0,
                                value=20.0,
                                label="Blur size",
                                step=1.00,
                                interactive=True,
                            )
                            bt_toggle_masking = gr.Button(
                                "Toggle manual masking", variant="secondary", size="sm"
                            )
                            selected_mask_engine = gr.Dropdown(
                                ["None", "Clip2Seg", "DFL XSeg"],
                                value="None",
                                label="Face masking engine",
                            )
                            clip_text = gr.Textbox(
                                label="List of objects to mask and restore back on fake face",
                                value="cup,hands,hair,banana",
                                interactive=False,
                            )
                            bt_preview_mask = gr.Button(
                                "👥 Show Mask Preview", variant="secondary"
                            )
                    with gr.Column(scale=2):
                        local_folder = gr.Textbox(show_label=False, placeholder="/content/", interactive=True)
                with gr.Row(variant='panel'):
                    bt_srcfiles = gr.Files(label='Source Images or Facesets', file_count="multiple", file_types=["image", ".fsz"], elem_id='filelist', height=233)
                    bt_destfiles = gr.Files(label='Target File(s)', file_count="multiple", file_types=["image", "video"], elem_id='filelist', height=233)
                with gr.Row(variant='panel'):
                    gr.Markdown('')
                    forced_fps = gr.Slider(minimum=0, maximum=120, value=0, label="Video FPS", info='Overrides detected fps if not 0', step=1.0, interactive=True, container=True)

            with gr.Column(scale=2):
                previewimage = gr.Image(label="Preview Image", height=576, interactive=False, visible=True, format=get_gradio_output_format())
                maskimage = gr.ImageEditor(label="Manual mask Image", sources=["clipboard"], transforms="", type="numpy",
                                             brush=gr.Brush(color_mode="fixed", colors=["rgba(255, 255, 255, 1"]), interactive=True, visible=False)
                with gr.Row(variant='panel'):
                    fake_preview = gr.Checkbox(label="Face swap frames", value=False)
                    bt_refresh_preview = gr.Button("🔄 Refresh", variant='secondary', size='sm')
                    bt_use_face_from_preview = gr.Button("Use Face from this Frame", variant='primary', size='sm')
                with gr.Row():
                    preview_frame_num = gr.Slider(1, 1, value=1, label="Frame Number", info='0:00:00', step=1.0, interactive=True)
                with gr.Row():
                    text_frame_clip = gr.Markdown('Processing frame range [0 - 0]')
                    set_frame_start = gr.Button("⬅ Set as Start", size='sm')
                    set_frame_end = gr.Button("➡ Set as End", size='sm')
        with gr.Row(visible=False) as dynamic_face_selection:
            with gr.Column(scale=2):
                face_selection = gr.Gallery(label="Detected faces", allow_preview=False, preview=False, height=138, object_fit="cover", columns=32)
            with gr.Column():
                bt_faceselect = gr.Button("☑ Use selected face", size='sm')
                bt_cancelfaceselect = gr.Button("Done", size='sm')
            with gr.Column():
                gr.Markdown(' ') 

        with gr.Row(variant='panel'):
            with gr.Column(scale=1):
                selected_face_detection = gr.Dropdown(swap_choices, value="First found", label="Specify face selection for swapping")
            with gr.Column(scale=1):
                num_swap_steps = gr.Slider(1, 5, value=1, step=1.0, label="Number of swapping steps", info="More steps may increase likeness")
            with gr.Column(scale=2):
                ui.globals.ui_selected_enhancer = gr.Dropdown(["None", "Codeformer", "DMDNet", "GFPGAN", "GPEN", "Restoreformer++"], value="None", label="Select post-processing")

        with gr.Row(variant='panel'):
            with gr.Column(scale=1):
                max_face_distance = gr.Slider(0.01, 1.0, value=0.65, label="Max Face Similarity Threshold", info="0.0 = identical 1.0 = no similarity")
            with gr.Column(scale=1):
                ui.globals.ui_upscale = gr.Dropdown(["128px", "256px", "512px"], value="128px", label="Subsample upscale to", interactive=True)
            with gr.Column(scale=2):
                ui.globals.ui_blend_ratio = gr.Slider(0.0, 1.0, value=0.65, label="Original/Enhanced image blend ratio", info="Only used with active post-processing")

        with gr.Row(variant='panel'):
            with gr.Column(scale=1):
                video_swapping_method = gr.Dropdown(["Extract Frames to media","In-Memory processing"], value="In-Memory processing", label="Select video processing method", interactive=True)
                no_face_action = gr.Dropdown(choices=no_face_choices, value=no_face_choices[0], label="Action on no face detected", interactive=True)
                vr_mode = gr.Checkbox(label="VR Mode", value=False)
            with gr.Column(scale=1):
                with gr.Group():
                    autorotate = gr.Checkbox(label="Auto rotate horizontal Faces", value=True)
                    roop.globals.skip_audio = gr.Checkbox(label="Skip audio", value=False)
                    roop.globals.keep_frames = gr.Checkbox(label="Keep Frames (relevant only when extracting frames)", value=False)
                    roop.globals.wait_after_extraction = gr.Checkbox(label="Wait for user key press before creating video ", value=False)

        with gr.Row(variant='panel'):
            with gr.Column():
                bt_start = gr.Button("▶ Start", variant='primary')
            with gr.Column():
                bt_stop = gr.Button("⏹ Stop", variant='secondary', interactive=False)
                gr.Button("👀 Open Output Folder", size='sm').click(fn=lambda: util.open_folder(roop.globals.output_path))
            with gr.Column(scale=2):
                output_method = gr.Dropdown(["File","Virtual Camera", "Both"], value="File", label="Select Output Method", interactive=True)
        with gr.Row(variant='panel'):
            with gr.Column():
                resultfiles = gr.Files(label='Processed File(s)', interactive=False)
            with gr.Column():
                resultimage = gr.Image(type='filepath', label='Final Image', interactive=False )
                resultvideo = gr.Video(label='Final Video', interactive=False, visible=False)

    previewinputs = [preview_frame_num, bt_destfiles, fake_preview, ui.globals.ui_selected_enhancer, selected_face_detection,
                        max_face_distance, ui.globals.ui_blend_ratio, selected_mask_engine, clip_text, no_face_action, vr_mode, autorotate, maskimage, chk_showmaskoffsets, chk_restoreoriginalmouth, num_swap_steps, ui.globals.ui_upscale]
    previewoutputs = [previewimage, maskimage, preview_frame_num] 
    input_faces.select(on_select_input_face, None, None).success(fn=on_preview_frame_changed, inputs=previewinputs, outputs=previewoutputs)
    
    bt_move_left_input.click(fn=move_selected_input, inputs=[bt_move_left_input], outputs=[input_faces])
    bt_move_right_input.click(fn=move_selected_input, inputs=[bt_move_right_input], outputs=[input_faces])
    bt_move_left_target.click(fn=move_selected_target, inputs=[bt_move_left_target], outputs=[target_faces])
    bt_move_right_target.click(fn=move_selected_target, inputs=[bt_move_right_target], outputs=[target_faces])

    bt_remove_selected_input_face.click(fn=remove_selected_input_face, outputs=[input_faces])
    bt_srcfiles.change(fn=on_srcfile_changed, show_progress='full', inputs=bt_srcfiles, outputs=[dynamic_face_selection, face_selection, input_faces, bt_srcfiles])

    mask_top.release(fn=on_mask_top_changed, inputs=[mask_top], show_progress='hidden')
    mask_bottom.release(fn=on_mask_bottom_changed, inputs=[mask_bottom], show_progress='hidden')
    mask_left.release(fn=on_mask_left_changed, inputs=[mask_left], show_progress='hidden')
    mask_right.release(fn=on_mask_right_changed, inputs=[mask_right], show_progress='hidden')
    mask_erosion.release(fn=on_mask_erosion_changed, inputs=[mask_erosion], show_progress='hidden')
    mask_blur.release(fn=on_mask_blur_changed, inputs=[mask_blur], show_progress='hidden')
    selected_mask_engine.change(fn=on_mask_engine_changed, inputs=[selected_mask_engine], outputs=[clip_text], show_progress='hidden')

    target_faces.select(on_select_target_face, None, None)
    bt_remove_selected_target_face.click(fn=remove_selected_target_face, outputs=[target_faces])

    forced_fps.change(fn=on_fps_changed, inputs=[forced_fps], show_progress='hidden')
    bt_destfiles.change(fn=on_destfiles_changed, inputs=[bt_destfiles], outputs=[preview_frame_num, text_frame_clip], show_progress='hidden').success(fn=on_preview_frame_changed, inputs=previewinputs, outputs=previewoutputs, show_progress='hidden')
    bt_destfiles.select(fn=on_destfiles_selected, outputs=[preview_frame_num, text_frame_clip, forced_fps], show_progress='hidden').success(fn=on_preview_frame_changed, inputs=previewinputs, outputs=previewoutputs, show_progress='hidden')
    bt_destfiles.clear(fn=on_clear_destfiles, outputs=[target_faces, selected_face_detection])
    resultfiles.select(fn=on_resultfiles_selected, inputs=[resultfiles], outputs=[resultimage, resultvideo])

    face_selection.select(on_select_face, None, None)
    bt_faceselect.click(fn=on_selected_face, outputs=[input_faces, target_faces, selected_face_detection])
    bt_cancelfaceselect.click(fn=on_end_face_selection, outputs=[dynamic_face_selection, face_selection])

    bt_clear_input_faces.click(fn=on_clear_input_faces, outputs=[input_faces])

    bt_add_local.click(fn=on_add_local_folder, inputs=[local_folder], outputs=[bt_destfiles])
    bt_preview_mask.click(fn=on_preview_mask, inputs=[preview_frame_num, bt_destfiles, clip_text, selected_mask_engine], outputs=[previewimage]) 

    start_event = bt_start.click(fn=start_swap, 
        inputs=[output_method, ui.globals.ui_selected_enhancer, selected_face_detection, roop.globals.keep_frames, roop.globals.wait_after_extraction,
                    roop.globals.skip_audio, max_face_distance, ui.globals.ui_blend_ratio, selected_mask_engine, clip_text,video_swapping_method, no_face_action, vr_mode, autorotate, chk_restoreoriginalmouth, num_swap_steps, ui.globals.ui_upscale, maskimage],
        outputs=[bt_start, bt_stop, resultfiles], show_progress='full')
    after_swap_event = start_event.success(fn=on_resultfiles_finished, inputs=[resultfiles], outputs=[resultimage, resultvideo])

    bt_stop.click(fn=stop_swap, cancels=[start_event, after_swap_event], outputs=[bt_start, bt_stop], queue=False)

    bt_refresh_preview.click(fn=on_preview_frame_changed, inputs=previewinputs, outputs=previewoutputs)            
    bt_toggle_masking.click(fn=on_toggle_masking, inputs=[previewimage, maskimage], outputs=[previewimage, maskimage])            
    fake_preview.change(fn=on_preview_frame_changed, inputs=previewinputs, outputs=previewoutputs)
    preview_frame_num.release(fn=on_preview_frame_changed, inputs=previewinputs, outputs=previewoutputs, show_progress='hidden', )
    bt_use_face_from_preview.click(fn=on_use_face_from_selected, show_progress='full', inputs=[bt_destfiles, preview_frame_num], outputs=[dynamic_face_selection, face_selection, target_faces, selected_face_detection])
    set_frame_start.click(fn=on_set_frame, inputs=[set_frame_start, preview_frame_num], outputs=[text_frame_clip])
    set_frame_end.click(fn=on_set_frame, inputs=[set_frame_end, preview_frame_num], outputs=[text_frame_clip])


def on_mask_top_changed(mask_offset):
    set_mask_offset(0, mask_offset)

def on_mask_bottom_changed(mask_offset):
    set_mask_offset(1, mask_offset)

def on_mask_left_changed(mask_offset):
    set_mask_offset(2, mask_offset)

def on_mask_right_changed(mask_offset):
    set_mask_offset(3, mask_offset)

def on_mask_erosion_changed(mask_offset):
    set_mask_offset(4, mask_offset)
def on_mask_blur_changed(mask_offset):
    set_mask_offset(5, mask_offset)


def set_mask_offset(index, mask_offset):
    global SELECTED_INPUT_FACE_INDEX

    if len(roop.globals.INPUT_FACESETS) > SELECTED_INPUT_FACE_INDEX:
        offs = roop.globals.INPUT_FACESETS[SELECTED_INPUT_FACE_INDEX].faces[0].mask_offsets
        offs[index] = mask_offset
        if offs[0] + offs[1] > 0.99:
            offs[0] = 0.99
            offs[1] = 0.0
        if offs[2] + offs[3] > 0.99:
            offs[2] = 0.99
            offs[3] = 0.0
        roop.globals.INPUT_FACESETS[SELECTED_INPUT_FACE_INDEX].faces[0].mask_offsets = offs

def on_mask_engine_changed(mask_engine):
    if mask_engine == "Clip2Seg":
        return gr.Textbox(interactive=True)
    return gr.Textbox(interactive=False)


def on_add_local_folder(folder):
    files = util.get_local_files_from_folder(folder)
    if files is None:
        gr.Warning("Empty folder or folder not found!")
    return files


def on_srcfile_changed(srcfiles, progress=gr.Progress()):
    global SELECTION_FACES_DATA, IS_INPUT, input_faces, face_selection, last_image
    
    IS_INPUT = True

    if srcfiles is None or len(srcfiles) < 1:
        return gr.Column(visible=False), None, ui.globals.ui_input_thumbs, None

    for f in srcfiles:    
        source_path = f.name
        if source_path.lower().endswith('fsz'):
            progress(0, desc="Retrieving faces from Faceset File")      
            unzipfolder = os.path.join(os.environ["TEMP"], 'faceset')
            if os.path.isdir(unzipfolder):
                files = os.listdir(unzipfolder)
                for file in files:
                    os.remove(os.path.join(unzipfolder, file))
            else:
                os.makedirs(unzipfolder)
            util.mkdir_with_umask(unzipfolder)
            util.unzip(source_path, unzipfolder)
            is_first = True
            face_set = FaceSet()
            for file in os.listdir(unzipfolder):
                if file.endswith(".png"):
                    filename = os.path.join(unzipfolder,file)
                    progress(0, desc="Extracting faceset")      
                    SELECTION_FACES_DATA = extract_face_images(filename,  (False, 0))
                    for f in SELECTION_FACES_DATA:
                        face = f[0]
                        face.mask_offsets = (0,0,0,0,1,20)
                        face_set.faces.append(face)
                        if is_first: 
                            image = util.convert_to_gradio(f[1])
                            ui.globals.ui_input_thumbs.append(image)
                            is_first = False
                        face_set.ref_images.append(get_image_frame(filename))
            if len(face_set.faces) > 0:
                if len(face_set.faces) > 1:
                    face_set.AverageEmbeddings()
                roop.globals.INPUT_FACESETS.append(face_set)
                                        
        elif util.has_image_extension(source_path):
            progress(0, desc="Retrieving faces from image")      
            roop.globals.source_path = source_path
            SELECTION_FACES_DATA = extract_face_images(roop.globals.source_path,  (False, 0))
            progress(0.5, desc="Retrieving faces from image")
            for f in SELECTION_FACES_DATA:
                face_set = FaceSet()
                face = f[0]
                face.mask_offsets = (0,0,0,0,1,20)
                face_set.faces.append(face)
                image = util.convert_to_gradio(f[1])
                ui.globals.ui_input_thumbs.append(image)
                roop.globals.INPUT_FACESETS.append(face_set)
                
    progress(1.0)
    return gr.Column(visible=False), None, ui.globals.ui_input_thumbs,None


def on_select_input_face(evt: gr.SelectData):
    global SELECTED_INPUT_FACE_INDEX

    SELECTED_INPUT_FACE_INDEX = evt.index


def remove_selected_input_face():
    global SELECTED_INPUT_FACE_INDEX

    if len(roop.globals.INPUT_FACESETS) > SELECTED_INPUT_FACE_INDEX:
        f = roop.globals.INPUT_FACESETS.pop(SELECTED_INPUT_FACE_INDEX)
        del f
    if len(ui.globals.ui_input_thumbs) > SELECTED_INPUT_FACE_INDEX:
        f = ui.globals.ui_input_thumbs.pop(SELECTED_INPUT_FACE_INDEX)
        del f

    return ui.globals.ui_input_thumbs

def move_selected_input(button_text):
    global SELECTED_INPUT_FACE_INDEX

    if button_text == "⬅ Move left":
        if SELECTED_INPUT_FACE_INDEX <= 0:
            return ui.globals.ui_input_thumbs
        offset = -1
    else:
        if len(ui.globals.ui_input_thumbs) <= SELECTED_INPUT_FACE_INDEX:
            return ui.globals.ui_input_thumbs
        offset = 1
    
    f = roop.globals.INPUT_FACESETS.pop(SELECTED_INPUT_FACE_INDEX)
    roop.globals.INPUT_FACESETS.insert(SELECTED_INPUT_FACE_INDEX + offset, f)
    f = ui.globals.ui_input_thumbs.pop(SELECTED_INPUT_FACE_INDEX)
    ui.globals.ui_input_thumbs.insert(SELECTED_INPUT_FACE_INDEX + offset, f)
    return ui.globals.ui_input_thumbs
        

def move_selected_target(button_text):
    global SELECTED_TARGET_FACE_INDEX

    if button_text == "⬅ Move left":
        if SELECTED_TARGET_FACE_INDEX <= 0:
            return ui.globals.ui_target_thumbs
        offset = -1
    else:
        if len(ui.globals.ui_target_thumbs) <= SELECTED_TARGET_FACE_INDEX:
            return ui.globals.ui_target_thumbs
        offset = 1
    
    f = roop.globals.TARGET_FACES.pop(SELECTED_TARGET_FACE_INDEX)
    roop.globals.TARGET_FACES.insert(SELECTED_TARGET_FACE_INDEX + offset, f)
    f = ui.globals.ui_target_thumbs.pop(SELECTED_TARGET_FACE_INDEX)
    ui.globals.ui_target_thumbs.insert(SELECTED_TARGET_FACE_INDEX + offset, f)
    return ui.globals.ui_target_thumbs




def on_select_target_face(evt: gr.SelectData):
    global SELECTED_TARGET_FACE_INDEX

    SELECTED_TARGET_FACE_INDEX = evt.index

def remove_selected_target_face():
    if len(ui.globals.ui_target_thumbs) > SELECTED_TARGET_FACE_INDEX:
        f = roop.globals.TARGET_FACES.pop(SELECTED_TARGET_FACE_INDEX)
        del f
    if len(ui.globals.ui_target_thumbs) > SELECTED_TARGET_FACE_INDEX:
        f = ui.globals.ui_target_thumbs.pop(SELECTED_TARGET_FACE_INDEX)
        del f
    return ui.globals.ui_target_thumbs


def on_use_face_from_selected(files, frame_num):
    global IS_INPUT, SELECTION_FACES_DATA

    IS_INPUT = False
    thumbs = []
    
    roop.globals.target_path = files[selected_preview_index].name
    if util.is_image(roop.globals.target_path) and not roop.globals.target_path.lower().endswith(('gif')):
        SELECTION_FACES_DATA = extract_face_images(roop.globals.target_path,  (False, 0))
        if len(SELECTION_FACES_DATA) > 0:
            for f in SELECTION_FACES_DATA:
                image = util.convert_to_gradio(f[1])
                thumbs.append(image)
        else:
            gr.Info('No faces detected!')
            roop.globals.target_path = None
                
    elif util.is_video(roop.globals.target_path) or roop.globals.target_path.lower().endswith(('gif')):
        selected_frame = frame_num
        SELECTION_FACES_DATA = extract_face_images(roop.globals.target_path, (True, selected_frame))
        if len(SELECTION_FACES_DATA) > 0:
            for f in SELECTION_FACES_DATA:
                image = util.convert_to_gradio(f[1])
                thumbs.append(image)
        else:
            gr.Info('No faces detected!')
            roop.globals.target_path = None
    else:
        gr.Info('Unknown image/video type!')
        roop.globals.target_path = None

    if len(thumbs) == 1:
        roop.globals.TARGET_FACES.append(SELECTION_FACES_DATA[0][0])
        ui.globals.ui_target_thumbs.append(thumbs[0])
        return gr.Row(visible=False), None, ui.globals.ui_target_thumbs, gr.Dropdown(value='Selected face')

    return gr.Row(visible=True), thumbs, gr.Gallery(visible=True), gr.Dropdown(visible=True)


def on_select_face(evt: gr.SelectData):  # SelectData is a subclass of EventData
    global SELECTED_FACE_INDEX
    SELECTED_FACE_INDEX = evt.index


def on_selected_face():
    global IS_INPUT, SELECTED_FACE_INDEX, SELECTION_FACES_DATA
    
    fd = SELECTION_FACES_DATA[SELECTED_FACE_INDEX]
    image = util.convert_to_gradio(fd[1])
    if IS_INPUT:
        face_set = FaceSet()
        fd[0].mask_offsets = (0,0,0,0,1,20)
        face_set.faces.append(fd[0])
        roop.globals.INPUT_FACESETS.append(face_set)
        ui.globals.ui_input_thumbs.append(image)
        return ui.globals.ui_input_thumbs, gr.Gallery(visible=True), gr.Dropdown(visible=True)
    else:
        roop.globals.TARGET_FACES.append(fd[0])
        ui.globals.ui_target_thumbs.append(image)
        return gr.Gallery(visible=True), ui.globals.ui_target_thumbs, gr.Dropdown(value='Selected face')

#        bt_faceselect.click(fn=on_selected_face, outputs=[dynamic_face_selection, face_selection, input_faces, target_faces])

def on_end_face_selection():
    return gr.Column(visible=False), None


def on_preview_frame_changed(frame_num, files, fake_preview, enhancer, detection, face_distance, blend_ratio,
                              selected_mask_engine, clip_text, no_face_action, vr_mode, auto_rotate, maskimage, show_face_area, restore_original_mouth, num_steps, upsample):
    global SELECTED_INPUT_FACE_INDEX, manual_masking, current_video_fps

    from roop.core import live_swap, get_processing_plugins

    manual_masking = False
    mask_offsets = (0,0,0,0)
    if len(roop.globals.INPUT_FACESETS) > SELECTED_INPUT_FACE_INDEX:
        if not hasattr(roop.globals.INPUT_FACESETS[SELECTED_INPUT_FACE_INDEX].faces[0], 'mask_offsets'):
            roop.globals.INPUT_FACESETS[SELECTED_INPUT_FACE_INDEX].faces[0].mask_offsets = mask_offsets
        mask_offsets = roop.globals.INPUT_FACESETS[SELECTED_INPUT_FACE_INDEX].faces[0].mask_offsets

    timeinfo = '0:00:00'
    if files is None or selected_preview_index >= len(files) or frame_num is None:
        return None,None, gr.Slider(info=timeinfo)

    filename = files[selected_preview_index].name
    if util.is_video(filename) or filename.lower().endswith('gif'):
        current_frame = get_video_frame(filename, frame_num)
        if current_video_fps == 0:
            current_video_fps = 1
        secs = (frame_num - 1) / current_video_fps
        minutes = secs / 60
        secs = secs % 60
        hours = minutes / 60
        minutes = minutes % 60
        milliseconds = (secs - int(secs)) * 1000
        timeinfo = f"{int(hours):0>2}:{int(minutes):0>2}:{int(secs):0>2}.{int(milliseconds):0>3}"  
    else:
        current_frame = get_image_frame(filename)
    if current_frame is None:
        return None, None, gr.Slider(info=timeinfo)
    
    layers = None
    if maskimage is not None:
        layers = maskimage["layers"]

    if not fake_preview or len(roop.globals.INPUT_FACESETS) < 1:
        return gr.Image(value=util.convert_to_gradio(current_frame), visible=True), gr.ImageEditor(visible=False), gr.Slider(info=timeinfo)

    roop.globals.face_swap_mode = translate_swap_mode(detection)
    roop.globals.selected_enhancer = enhancer
    roop.globals.distance_threshold = face_distance
    roop.globals.blend_ratio = blend_ratio
    roop.globals.no_face_action = index_of_no_face_action(no_face_action)
    roop.globals.vr_mode = vr_mode
    roop.globals.autorotate_faces = auto_rotate
    roop.globals.subsample_size = int(upsample[:3])


    mask_engine = map_mask_engine(selected_mask_engine, clip_text)

    roop.globals.execution_threads = roop.globals.CFG.max_threads
    mask = layers[0] if layers is not None else None
    face_index = SELECTED_INPUT_FACE_INDEX
    if len(roop.globals.INPUT_FACESETS) <= face_index:
        face_index = 0
   
    options = ProcessOptions(get_processing_plugins(mask_engine), roop.globals.distance_threshold, roop.globals.blend_ratio,
                              roop.globals.face_swap_mode, face_index, clip_text, maskimage, num_steps, roop.globals.subsample_size, show_face_area, restore_original_mouth)

    current_frame = live_swap(current_frame, options)
    if current_frame is None:
        return gr.Image(visible=True), None, gr.Slider(info=timeinfo)
    return gr.Image(value=util.convert_to_gradio(current_frame), visible=True), gr.ImageEditor(visible=False), gr.Slider(info=timeinfo)

def map_mask_engine(selected_mask_engine, clip_text):
    if selected_mask_engine == "Clip2Seg":
        mask_engine = "mask_clip2seg"
        if clip_text is None or len(clip_text) < 1:
          mask_engine = None
    elif selected_mask_engine == "DFL XSeg":
        mask_engine = "mask_xseg"
    else:
        mask_engine = None
    return mask_engine


def on_toggle_masking(previewimage, mask):
    global manual_masking

    manual_masking = not manual_masking
    if manual_masking:
        layers = mask["layers"]
        if len(layers) == 1:
            layers = [create_blank_image(previewimage.shape[1],previewimage.shape[0])]
        return gr.Image(visible=False), gr.ImageEditor(value={"background": previewimage, "layers": layers, "composite": None}, visible=True)
    return gr.Image(visible=True), gr.ImageEditor(visible=False)

def gen_processing_text(start, end):
    return f'Processing frame range [{start} - {end}]'

def on_set_frame(sender:str, frame_num):
    global selected_preview_index, list_files_process
    
    idx = selected_preview_index
    if list_files_process[idx].endframe == 0:
        return gen_processing_text(0,0)
    
    start = list_files_process[idx].startframe
    end = list_files_process[idx].endframe
    if sender.lower().endswith('start'):
        list_files_process[idx].startframe = min(frame_num, end)
    else:
        list_files_process[idx].endframe = max(frame_num, start)
    
    return gen_processing_text(list_files_process[idx].startframe,list_files_process[idx].endframe)


def on_preview_mask(frame_num, files, clip_text, mask_engine):
    from roop.core import live_swap, get_processing_plugins
    global is_processing

    if is_processing or files is None or selected_preview_index >= len(files) or clip_text is None or frame_num is None:
        return None
        
    filename = files[selected_preview_index].name
    if util.is_video(filename) or filename.lower().endswith('gif'):
        current_frame = get_video_frame(filename, frame_num
                                        )
    else:
        current_frame = get_image_frame(filename)
    if current_frame is None or mask_engine is None:
        return None
    if mask_engine == "Clip2Seg":
        mask_engine = "mask_clip2seg"
        if clip_text is None or len(clip_text) < 1:
          mask_engine = None
    elif mask_engine == "DFL XSeg":
        mask_engine = "mask_xseg"
    options = ProcessOptions(get_processing_plugins(mask_engine), roop.globals.distance_threshold, roop.globals.blend_ratio,
                              "all", 0, clip_text, None, 0, 128, False, False, True)

    current_frame = live_swap(current_frame, options)
    return util.convert_to_gradio(current_frame)


def on_clear_input_faces():
    ui.globals.ui_input_thumbs.clear()
    roop.globals.INPUT_FACESETS.clear()
    return ui.globals.ui_input_thumbs

def on_clear_destfiles():
    roop.globals.TARGET_FACES.clear()
    ui.globals.ui_target_thumbs.clear()
    return ui.globals.ui_target_thumbs, gr.Dropdown(value="First found")    


def index_of_no_face_action(dropdown_text):
    global no_face_choices

    return no_face_choices.index(dropdown_text) 

def translate_swap_mode(dropdown_text):
    if dropdown_text == "Selected face":
        return "selected"
    elif dropdown_text == "First found":
        return "first"
    elif dropdown_text == "All input faces":
        return "all_input"
    elif dropdown_text == "All female":
        return "all_female"
    elif dropdown_text == "All male":
        return "all_male"
    
    return "all"


def start_swap( output_method, enhancer, detection, keep_frames, wait_after_extraction, skip_audio, face_distance, blend_ratio,
                selected_mask_engine, clip_text, processing_method, no_face_action, vr_mode, autorotate, restore_original_mouth, num_swap_steps, upsample, imagemask, progress=gr.Progress()):
    from ui.main import prepare_environment
    from roop.core import batch_process_regular
    global is_processing, list_files_process

    if list_files_process is None or len(list_files_process) <= 0:
        return gr.Button(variant="primary"), None, None
    
    if roop.globals.CFG.clear_output:
        clean_dir(roop.globals.output_path)

    if not util.is_installed("ffmpeg"):
        msg = "ffmpeg is not installed! No video processing possible."
        gr.Warning(msg)

    prepare_environment()

    roop.globals.selected_enhancer = enhancer
    roop.globals.target_path = None
    roop.globals.distance_threshold = face_distance
    roop.globals.blend_ratio = blend_ratio
    roop.globals.keep_frames = keep_frames
    roop.globals.wait_after_extraction = wait_after_extraction
    roop.globals.skip_audio = skip_audio
    roop.globals.face_swap_mode = translate_swap_mode(detection)
    roop.globals.no_face_action = index_of_no_face_action(no_face_action)
    roop.globals.vr_mode = vr_mode
    roop.globals.autorotate_faces = autorotate
    roop.globals.subsample_size = int(upsample[:3])
    mask_engine = map_mask_engine(selected_mask_engine, clip_text)

    if roop.globals.face_swap_mode == 'selected':
        if len(roop.globals.TARGET_FACES) < 1:
            gr.Error('No Target Face selected!')
            return gr.Button(variant="primary"), None, None

    is_processing = True            
    yield gr.Button(variant="secondary", interactive=False), gr.Button(variant="primary", interactive=True), None
    roop.globals.execution_threads = roop.globals.CFG.max_threads
    roop.globals.video_encoder = roop.globals.CFG.output_video_codec
    roop.globals.video_quality = roop.globals.CFG.video_quality
    roop.globals.max_memory = roop.globals.CFG.memory_limit if roop.globals.CFG.memory_limit > 0 else None

    batch_process_regular(output_method, list_files_process, mask_engine, clip_text, processing_method == "In-Memory processing", imagemask, restore_original_mouth, num_swap_steps, progress, SELECTED_INPUT_FACE_INDEX)
    is_processing = False
    outdir = pathlib.Path(roop.globals.output_path)
    outfiles = [str(item) for item in outdir.rglob("*") if item.is_file()]
    if len(outfiles) > 0:
        yield gr.Button(variant="primary", interactive=True),gr.Button(variant="secondary", interactive=False),gr.Files(value=outfiles)
    else:
        yield gr.Button(variant="primary", interactive=True),gr.Button(variant="secondary", interactive=False),None


def stop_swap():
    roop.globals.processing = False
    gr.Info('Aborting processing - please wait for the remaining threads to be stopped')
    return gr.Button(variant="primary", interactive=True),gr.Button(variant="secondary", interactive=False),None


def on_fps_changed(fps):
    global selected_preview_index, list_files_process

    if len(list_files_process) < 1 or list_files_process[selected_preview_index].endframe < 1:
        return
    list_files_process[selected_preview_index].fps = fps


def on_destfiles_changed(destfiles):
    global selected_preview_index, list_files_process, current_video_fps

    if destfiles is None or len(destfiles) < 1:
        list_files_process.clear()
        return gr.Slider(value=1, maximum=1, info='0:00:00'), ''
    
    for f in destfiles:
        list_files_process.append(ProcessEntry(f.name, 0,0, 0))

    selected_preview_index = 0
    idx = selected_preview_index    
    
    filename = list_files_process[idx].filename
    
    if util.is_video(filename) or filename.lower().endswith('gif'):
        total_frames = get_video_frame_total(filename)
        if total_frames is None or total_frames < 1:
            total_frames = 1
            gr.Warning(f"Corrupted video {filename}, can't detect number of frames!")
        else:
            current_video_fps = util.detect_fps(filename)
    else:
        total_frames = 1
    list_files_process[idx].endframe = total_frames
    if total_frames > 1:
        return gr.Slider(value=1, maximum=total_frames, info='0:00:00'), gen_processing_text(list_files_process[idx].startframe,list_files_process[idx].endframe)
    return gr.Slider(value=1, maximum=total_frames, info='0:00:00'), ''


def on_destfiles_selected(evt: gr.SelectData):
    global selected_preview_index, list_files_process, current_video_fps

    if evt is not None:
        selected_preview_index = evt.index
    idx = selected_preview_index    
    filename = list_files_process[idx].filename
    fps = list_files_process[idx].fps
    if util.is_video(filename) or filename.lower().endswith('gif'):
        total_frames = get_video_frame_total(filename)
        current_video_fps = util.detect_fps(filename)
        if list_files_process[idx].endframe == 0:
            list_files_process[idx].endframe = total_frames 
    else:
        total_frames = 1
    
    if total_frames > 1:
        return gr.Slider(value=list_files_process[idx].startframe, maximum=total_frames, info='0:00:00'), gen_processing_text(list_files_process[idx].startframe,list_files_process[idx].endframe), fps
    return gr.Slider(value=1, maximum=total_frames, info='0:00:00'), gen_processing_text(0,0), fps


def on_resultfiles_selected(evt: gr.SelectData, files):
    selected_index = evt.index
    filename = files[selected_index].name
    return display_output(filename)

def on_resultfiles_finished(files):
    selected_index = 0
    if files is None or len(files) < 1:
        return None, None
    
    filename = files[selected_index].name
    return display_output(filename)


def get_gradio_output_format():
    if roop.globals.CFG.output_image_format == "jpg":
        return "jpeg"
    return roop.globals.CFG.output_image_format


def display_output(filename):
    if util.is_video(filename) and roop.globals.CFG.output_show_video:
        return gr.Image(visible=False), gr.Video(visible=True, value=filename)
    else:
        if util.is_video(filename) or filename.lower().endswith('gif'):
            current_frame = get_video_frame(filename)
        else:
            current_frame = get_image_frame(filename)
        return gr.Image(visible=True, value=util.convert_to_gradio(current_frame)), gr.Video(visible=False)

```

# ui\tabs\facemgr_tab.py

```py
import os
import shutil
import cv2
import gradio as gr
import roop.utilities as util
import roop.globals
from roop.face_util import extract_face_images
from roop.capturer import get_video_frame, get_video_frame_total
from typing import List, Tuple, Optional
from roop.typing import Frame, Face, FaceSet

selected_face_index = -1
thumbs = []
images = []


def facemgr_tab() -> None:
    with gr.Tab("👨‍👩‍👧‍👦 Face Management"):
        with gr.Row():
            gr.Markdown("""
                        # Create blending facesets
                        Add multiple reference images into a faceset file.
                        """)
        with gr.Row():
            videoimagefst = gr.Image(label="Cut face from video frame", height=576, interactive=False, visible=True, format="jpeg")
        with gr.Row():
            frame_num_fst = gr.Slider(1, 1, value=1, label="Frame Number", info='0:00:00', step=1.0, interactive=False)
            fb_cutfromframe = gr.Button("Use faces from this frame", variant='secondary', interactive=False)
        with gr.Row():
            fb_facesetfile = gr.Files(label='Faceset', file_count='single', file_types=['.fsz'], interactive=True)
            fb_files = gr.Files(label='Input Files', file_count="multiple", file_types=["image", "video"], interactive=True)
        with gr.Row():
            with gr.Column():
                gr.Button("👀 Open Output Folder", size='sm').click(fn=lambda: util.open_folder(roop.globals.output_path))
            with gr.Column():
                gr.Markdown(' ')
        with gr.Row():
            faces = gr.Gallery(label="Faces in this Faceset", allow_preview=True, preview=True, height=128, object_fit="scale-down")
        with gr.Row():
            fb_remove = gr.Button("Remove selected", variant='secondary')
            fb_update = gr.Button("Create/Update Faceset file", variant='primary')
            fb_clear = gr.Button("Clear all", variant='stop')

    fb_facesetfile.change(fn=on_faceset_changed, inputs=[fb_facesetfile], outputs=[faces])
    fb_files.change(fn=on_fb_files_changed, inputs=[fb_files], outputs=[faces, videoimagefst, frame_num_fst, fb_cutfromframe])
    fb_update.click(fn=on_update_clicked, outputs=[fb_facesetfile])
    fb_remove.click(fn=on_remove_clicked, outputs=[faces])
    fb_clear.click(fn=on_clear_clicked, outputs=[faces, fb_files, fb_facesetfile])
    fb_cutfromframe.click(fn=on_cutfromframe_clicked, inputs=[fb_files, frame_num_fst], outputs=[faces])
    frame_num_fst.release(fn=on_frame_num_fst_changed, inputs=[fb_files, frame_num_fst], outputs=[videoimagefst])
    faces.select(fn=on_face_selected)


def on_faceset_changed(faceset, progress=gr.Progress()) -> List[Frame]:
    global thumbs, images

    if faceset is None:
        return thumbs

    thumbs.clear()
    filename = faceset.name
        
    if filename.lower().endswith('fsz'):
        progress(0, desc="Retrieving faces from Faceset File", )      
        unzipfolder = os.path.join(os.environ["TEMP"], 'faceset')
        if os.path.isdir(unzipfolder):
            shutil.rmtree(unzipfolder)
        util.mkdir_with_umask(unzipfolder)
        util.unzip(filename, unzipfolder)
        for file in os.listdir(unzipfolder):
            if file.endswith(".png"):
                SELECTION_FACES_DATA = extract_face_images(os.path.join(unzipfolder,file),  (False, 0), 0.5)
                if len(SELECTION_FACES_DATA) < 1:
                    gr.Warning(f"No face detected in {file}!")
                for f in SELECTION_FACES_DATA:
                    image = f[1]
                    images.append(image)
                    thumbs.append(util.convert_to_gradio(image))
        
        return thumbs


def on_fb_files_changed(inputfiles, progress=gr.Progress()) -> Tuple[List[Frame], Optional[gr.Image], Optional[gr.Slider], Optional[gr.Button]]:
    global thumbs, images, total_frames, current_video_fps

    if inputfiles is None or len(inputfiles) < 1:
        return thumbs, None, None, None
    
    progress(0, desc="Retrieving faces from images", )
    slider = None
    video_image = None
    cut_button = None
    for f in inputfiles:
        source_path = f.name
        if util.has_image_extension(source_path):
            slider = gr.Slider(interactive=False)
            video_image = gr.Image(interactive=False)
            cut_button = gr.Button(interactive=False)
            roop.globals.source_path = source_path
            SELECTION_FACES_DATA = extract_face_images(roop.globals.source_path,  (False, 0), 0.5)
            for f in SELECTION_FACES_DATA:
                image = f[1]
                images.append(image)
                thumbs.append(util.convert_to_gradio(image))
        elif util.is_video(source_path) or source_path.lower().endswith('gif'):
            total_frames = get_video_frame_total(source_path)
            current_video_fps = util.detect_fps(source_path)
            cut_button = gr.Button(interactive=True)
            video_image, slider = display_video_frame(source_path, 1, total_frames)

    return thumbs, video_image, slider, cut_button
    

def display_video_frame(filename: str, frame_num: int, total: int=0) -> Tuple[gr.Image, gr.Slider]:
    global current_video_fps

    current_frame = get_video_frame(filename, frame_num)
    if current_video_fps == 0:
        current_video_fps = 1
    secs = (frame_num - 1) / current_video_fps
    minutes = secs / 60
    secs = secs % 60
    hours = minutes / 60
    minutes = minutes % 60
    milliseconds = (secs - int(secs)) * 1000
    timeinfo = f"{int(hours):0>2}:{int(minutes):0>2}:{int(secs):0>2}.{int(milliseconds):0>3}"
    if total > 0:
        return gr.Image(value=util.convert_to_gradio(current_frame), interactive=True), gr.Slider(info=timeinfo, minimum=1, maximum=total, interactive=True)  
    return gr.Image(value=util.convert_to_gradio(current_frame), interactive=True), gr.Slider(info=timeinfo, interactive=True)  


def on_face_selected(evt: gr.SelectData) -> None:
    global selected_face_index

    if evt is not None:
        selected_face_index = evt.index

def on_frame_num_fst_changed(inputfiles: List[gr.Files], frame_num: int) -> Frame:
    filename = inputfiles[0].name
    video_image, _ = display_video_frame(filename, frame_num, 0)
    return video_image


def on_cutfromframe_clicked(inputfiles: List[gr.Files], frame_num: int) -> List[Frame]:
    global thumbs

    filename = inputfiles[0].name
    SELECTION_FACES_DATA = extract_face_images(filename,  (True, frame_num), 0.5)
    for f in SELECTION_FACES_DATA:
        image = f[1]
        images.append(image)
        thumbs.append(util.convert_to_gradio(image))
    return thumbs


def on_remove_clicked() -> List[Frame]:
    global thumbs, images, selected_face_index

    if len(thumbs) > selected_face_index:
        f = thumbs.pop(selected_face_index)
        del f
        f = images.pop(selected_face_index)
        del f
    return thumbs

def on_clear_clicked() -> Tuple[List[Frame], None, None]:
    global thumbs, images

    thumbs.clear()
    images.clear()
    return thumbs, None, None


def on_update_clicked() -> Optional[str]:
    if len(images) < 1:
        gr.Warning(f"No faces to create faceset from!")
        return None

    imgnames = []
    for index,img in enumerate(images):
        filename = os.path.join(roop.globals.output_path, f'{index}.png')
        cv2.imwrite(filename, img)
        imgnames.append(filename)

    finalzip = os.path.join(roop.globals.output_path, 'faceset.fsz')        
    util.zip(imgnames, finalzip)
    return finalzip

```

# ui\tabs\extras_tab.py

```py
import os
import gradio as gr
import shutil
import roop.utilities as util
import roop.util_ffmpeg as ffmpeg
import roop.globals
from roop.utilities import clean_dir

frame_filters_map = { 
    "Colorize B/W Images (Deoldify Artistic)" : {"colorizer" : {"subtype": "deoldify_artistic"}},
    "Colorize B/W Images (Deoldify Stable)" : {"colorizer" : {"subtype": "deoldify_stable"}},
    "Background remove" : {"removebg" : {"subtype": ""}},
    "Filter Stylize" : {"filter_generic" : {"subtype" : "stylize" }},
    "Filter Detail Enhance" : {"filter_generic" : {"subtype" : "detailenhance" }},
    "Filter Pencil Sketch" : {"filter_generic" : {"subtype" : "pencil" }},
    "Filter Cartoon" : {"filter_generic" : {"subtype" : "cartoon" }},
    "Filter C64" : {"filter_generic" : {"subtype" : "C64" }}
    }

frame_upscalers_map = {
    "ESRGAN x2" : {"upscale" : {"subtype": "esrganx2"}},
    "ESRGAN x4" : {"upscale" : {"subtype": "esrganx4"}},
    "LSDIR x4" : {"upscale" : {"subtype": "lsdirx4"}}
}

def extras_tab():
    filternames = ["None"]
    for f in frame_filters_map.keys():
        filternames.append(f)
    upscalernames = ["None"]
    for f in frame_upscalers_map.keys():
        upscalernames.append(f)

    with gr.Tab("🎉 Extras"):
        with gr.Row():
            files_to_process = gr.Files(label='File(s) to process', file_count="multiple", file_types=["image", "video"])
        with gr.Row(variant='panel'):
            with gr.Accordion(label="Video/GIF", open=False):
                with gr.Row(variant='panel'):
                    with gr.Column():
                        gr.Markdown("""
                                    # Poor man's video editor
                                    Re-encoding uses your configuration from the Settings Tab.
    """)
                    with gr.Column():
                        cut_start_time = gr.Slider(0, 1000000, value=0, label="Start Frame", step=1.0, interactive=True)
                    with gr.Column():
                        cut_end_time = gr.Slider(1, 1000000, value=1, label="End Frame", step=1.0, interactive=True)
                    with gr.Column():
                        extras_chk_encode = gr.Checkbox(label='Re-encode videos (necessary for videos with different codecs)', value=False)
                        start_cut_video = gr.Button("Cut video")
                        start_extract_frames = gr.Button("Extract frames")
                        start_join_videos = gr.Button("Join videos")

                with gr.Row(variant='panel'):
                    with gr.Column():
                        gr.Markdown("""
                                    # Create video/gif from images
    """)
                    with gr.Column():
                        extras_fps = gr.Slider(minimum=0, maximum=120, value=30, label="Video FPS", step=1.0, interactive=True)
                        extras_images_folder = gr.Textbox(show_label=False, placeholder="/content/", interactive=True)
                    with gr.Column():
                        extras_chk_creategif = gr.Checkbox(label='Create GIF from video', value=False)
                        extras_create_video=gr.Button("Create")
                with gr.Row(variant='panel'):
                    with gr.Column():
                        gr.Markdown("""
                                    # Create video from gif
    """)
                    with gr.Column():
                        extras_video_fps = gr.Slider(minimum=0, maximum=120, value=0, label="Video FPS", step=1.0, interactive=True)
                    with gr.Column():
                        extras_create_video_from_gif=gr.Button("Create")
                with gr.Row(variant='panel'):
                    with gr.Column(scale=2):
                        gr.Markdown("""
                                    # Repair video

                                    Uses FFMpeg to fix corrupt videos. 
    """)
                    with gr.Column():
                        extras_repair_video=gr.Button("Repair")


        with gr.Row(variant='panel'):
            with gr.Accordion(label="Full frame processing", open=True):
                with gr.Row(variant='panel'):
                    filterselection = gr.Dropdown(filternames, value="None", label="Colorizer/FilterFX", interactive=True)
                    upscalerselection = gr.Dropdown(upscalernames, value="None", label="Enhancer", interactive=True)
                with gr.Row(variant='panel'):
                    start_frame_process=gr.Button("Start processing")

        with gr.Row():
            gr.Button("👀 Open Output Folder", size='sm').click(fn=lambda: util.open_folder(roop.globals.output_path))
        with gr.Row():
            extra_files_output = gr.Files(label='Resulting output files', file_count="multiple")

    start_cut_video.click(fn=on_cut_video, inputs=[files_to_process, cut_start_time, cut_end_time, extras_chk_encode], outputs=[extra_files_output])
    start_extract_frames.click(fn=on_extras_extract_frames, inputs=[files_to_process], outputs=[extra_files_output])
    start_join_videos.click(fn=on_join_videos, inputs=[files_to_process, extras_chk_encode], outputs=[extra_files_output])
    extras_create_video.click(fn=on_extras_create_video, inputs=[files_to_process, extras_images_folder, extras_fps, extras_chk_creategif], outputs=[extra_files_output])
    extras_create_video_from_gif.click(fn=on_extras_create_video_from_gif, inputs=[files_to_process, extras_video_fps], outputs=[extra_files_output])
    extras_repair_video.click(fn=on_extras_repair_video, inputs=[files_to_process], outputs=[extra_files_output])
    start_frame_process.click(fn=on_frame_process, inputs=[files_to_process, filterselection, upscalerselection], outputs=[extra_files_output])


def on_cut_video(files, cut_start_frame, cut_end_frame, reencode):
    if files is None:
        return None
    
    resultfiles = []
    for tf in files:
        f = tf.name
        destfile = util.get_destfilename_from_path(f, roop.globals.output_path, '_cut')
        ffmpeg.cut_video(f, destfile, cut_start_frame, cut_end_frame, reencode)
        if os.path.isfile(destfile):
            resultfiles.append(destfile)
        else:
            gr.Error('Cutting video failed!')
    return resultfiles


def on_join_videos(files, chk_encode):
    if files is None:
        return None
    
    filenames = []
    for f in files:
        filenames.append(f.name)
    destfile = util.get_destfilename_from_path(filenames[0], roop.globals.output_path, '_join')
    sorted_filenames = util.sort_filenames_ignore_path(filenames)        
    ffmpeg.join_videos(sorted_filenames, destfile, not chk_encode)
    resultfiles = []
    if os.path.isfile(destfile):
        resultfiles.append(destfile)
    else:
        gr.Error('Joining videos failed!')
    return resultfiles

def on_extras_create_video_from_gif(files,fps):
    if files is None:
        return None
    
    filenames = []
    resultfiles = []
    for f in files:
        filenames.append(f.name)

    destfilename = os.path.join(roop.globals.output_path, "img2video." + roop.globals.CFG.output_video_format)
    ffmpeg.create_video_from_gif(filenames[0], destfilename)
    if os.path.isfile(destfilename):
        resultfiles.append(destfilename)
    return resultfiles


def on_extras_repair_video(files):
    if files is None:
        return None
    
    resultfiles = []
    for tf in files:
        f = tf.name
        destfile = util.get_destfilename_from_path(f, roop.globals.output_path, '_repair')
        ffmpeg.repair_video(f, destfile)
        if os.path.isfile(destfile):
            resultfiles.append(destfile)
        else:
            gr.Error('Repairing video failed!')
    return resultfiles





def on_extras_create_video(files, images_path,fps, create_gif):
    if images_path is None:
        return None
    resultfiles = []
    if len(files) > 0 and util.is_video(files[0]) and create_gif:
        destfilename = files[0]
    else:                     
        util.sort_rename_frames(os.path.dirname(images_path))
        destfilename = os.path.join(roop.globals.output_path, "img2video." + roop.globals.CFG.output_video_format)
        ffmpeg.create_video('', destfilename, fps, images_path)
        if os.path.isfile(destfilename):
            resultfiles.append(destfilename)
        else:
            return None
    if create_gif:
        gifname = util.get_destfilename_from_path(destfilename, './output', '.gif')
        ffmpeg.create_gif_from_video(destfilename, gifname)
        if os.path.isfile(destfilename):
            resultfiles.append(gifname)
    return resultfiles
    

def on_extras_extract_frames(files):
    if files is None:
        return None
    
    resultfiles = []
    for tf in files:
        f = tf.name
        resfolder = ffmpeg.extract_frames(f)
        for file in os.listdir(resfolder):
            outfile = os.path.join(resfolder, file)
            if os.path.isfile(outfile):
                resultfiles.append(outfile)
    return resultfiles


def on_frame_process(files, filterselection, upscaleselection):
    import pathlib
    from roop.core import batch_process_with_options
    from roop.ProcessEntry import ProcessEntry
    from roop.ProcessOptions import ProcessOptions
    from ui.main import prepare_environment


    if files is None:
        return None

    if roop.globals.CFG.clear_output:
        clean_dir(roop.globals.output_path)
    prepare_environment()
    list_files_process : list[ProcessEntry] = []

    for tf in files:
        list_files_process.append(ProcessEntry(tf.name, 0,0, 0))

    processoroptions = {}
    filter = next((x for x in frame_filters_map.keys() if x == filterselection), None)
    if filter is not None:
        processoroptions.update(frame_filters_map[filter])
    filter = next((x for x in frame_upscalers_map.keys() if x == upscaleselection), None)
    if filter is not None:
        processoroptions.update(frame_upscalers_map[filter])
    options = ProcessOptions(processoroptions, 0,  0, "all", 0, None, None, 0, 128, False, False)
    batch_process_with_options(list_files_process, options, None)
    outdir = pathlib.Path(roop.globals.output_path)
    outfiles = [str(item) for item in outdir.rglob("*") if item.is_file()]
    return outfiles



```

# roop\processors\__init__.py

```py

```

# roop\processors\Mask_XSeg.py

```py
import numpy as np
import cv2
import onnxruntime
import roop.globals

from roop.typing import Frame
from roop.utilities import resolve_relative_path, conditional_thread_semaphore



class Mask_XSeg():
    plugin_options:dict = None

    model_xseg = None

    processorname = 'mask_xseg'
    type = 'mask'


    def Initialize(self, plugin_options:dict):
        if self.plugin_options is not None:
            if self.plugin_options["devicename"] != plugin_options["devicename"]:
                self.Release()

        self.plugin_options = plugin_options
        if self.model_xseg is None:
            model_path = resolve_relative_path('../models/xseg.onnx')
            onnxruntime.set_default_logger_severity(3)
            self.model_xseg = onnxruntime.InferenceSession(model_path, None, providers=roop.globals.execution_providers)
            self.model_inputs = self.model_xseg.get_inputs()
            self.model_outputs = self.model_xseg.get_outputs()

            # replace Mac mps with cpu for the moment
            self.devicename = self.plugin_options["devicename"].replace('mps', 'cpu')


    def Run(self, img1, keywords:str) -> Frame:
        temp_frame = cv2.resize(img1, (256, 256), cv2.INTER_CUBIC)
        temp_frame = temp_frame.astype('float32') / 255.0
        temp_frame = temp_frame[None, ...]
        io_binding = self.model_xseg.io_binding()           
        io_binding.bind_cpu_input(self.model_inputs[0].name, temp_frame)
        io_binding.bind_output(self.model_outputs[0].name, self.devicename)
        self.model_xseg.run_with_iobinding(io_binding)
        ort_outs = io_binding.copy_outputs_to_cpu()
        result = ort_outs[0][0]
        result = np.clip(result, 0, 1.0)
        result[result < 0.1] = 0
        # invert values to mask areas to keep
        result = 1.0 - result
        return result       


    def Release(self):
        del self.model_xseg
        self.model_xseg = None



```

# roop\processors\Mask_Clip2Seg.py

```py
import cv2
import numpy as np
import torch
import threading
from torchvision import transforms
from clip.clipseg import CLIPDensePredT
import numpy as np

from roop.typing import Frame

THREAD_LOCK_CLIP = threading.Lock()


class Mask_Clip2Seg():
    plugin_options:dict = None
    model_clip = None

    processorname = 'clip2seg'
    type = 'mask'


    def Initialize(self, plugin_options:dict):
        if self.plugin_options is not None:
            if self.plugin_options["devicename"] != plugin_options["devicename"]:
                self.Release()

        self.plugin_options = plugin_options
        if self.model_clip is None:
            self.model_clip = CLIPDensePredT(version='ViT-B/16', reduce_dim=64, complex_trans_conv=True)
            self.model_clip.eval();
            self.model_clip.load_state_dict(torch.load('models/CLIP/rd64-uni-refined.pth', map_location=torch.device('cpu')), strict=False)

        device = torch.device(self.plugin_options["devicename"])
        self.model_clip.to(device)


    def Run(self, img1, keywords:str) -> Frame:
        if keywords is None or len(keywords) < 1 or img1 is None:
            return img1
        
        source_image_small = cv2.resize(img1, (256,256))
        
        img_mask = np.full((source_image_small.shape[0],source_image_small.shape[1]), 0, dtype=np.float32)
        mask_border = 1
        l = 0
        t = 0
        r = 1
        b = 1
        
        mask_blur = 5
        clip_blur = 5
        
        img_mask = cv2.rectangle(img_mask, (mask_border+int(l), mask_border+int(t)), 
                                (256 - mask_border-int(r), 256-mask_border-int(b)), (255, 255, 255), -1)    
        img_mask = cv2.GaussianBlur(img_mask, (mask_blur*2+1,mask_blur*2+1), 0)    
        img_mask /= 255

        
        input_image = source_image_small

        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            transforms.Resize((256, 256)),
        ])
        img = transform(input_image).unsqueeze(0)

        thresh = 0.5
        prompts = keywords.split(',')
        with THREAD_LOCK_CLIP:
            with torch.no_grad():
                preds = self.model_clip(img.repeat(len(prompts),1,1,1), prompts)[0]
        clip_mask = torch.sigmoid(preds[0][0])
        for i in range(len(prompts)-1):
            clip_mask += torch.sigmoid(preds[i+1][0])
           
        clip_mask = clip_mask.data.cpu().numpy()
        np.clip(clip_mask, 0, 1)
        
        clip_mask[clip_mask>thresh] = 1.0
        clip_mask[clip_mask<=thresh] = 0.0
        kernel = np.ones((5, 5), np.float32)
        clip_mask = cv2.dilate(clip_mask, kernel, iterations=1)
        clip_mask = cv2.GaussianBlur(clip_mask, (clip_blur*2+1,clip_blur*2+1), 0)
       
        img_mask *= clip_mask
        img_mask[img_mask<0.0] = 0.0
        return img_mask
       


    def Release(self):
        self.model_clip = None


```

# roop\processors\Frame_Upscale.py

```py
import cv2 
import numpy as np
import onnxruntime
import roop.globals

from roop.utilities import resolve_relative_path, conditional_thread_semaphore
from roop.typing import Frame


class Frame_Upscale():
    plugin_options:dict = None
    model_upscale = None
    devicename = None
    prev_type = None

    processorname = 'upscale'
    type = 'frame_enhancer'


    def Initialize(self, plugin_options:dict):
        if self.plugin_options is not None:
            if self.plugin_options["devicename"] != plugin_options["devicename"]:
                self.Release()

        self.plugin_options = plugin_options
        if self.prev_type is not None and self.prev_type != self.plugin_options["subtype"]:
            self.Release()
        self.prev_type = self.plugin_options["subtype"]
        if self.model_upscale is None:
            # replace Mac mps with cpu for the moment
            self.devicename = self.plugin_options["devicename"].replace('mps', 'cpu')
            if self.prev_type == "esrganx4":
                model_path = resolve_relative_path('../models/Frame/real_esrgan_x4.onnx')
                self.scale = 4
            elif self.prev_type == "esrganx2":
                model_path = resolve_relative_path('../models/Frame/real_esrgan_x2.onnx')
                self.scale = 2
            elif self.prev_type == "lsdirx4":
                model_path = resolve_relative_path('../models/Frame/lsdir_x4.onnx')
                self.scale = 4
            onnxruntime.set_default_logger_severity(3)
            self.model_upscale = onnxruntime.InferenceSession(model_path, None, providers=roop.globals.execution_providers)
            self.model_inputs = self.model_upscale.get_inputs()
            model_outputs = self.model_upscale.get_outputs()
            self.io_binding = self.model_upscale.io_binding()
            self.io_binding.bind_output(model_outputs[0].name, self.devicename)

    def getProcessedResolution(self, width, height):
        return (width * self.scale, height * self.scale)

# borrowed from facefusion -> https://github.com/facefusion/facefusion
    def prepare_tile_frame(self, tile_frame : Frame) -> Frame:
        tile_frame = np.expand_dims(tile_frame[:, :, ::-1], axis = 0)
        tile_frame = tile_frame.transpose(0, 3, 1, 2)
        tile_frame = tile_frame.astype(np.float32) / 255
        return tile_frame


    def normalize_tile_frame(self, tile_frame : Frame) -> Frame:
        tile_frame = tile_frame.transpose(0, 2, 3, 1).squeeze(0) * 255
        tile_frame = tile_frame.clip(0, 255).astype(np.uint8)[:, :, ::-1]
        return tile_frame

    def create_tile_frames(self, input_frame : Frame, size):
        input_frame = np.pad(input_frame, ((size[1], size[1]), (size[1], size[1]), (0, 0)))
        tile_width = size[0] - 2 * size[2]
        pad_size_bottom = size[2] + tile_width - input_frame.shape[0] % tile_width
        pad_size_right = size[2] + tile_width - input_frame.shape[1] % tile_width
        pad_vision_frame = np.pad(input_frame, ((size[2], pad_size_bottom), (size[2], pad_size_right), (0, 0)))
        pad_height, pad_width = pad_vision_frame.shape[:2]
        row_range = range(size[2], pad_height - size[2], tile_width)
        col_range = range(size[2], pad_width - size[2], tile_width)
        tile_frames = []

        for row_frame in row_range:
            top = row_frame - size[2]
            bottom = row_frame + size[2] + tile_width
            for column_vision_frame in col_range:
                left = column_vision_frame - size[2]
                right = column_vision_frame + size[2] + tile_width
                tile_frames.append(pad_vision_frame[top:bottom, left:right, :])
        return tile_frames, pad_width, pad_height


    def merge_tile_frames(self, tile_frames, temp_width : int, temp_height : int, pad_width : int, pad_height : int, size) -> Frame:
        merge_frame = np.zeros((pad_height, pad_width, 3)).astype(np.uint8)
        tile_width = tile_frames[0].shape[1] - 2 * size[2]
        tiles_per_row = min(pad_width // tile_width, len(tile_frames))

        for index, tile_frame in enumerate(tile_frames):
            tile_frame = tile_frame[size[2]:-size[2], size[2]:-size[2]]
            row_index = index // tiles_per_row
            col_index = index % tiles_per_row
            top = row_index * tile_frame.shape[0]
            bottom = top + tile_frame.shape[0]
            left = col_index * tile_frame.shape[1]
            right = left + tile_frame.shape[1]
            merge_frame[top:bottom, left:right, :] = tile_frame
        merge_frame = merge_frame[size[1] : size[1] + temp_height, size[1]: size[1] + temp_width, :]
        return merge_frame


    def Run(self, temp_frame: Frame) -> Frame:
        size = (128, 8, 2)
        temp_height, temp_width = temp_frame.shape[:2]
        upscale_tile_frames, pad_width, pad_height = self.create_tile_frames(temp_frame, size)

        for index, tile_frame in enumerate(upscale_tile_frames):
            tile_frame = self.prepare_tile_frame(tile_frame)
            with conditional_thread_semaphore():
                self.io_binding.bind_cpu_input(self.model_inputs[0].name, tile_frame)
                self.model_upscale.run_with_iobinding(self.io_binding)
                ort_outs = self.io_binding.copy_outputs_to_cpu()
                result = ort_outs[0]
            upscale_tile_frames[index] = self.normalize_tile_frame(result)
        final_frame = self.merge_tile_frames(upscale_tile_frames, temp_width * self.scale
                                                    , temp_height * self.scale
                                                    , pad_width * self.scale, pad_height * self.scale
                                                    , (size[0] * self.scale, size[1] * self.scale, size[2] * self.scale))
        return final_frame.astype(np.uint8)



    def Release(self):
        del self.model_upscale
        self.model_upscale = None
        del self.io_binding
        self.io_binding = None


```

# roop\processors\Frame_Masking.py

```py
import cv2 
import numpy as np
import onnxruntime
import roop.globals

from roop.utilities import resolve_relative_path
from roop.typing import Frame

class Frame_Masking():
    plugin_options:dict = None
    model_masking = None
    devicename = None
    name = None

    processorname = 'removebg'
    type = 'frame_masking'
    

    def Initialize(self, plugin_options:dict):
        if self.plugin_options is not None:
            if self.plugin_options["devicename"] != plugin_options["devicename"]:
                self.Release()

        self.plugin_options = plugin_options
        if self.model_masking is None:
            # replace Mac mps with cpu for the moment
            self.devicename = self.plugin_options["devicename"]
            self.devicename = self.devicename.replace('mps', 'cpu')
            model_path = resolve_relative_path('../models/Frame/isnet-general-use.onnx')
            self.model_masking = onnxruntime.InferenceSession(model_path, None, providers=roop.globals.execution_providers)
            self.model_inputs = self.model_masking.get_inputs()
            model_outputs = self.model_masking.get_outputs()
            self.io_binding = self.model_masking.io_binding()
            self.io_binding.bind_output(model_outputs[0].name, self.devicename)

    def Run(self, temp_frame: Frame) -> Frame:
        # Pre process:Resize, BGR->RGB, float32 cast
        input_image = cv2.resize(temp_frame, (1024, 1024))
        input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
        mean = [0.5, 0.5, 0.5]
        std = [1.0, 1.0, 1.0]
        input_image = (input_image / 255.0 - mean) / std
        input_image = input_image.transpose(2, 0, 1)
        input_image = np.expand_dims(input_image, axis=0)
        input_image = input_image.astype('float32')
        
        self.io_binding.bind_cpu_input(self.model_inputs[0].name, input_image)
        self.model_masking.run_with_iobinding(self.io_binding)
        ort_outs = self.io_binding.copy_outputs_to_cpu()
        result = ort_outs[0][0]
        del ort_outs
        # Post process:squeeze, Sigmoid, Normarize, uint8 cast
        mask = np.squeeze(result[0])
        min_value = np.min(mask)
        max_value = np.max(mask)
        mask = (mask - min_value) / (max_value - min_value)
        #mask = np.where(mask < score_th, 0, 1)
        #mask *= 255
        mask = cv2.resize(mask, (temp_frame.shape[1], temp_frame.shape[0]), interpolation=cv2.INTER_LINEAR)        
        mask = np.reshape(mask, [mask.shape[0],mask.shape[1],1])
        result = mask * temp_frame.astype(np.float32)
        return result.astype(np.uint8)



    def Release(self):
        del self.model_masking
        self.model_masking = None
        del self.io_binding
        self.io_binding = None


```

# roop\processors\Frame_Filter.py

```py
import cv2
import numpy as np

from roop.typing import Frame

class Frame_Filter():
    processorname = 'generic_filter'
    type = 'frame_processor'

    plugin_options:dict = None

    c64_palette = np.array([
            [0, 0, 0],
            [255, 255, 255],
            [0x81, 0x33, 0x38],
            [0x75, 0xce, 0xc8],
            [0x8e, 0x3c, 0x97],
            [0x56, 0xac, 0x4d],
            [0x2e, 0x2c, 0x9b],
            [0xed, 0xf1, 0x71],
            [0x8e, 0x50, 0x29],
            [0x55, 0x38, 0x00],
            [0xc4, 0x6c, 0x71],
            [0x4a, 0x4a, 0x4a],
            [0x7b, 0x7b, 0x7b],
            [0xa9, 0xff, 0x9f],
            [0x70, 0x6d, 0xeb],
            [0xb2, 0xb2, 0xb2]
        ])


    def RenderC64Screen(self, image):
        # Simply round the color values to the nearest color in the palette
        image = cv2.resize(image,(320,200))
        palette = self.c64_palette / 255.0  # Normalize palette
        img_normalized = image  / 255.0  # Normalize image

        # Calculate the index in the palette that is closest to each pixel in the image
        indices = np.sqrt(((img_normalized[:, :, None, :] - palette[None, None, :, :]) ** 2).sum(axis=3)).argmin(axis=2)
        # Map the image to the palette colors
        mapped_image = palette[indices]
        return (mapped_image * 255).astype(np.uint8)  # Denormalize and return the image


    def RenderDetailEnhance(self, image):
        return cv2.detailEnhance(image)

    def RenderStylize(self, image):
        return cv2.stylization(image)
    
    def RenderPencilSketch(self, image):
        imgray, imout = cv2.pencilSketch(image, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
        return imout
    
    def RenderCartoon(self, image):
        numDownSamples = 2 # number of downscaling steps
        numBilateralFilters = 7  # number of bilateral filtering steps

        img_color = image
        for _ in range(numDownSamples):
            img_color = cv2.pyrDown(img_color)
        for _ in range(numBilateralFilters):
            img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
        for _ in range(numDownSamples):
            img_color = cv2.pyrUp(img_color)
        img_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        img_blur = cv2.medianBlur(img_gray, 7)
        img_edge = cv2.adaptiveThreshold(img_blur, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
        img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
        if img_color.shape != image.shape:
            img_color = cv2.resize(img_color, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_LINEAR)        
        if img_color.shape != img_edge.shape:
            img_edge = cv2.resize(img_edge, (img_color.shape[1], img_color.shape[0]), interpolation=cv2.INTER_LINEAR)        
        return cv2.bitwise_and(img_color, img_edge)
    

    def Initialize(self, plugin_options:dict):
        if self.plugin_options is not None:
            if self.plugin_options["devicename"] != plugin_options["devicename"]:
                self.Release()
        self.plugin_options = plugin_options

    def Run(self, temp_frame: Frame) -> Frame:
        subtype = self.plugin_options["subtype"]
        if subtype == "stylize":
            return self.RenderStylize(temp_frame).astype(np.uint8)
        if subtype == "detailenhance":
            return self.RenderDetailEnhance(temp_frame).astype(np.uint8)
        if subtype == "pencil":
            return self.RenderPencilSketch(temp_frame).astype(np.uint8)
        if subtype == "cartoon":
            return self.RenderCartoon(temp_frame).astype(np.uint8)
        if subtype == "C64":
            return self.RenderC64Screen(temp_frame).astype(np.uint8)


    def Release(self):
        pass

    def getProcessedResolution(self, width, height):
        if self.plugin_options["subtype"] == "C64":
            return (320,200)
        return None


```

# roop\processors\Frame_Colorizer.py

```py
import cv2 
import numpy as np
import onnxruntime
import roop.globals

from roop.utilities import resolve_relative_path
from roop.typing import Frame

class Frame_Colorizer():
    plugin_options:dict = None
    model_colorizer = None
    devicename = None
    prev_type = None

    processorname = 'deoldify'
    type = 'frame_colorizer'
    

    def Initialize(self, plugin_options:dict):
        if self.plugin_options is not None:
            if self.plugin_options["devicename"] != plugin_options["devicename"]:
                self.Release()

        self.plugin_options = plugin_options
        if self.prev_type is not None and self.prev_type != self.plugin_options["subtype"]:
            self.Release()
        self.prev_type = self.plugin_options["subtype"]
        if self.model_colorizer is None:
            # replace Mac mps with cpu for the moment
            self.devicename = self.plugin_options["devicename"].replace('mps', 'cpu')
            if self.prev_type == "deoldify_artistic":
                model_path = resolve_relative_path('../models/Frame/deoldify_artistic.onnx')
            elif self.prev_type == "deoldify_stable":
                model_path = resolve_relative_path('../models/Frame/deoldify_stable.onnx')

            onnxruntime.set_default_logger_severity(3)
            self.model_colorizer = onnxruntime.InferenceSession(model_path, None, providers=roop.globals.execution_providers)
            self.model_inputs = self.model_colorizer.get_inputs()
            model_outputs = self.model_colorizer.get_outputs()
            self.io_binding = self.model_colorizer.io_binding()
            self.io_binding.bind_output(model_outputs[0].name, self.devicename)

    def Run(self, input_frame: Frame) -> Frame:
        temp_frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2GRAY)
        temp_frame = cv2.cvtColor(temp_frame, cv2.COLOR_GRAY2RGB)
        temp_frame = cv2.resize(temp_frame, (256, 256))
        temp_frame = temp_frame.transpose((2, 0, 1))
        temp_frame = np.expand_dims(temp_frame, axis=0).astype(np.float32)
        self.io_binding.bind_cpu_input(self.model_inputs[0].name, temp_frame)
        self.model_colorizer.run_with_iobinding(self.io_binding)
        ort_outs = self.io_binding.copy_outputs_to_cpu()
        result = ort_outs[0][0]
        del ort_outs
        colorized_frame = result.transpose(1, 2, 0)
        colorized_frame = cv2.resize(colorized_frame, (input_frame.shape[1], input_frame.shape[0]))
        temp_blue_channel, _, _ = cv2.split(input_frame)
        colorized_frame = cv2.cvtColor(colorized_frame, cv2.COLOR_BGR2RGB).astype(np.uint8)
        colorized_frame = cv2.cvtColor(colorized_frame, cv2.COLOR_BGR2LAB)
        _, color_green_channel, color_red_channel = cv2.split(colorized_frame)
        colorized_frame = cv2.merge((temp_blue_channel, color_green_channel, color_red_channel))
        colorized_frame = cv2.cvtColor(colorized_frame, cv2.COLOR_LAB2BGR)
        return colorized_frame.astype(np.uint8)


    def Release(self):
        del self.model_colorizer
        self.model_colorizer = None
        del self.io_binding
        self.io_binding = None


```

# roop\processors\FaceSwapInsightFace.py

```py
import roop.globals
import cv2
import numpy as np
import onnx
import onnxruntime

from roop.typing import Face, Frame
from roop.utilities import resolve_relative_path



class FaceSwapInsightFace():
    plugin_options:dict = None
    model_swap_insightface = None

    processorname = 'faceswap'
    type = 'swap'


    def Initialize(self, plugin_options:dict):
        if self.plugin_options is not None:
            if self.plugin_options["devicename"] != plugin_options["devicename"]:
                self.Release()

        self.plugin_options = plugin_options
        if self.model_swap_insightface is None:
            model_path = resolve_relative_path('../models/inswapper_128.onnx')
            graph = onnx.load(model_path).graph
            self.emap = onnx.numpy_helper.to_array(graph.initializer[-1])
            self.devicename = self.plugin_options["devicename"].replace('mps', 'cpu')
            self.input_mean = 0.0
            self.input_std = 255.0
            #cuda_options = {"arena_extend_strategy": "kSameAsRequested", 'cudnn_conv_algo_search': 'DEFAULT'}            
            sess_options = onnxruntime.SessionOptions()
            sess_options.enable_cpu_mem_arena = False
            self.model_swap_insightface = onnxruntime.InferenceSession(model_path, sess_options, providers=roop.globals.execution_providers)



    def Run(self, source_face: Face, target_face: Face, temp_frame: Frame) -> Frame:
        latent = source_face.normed_embedding.reshape((1,-1))
        latent = np.dot(latent, self.emap)
        latent /= np.linalg.norm(latent)
        io_binding = self.model_swap_insightface.io_binding()           
        io_binding.bind_cpu_input("target", temp_frame)
        io_binding.bind_cpu_input("source", latent)
        io_binding.bind_output("output", self.devicename)
        self.model_swap_insightface.run_with_iobinding(io_binding)
        ort_outs = io_binding.copy_outputs_to_cpu()[0]
        return ort_outs[0]


    def Release(self):
        del self.model_swap_insightface
        self.model_swap_insightface = None


                




```

# roop\processors\Enhance_RestoreFormerPPlus.py

```py
from typing import Any, List, Callable
import cv2 
import numpy as np
import onnxruntime
import roop.globals

from roop.typing import Face, Frame, FaceSet
from roop.utilities import resolve_relative_path

class Enhance_RestoreFormerPPlus():
    plugin_options:dict = None
    model_restoreformerpplus = None
    devicename = None
    name = None

    processorname = 'restoreformer++'
    type = 'enhance'
    

    def Initialize(self, plugin_options:dict):
        if self.plugin_options is not None:
            if self.plugin_options["devicename"] != plugin_options["devicename"]:
                self.Release()

        self.plugin_options = plugin_options
        if self.model_restoreformerpplus is None:
            # replace Mac mps with cpu for the moment
            self.devicename = self.plugin_options["devicename"].replace('mps', 'cpu')
            model_path = resolve_relative_path('../models/restoreformer_plus_plus.onnx')
            self.model_restoreformerpplus = onnxruntime.InferenceSession(model_path, None, providers=roop.globals.execution_providers)
            self.model_inputs = self.model_restoreformerpplus.get_inputs()
            model_outputs = self.model_restoreformerpplus.get_outputs()
            self.io_binding = self.model_restoreformerpplus.io_binding()
            self.io_binding.bind_output(model_outputs[0].name, self.devicename)

    def Run(self, source_faceset: FaceSet, target_face: Face, temp_frame: Frame) -> Frame:
        # preprocess
        input_size = temp_frame.shape[1]
        temp_frame = cv2.resize(temp_frame, (512, 512), cv2.INTER_CUBIC)
        temp_frame = cv2.cvtColor(temp_frame, cv2.COLOR_BGR2RGB)
        temp_frame = temp_frame.astype('float32') / 255.0
        temp_frame = (temp_frame - 0.5) / 0.5
        temp_frame = np.expand_dims(temp_frame, axis=0).transpose(0, 3, 1, 2)
        
        self.io_binding.bind_cpu_input(self.model_inputs[0].name, temp_frame) # .astype(np.float32)
        self.model_restoreformerpplus.run_with_iobinding(self.io_binding)
        ort_outs = self.io_binding.copy_outputs_to_cpu()
        result = ort_outs[0][0]
        del ort_outs 
        
        result = np.clip(result, -1, 1)
        result = (result + 1) / 2
        result = result.transpose(1, 2, 0) * 255.0
        result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
        scale_factor = int(result.shape[1] / input_size)       
        return result.astype(np.uint8), scale_factor


    def Release(self):
        del self.model_restoreformerpplus
        self.model_restoreformerpplus = None
        del self.io_binding
        self.io_binding = None


```

# roop\processors\Enhance_GPEN.py

```py
from typing import Any, List, Callable
import cv2 
import numpy as np
import onnxruntime
import roop.globals

from roop.typing import Face, Frame, FaceSet
from roop.utilities import resolve_relative_path


class Enhance_GPEN():
    plugin_options:dict = None

    model_gpen = None
    name = None
    devicename = None

    processorname = 'gpen'
    type = 'enhance'


    def Initialize(self, plugin_options:dict):
        if self.plugin_options is not None:
            if self.plugin_options["devicename"] != plugin_options["devicename"]:
                self.Release()

        self.plugin_options = plugin_options
        if self.model_gpen is None:
            model_path = resolve_relative_path('../models/GPEN-BFR-512.onnx')
            self.model_gpen = onnxruntime.InferenceSession(model_path, None, providers=roop.globals.execution_providers)
            # replace Mac mps with cpu for the moment
            self.devicename = self.plugin_options["devicename"].replace('mps', 'cpu')

        self.name = self.model_gpen.get_inputs()[0].name

    def Run(self, source_faceset: FaceSet, target_face: Face, temp_frame: Frame) -> Frame:
        # preprocess
        input_size = temp_frame.shape[1]
        temp_frame = cv2.resize(temp_frame, (512, 512), cv2.INTER_CUBIC)

        temp_frame = cv2.cvtColor(temp_frame, cv2.COLOR_BGR2RGB)
        temp_frame = temp_frame.astype('float32') / 255.0
        temp_frame = (temp_frame - 0.5) / 0.5
        temp_frame = np.expand_dims(temp_frame, axis=0).transpose(0, 3, 1, 2)

        io_binding = self.model_gpen.io_binding()           
        io_binding.bind_cpu_input("input", temp_frame)
        io_binding.bind_output("output", self.devicename)
        self.model_gpen.run_with_iobinding(io_binding)
        ort_outs = io_binding.copy_outputs_to_cpu()
        result = ort_outs[0][0]

        # post-process
        result = np.clip(result, -1, 1)
        result = (result + 1) / 2
        result = result.transpose(1, 2, 0) * 255.0
        result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
        scale_factor = int(result.shape[1] / input_size)       
        return result.astype(np.uint8), scale_factor


    def Release(self):
        self.model_gpen = None

```

# roop\processors\Enhance_GFPGAN.py

```py
from typing import Any, List, Callable
import cv2 
import numpy as np
import onnxruntime
import roop.globals

from roop.typing import Face, Frame, FaceSet
from roop.utilities import resolve_relative_path

class Enhance_GFPGAN():
    plugin_options:dict = None

    model_gfpgan = None
    name = None
    devicename = None

    processorname = 'gfpgan'
    type = 'enhance'


    def Initialize(self, plugin_options:dict):
        if self.plugin_options is not None:
            if self.plugin_options["devicename"] != plugin_options["devicename"]:
                self.Release()

        self.plugin_options = plugin_options
        if self.model_gfpgan is None:
            model_path = resolve_relative_path('../models/GFPGANv1.4.onnx')
            self.model_gfpgan = onnxruntime.InferenceSession(model_path, None, providers=roop.globals.execution_providers)
            # replace Mac mps with cpu for the moment
            self.devicename = self.plugin_options["devicename"].replace('mps', 'cpu')

        self.name = self.model_gfpgan.get_inputs()[0].name

    def Run(self, source_faceset: FaceSet, target_face: Face, temp_frame: Frame) -> Frame:
        # preprocess
        input_size = temp_frame.shape[1]
        temp_frame = cv2.resize(temp_frame, (512, 512), cv2.INTER_CUBIC)

        temp_frame = cv2.cvtColor(temp_frame, cv2.COLOR_BGR2RGB)
        temp_frame = temp_frame.astype('float32') / 255.0
        temp_frame = (temp_frame - 0.5) / 0.5
        temp_frame = np.expand_dims(temp_frame, axis=0).transpose(0, 3, 1, 2)

        io_binding = self.model_gfpgan.io_binding()           
        io_binding.bind_cpu_input("input", temp_frame)
        io_binding.bind_output("1288", self.devicename)
        self.model_gfpgan.run_with_iobinding(io_binding)
        ort_outs = io_binding.copy_outputs_to_cpu()
        result = ort_outs[0][0]

        # post-process
        result = np.clip(result, -1, 1)
        result = (result + 1) / 2
        result = result.transpose(1, 2, 0) * 255.0
        result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
        scale_factor = int(result.shape[1] / input_size)       
        return result.astype(np.uint8), scale_factor


    def Release(self):
        self.model_gfpgan = None












```

# roop\processors\Enhance_DMDNet.py

```py
from typing import Any, List, Callable
import cv2 
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.utils.spectral_norm as SpectralNorm
import threading
from torchvision.ops import roi_align

from math import sqrt

from torchvision.transforms.functional import normalize

from roop.typing import Face, Frame, FaceSet


THREAD_LOCK_DMDNET = threading.Lock()


class Enhance_DMDNet():
    plugin_options:dict = None
    model_dmdnet = None
    torchdevice = None

    processorname = 'dmdnet'
    type = 'enhance'


    def Initialize(self, plugin_options:dict):
        if self.plugin_options is not None:
            if self.plugin_options["devicename"] != plugin_options["devicename"]:
                self.Release()

        self.plugin_options = plugin_options
        if self.model_dmdnet is None:
            self.model_dmdnet = self.create(self.plugin_options["devicename"])
            

    # temp_frame already cropped+aligned, bbox not
    def Run(self, source_faceset: FaceSet, target_face: Face, temp_frame: Frame) -> Frame:
        input_size = temp_frame.shape[1]

        result = self.enhance_face(source_faceset, temp_frame, target_face)
        scale_factor = int(result.shape[1] / input_size)       
        return result.astype(np.uint8), scale_factor


    def Release(self):
        self.model_gfpgan = None


    # https://stackoverflow.com/a/67174339
    def landmarks106_to_68(self, pt106):
        map106to68=[1,10,12,14,16,3,5,7,0,23,21,19,32,30,28,26,17,
                        43,48,49,51,50,
                        102,103,104,105,101,
                        72,73,74,86,78,79,80,85,84,
                        35,41,42,39,37,36,
                        89,95,96,93,91,90,
                        52,64,63,71,67,68,61,58,59,53,56,55,65,66,62,70,69,57,60,54
                        ]
      
        pt68 = []
        for i in range(68):
            index = map106to68[i]
            pt68.append(pt106[index])
        return pt68

        


    def check_bbox(self, imgs, boxes):
        boxes = boxes.view(-1, 4, 4)
        colors = [(0, 255, 0), (0, 255, 0), (255, 255, 0), (255, 0, 0)]
        i = 0
        for img, box in zip(imgs, boxes):
            img = (img + 1)/2 * 255
            img2 = img.permute(1, 2, 0).float().cpu().flip(2).numpy().copy()
            for idx, point in enumerate(box):
                cv2.rectangle(img2, (int(point[0]), int(point[1])), (int(point[2]), int(point[3])), color=colors[idx], thickness=2)
            cv2.imwrite('dmdnet_{:02d}.png'.format(i), img2)
            i += 1


    def trans_points2d(self, pts, M):
        new_pts = np.zeros(shape=pts.shape, dtype=np.float32)
        for i in range(pts.shape[0]):
            pt = pts[i]
            new_pt = np.array([pt[0], pt[1], 1.0], dtype=np.float32)
            new_pt = np.dot(M, new_pt)
            new_pts[i] = new_pt[0:2]

        return new_pts


    def enhance_face(self, ref_faceset: FaceSet, temp_frame, face: Face):
        # preprocess
        start_x, start_y, end_x, end_y = map(int, face['bbox'])
        lm106 = face.landmark_2d_106
        lq_landmarks = np.asarray(self.landmarks106_to_68(lm106))

        if temp_frame.shape[0] != 512 or temp_frame.shape[1] != 512:
            # scale to 512x512
            scale_factor = 512 / temp_frame.shape[1]

            M = face.matrix * scale_factor

            lq_landmarks = self.trans_points2d(lq_landmarks, M)
            temp_frame = cv2.resize(temp_frame, (512,512), interpolation = cv2.INTER_AREA)

        if temp_frame.ndim == 2:
            temp_frame = cv2.cvtColor(temp_frame, cv2.COLOR_GRAY2RGB)  # GGG
        # else:
        #     temp_frame = cv2.cvtColor(temp_frame, cv2.COLOR_BGR2RGB)  # RGB

        lq = read_img_tensor(temp_frame)

        LQLocs = get_component_location(lq_landmarks)
        # self.check_bbox(lq, LQLocs.unsqueeze(0))

        # specific, change 1000 to 1 to activate
        if len(ref_faceset.faces) > 1:
            SpecificImgs = []
            SpecificLocs = []
            for i,face in enumerate(ref_faceset.faces):
                lm106 = face.landmark_2d_106
                lq_landmarks = np.asarray(self.landmarks106_to_68(lm106))
                ref_image = ref_faceset.ref_images[i]
                if ref_image.shape[0] != 512 or ref_image.shape[1] != 512:
                    # scale to 512x512
                    scale_factor = 512 / ref_image.shape[1]

                    M = face.matrix * scale_factor

                    lq_landmarks = self.trans_points2d(lq_landmarks, M)
                    ref_image = cv2.resize(ref_image, (512,512), interpolation = cv2.INTER_AREA)

                if ref_image.ndim == 2:
                    temp_frame = cv2.cvtColor(temp_frame, cv2.COLOR_GRAY2RGB)  # GGG
                # else:
                #     temp_frame = cv2.cvtColor(temp_frame, cv2.COLOR_BGR2RGB)  # RGB

                ref_tensor = read_img_tensor(ref_image)
                ref_locs = get_component_location(lq_landmarks)
                # self.check_bbox(ref_tensor, ref_locs.unsqueeze(0))

                SpecificImgs.append(ref_tensor)
                SpecificLocs.append(ref_locs.unsqueeze(0))

            SpecificImgs = torch.cat(SpecificImgs, dim=0)
            SpecificLocs = torch.cat(SpecificLocs, dim=0)
            # check_bbox(SpecificImgs, SpecificLocs)
            SpMem256, SpMem128, SpMem64 = self.model_dmdnet.generate_specific_dictionary(sp_imgs = SpecificImgs.to(self.torchdevice), sp_locs = SpecificLocs)
            SpMem256Para = {}
            SpMem128Para = {}
            SpMem64Para = {}
            for k, v in SpMem256.items():
                SpMem256Para[k] = v
            for k, v in SpMem128.items():
                SpMem128Para[k] = v
            for k, v in SpMem64.items():
                SpMem64Para[k] = v
        else:
            # generic
            SpMem256Para, SpMem128Para, SpMem64Para = None, None, None

        with torch.no_grad():
            with THREAD_LOCK_DMDNET:
                try:
                    GenericResult, SpecificResult = self.model_dmdnet(lq = lq.to(self.torchdevice), loc = LQLocs.unsqueeze(0), sp_256 = SpMem256Para, sp_128 = SpMem128Para, sp_64 = SpMem64Para)
                except Exception as e:
                    print(f'Error {e} there may be something wrong with the detected component locations.')
                    return temp_frame
        
        if SpecificResult is not None:
            save_specific = SpecificResult * 0.5 + 0.5
            save_specific = save_specific.squeeze(0).permute(1, 2, 0).flip(2) # RGB->BGR
            save_specific = np.clip(save_specific.float().cpu().numpy(), 0, 1) * 255.0
            temp_frame =  save_specific.astype("uint8")
            if False:
                save_generic = GenericResult * 0.5 + 0.5
                save_generic = save_generic.squeeze(0).permute(1, 2, 0).flip(2) # RGB->BGR
                save_generic = np.clip(save_generic.float().cpu().numpy(), 0, 1) * 255.0
                check_lq = lq * 0.5 + 0.5
                check_lq = check_lq.squeeze(0).permute(1, 2, 0).flip(2) # RGB->BGR
                check_lq = np.clip(check_lq.float().cpu().numpy(), 0, 1) * 255.0
                cv2.imwrite('dmdnet_comparison.png', cv2.cvtColor(np.hstack((check_lq, save_generic, save_specific)),cv2.COLOR_RGB2BGR))
        else:
            save_generic = GenericResult * 0.5 + 0.5
            save_generic = save_generic.squeeze(0).permute(1, 2, 0).flip(2) # RGB->BGR
            save_generic = np.clip(save_generic.float().cpu().numpy(), 0, 1) * 255.0
            temp_frame =  save_generic.astype("uint8")
        temp_frame = cv2.cvtColor(temp_frame, cv2.COLOR_RGB2BGR)  # RGB
        return temp_frame

    

    def create(self, devicename):
        self.torchdevice = torch.device(devicename)
        model_dmdnet = DMDNet().to(self.torchdevice)
        weights = torch.load('./models/DMDNet.pth') 
        model_dmdnet.load_state_dict(weights, strict=True)

        model_dmdnet.eval()
        num_params = 0
        for param in model_dmdnet.parameters():
            num_params += param.numel()
        return model_dmdnet

    # print('{:>8s} : {}'.format('Using device', device))
    # print('{:>8s} : {:.2f}M'.format('Model params', num_params/1e6))



def read_img_tensor(Img=None): #rgb -1~1 
    Img = Img.transpose((2, 0, 1))/255.0
    Img = torch.from_numpy(Img).float()
    normalize(Img, [0.5,0.5,0.5], [0.5,0.5,0.5], inplace=True)
    ImgTensor = Img.unsqueeze(0)
    return ImgTensor


def get_component_location(Landmarks, re_read=False):
    if re_read:
        ReadLandmark = []
        with open(Landmarks,'r') as f:
            for line in f:
                tmp = [float(i) for i in line.split(' ') if i != '\n']
                ReadLandmark.append(tmp)
        ReadLandmark = np.array(ReadLandmark) #
        Landmarks = np.reshape(ReadLandmark, [-1, 2]) # 68*2
    Map_LE_B = list(np.hstack((range(17,22), range(36,42))))
    Map_RE_B = list(np.hstack((range(22,27), range(42,48))))
    Map_LE = list(range(36,42))
    Map_RE = list(range(42,48))
    Map_NO = list(range(29,36))
    Map_MO = list(range(48,68))

    Landmarks[Landmarks>504]=504
    Landmarks[Landmarks<8]=8
    
    #left eye
    Mean_LE = np.mean(Landmarks[Map_LE],0)
    L_LE1 = Mean_LE[1] - np.min(Landmarks[Map_LE_B,1])
    L_LE1 = L_LE1 * 1.3
    L_LE2 = L_LE1 / 1.9
    L_LE_xy = L_LE1 + L_LE2
    L_LE_lt = [L_LE_xy/2, L_LE1]
    L_LE_rb = [L_LE_xy/2, L_LE2]
    Location_LE = np.hstack((Mean_LE - L_LE_lt + 1, Mean_LE + L_LE_rb)).astype(int)

    #right eye
    Mean_RE = np.mean(Landmarks[Map_RE],0)
    L_RE1 = Mean_RE[1] - np.min(Landmarks[Map_RE_B,1])
    L_RE1 = L_RE1 * 1.3
    L_RE2 = L_RE1 / 1.9
    L_RE_xy = L_RE1 + L_RE2
    L_RE_lt = [L_RE_xy/2, L_RE1]
    L_RE_rb = [L_RE_xy/2, L_RE2]
    Location_RE = np.hstack((Mean_RE - L_RE_lt + 1, Mean_RE + L_RE_rb)).astype(int)

    #nose
    Mean_NO = np.mean(Landmarks[Map_NO],0)
    L_NO1 =( np.max([Mean_NO[0] - Landmarks[31][0], Landmarks[35][0] - Mean_NO[0]])) * 1.25
    L_NO2 = (Landmarks[33][1] - Mean_NO[1]) * 1.1
    L_NO_xy = L_NO1 * 2
    L_NO_lt = [L_NO_xy/2, L_NO_xy - L_NO2]
    L_NO_rb = [L_NO_xy/2, L_NO2]
    Location_NO = np.hstack((Mean_NO - L_NO_lt + 1, Mean_NO + L_NO_rb)).astype(int)
    
    #mouth
    Mean_MO = np.mean(Landmarks[Map_MO],0)
    L_MO = np.max((np.max(np.max(Landmarks[Map_MO],0) - np.min(Landmarks[Map_MO],0))/2,16)) * 1.1
    MO_O = Mean_MO - L_MO + 1
    MO_T = Mean_MO + L_MO
    MO_T[MO_T>510]=510
    Location_MO = np.hstack((MO_O, MO_T)).astype(int)
    return torch.cat([torch.FloatTensor(Location_LE).unsqueeze(0), torch.FloatTensor(Location_RE).unsqueeze(0), torch.FloatTensor(Location_NO).unsqueeze(0), torch.FloatTensor(Location_MO).unsqueeze(0)], dim=0)




def calc_mean_std_4D(feat, eps=1e-5):
    # eps is a small value added to the variance to avoid divide-by-zero.
    size = feat.size()
    assert (len(size) == 4)
    N, C = size[:2]
    feat_var = feat.view(N, C, -1).var(dim=2) + eps
    feat_std = feat_var.sqrt().view(N, C, 1, 1)
    feat_mean = feat.view(N, C, -1).mean(dim=2).view(N, C, 1, 1)
    return feat_mean, feat_std

def adaptive_instance_normalization_4D(content_feat, style_feat): # content_feat is ref feature, style is degradate feature
    size = content_feat.size()
    style_mean, style_std = calc_mean_std_4D(style_feat)
    content_mean, content_std = calc_mean_std_4D(content_feat)
    normalized_feat = (content_feat - content_mean.expand(size)) / content_std.expand(size)
    return normalized_feat * style_std.expand(size) + style_mean.expand(size)


def convU(in_channels, out_channels,conv_layer, norm_layer, kernel_size=3, stride=1,dilation=1, bias=True):
    return nn.Sequential(
        SpectralNorm(conv_layer(in_channels, out_channels, kernel_size=kernel_size, stride=stride, dilation=dilation, padding=((kernel_size-1)//2)*dilation, bias=bias)),
        nn.LeakyReLU(0.2),
        SpectralNorm(conv_layer(out_channels, out_channels, kernel_size=kernel_size, stride=stride, dilation=dilation, padding=((kernel_size-1)//2)*dilation, bias=bias)),
    )
    

class MSDilateBlock(nn.Module):
    def __init__(self, in_channels,conv_layer=nn.Conv2d, norm_layer=nn.BatchNorm2d, kernel_size=3, dilation=[1,1,1,1], bias=True):
        super(MSDilateBlock, self).__init__()
        self.conv1 =  convU(in_channels, in_channels,conv_layer, norm_layer, kernel_size,dilation=dilation[0], bias=bias)
        self.conv2 =  convU(in_channels, in_channels,conv_layer, norm_layer, kernel_size,dilation=dilation[1], bias=bias)
        self.conv3 =  convU(in_channels, in_channels,conv_layer, norm_layer, kernel_size,dilation=dilation[2], bias=bias)
        self.conv4 =  convU(in_channels, in_channels,conv_layer, norm_layer, kernel_size,dilation=dilation[3], bias=bias)
        self.convi =  SpectralNorm(conv_layer(in_channels*4, in_channels, kernel_size=kernel_size, stride=1, padding=(kernel_size-1)//2, bias=bias))
    def forward(self, x):
        conv1 = self.conv1(x)
        conv2 = self.conv2(x)
        conv3 = self.conv3(x)
        conv4 = self.conv4(x)
        cat  = torch.cat([conv1, conv2, conv3, conv4], 1)
        out = self.convi(cat) + x
        return out


class AdaptiveInstanceNorm(nn.Module):
    def __init__(self, in_channel):
        super().__init__()
        self.norm = nn.InstanceNorm2d(in_channel)

    def forward(self, input, style):
        style_mean, style_std = calc_mean_std_4D(style)
        out = self.norm(input)
        size = input.size()
        out = style_std.expand(size) * out + style_mean.expand(size)
        return out

class NoiseInjection(nn.Module):
    def __init__(self, channel):
        super().__init__()
        self.weight = nn.Parameter(torch.zeros(1, channel, 1, 1))
    def forward(self, image, noise):
        if noise is None:
            b, c, h, w = image.shape
            noise = image.new_empty(b, 1, h, w).normal_()
        return image + self.weight * noise

class StyledUpBlock(nn.Module):
    def __init__(self, in_channel, out_channel, kernel_size=3, padding=1,upsample=False, noise_inject=False):
        super().__init__()

        self.noise_inject = noise_inject
        if upsample:
            self.conv1 = nn.Sequential(
                nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False),
                SpectralNorm(nn.Conv2d(in_channel, out_channel, kernel_size, padding=padding)),
                nn.LeakyReLU(0.2),
            )
        else:
            self.conv1 = nn.Sequential(
                SpectralNorm(nn.Conv2d(in_channel, out_channel, kernel_size, padding=padding)),
                nn.LeakyReLU(0.2),
                SpectralNorm(nn.Conv2d(out_channel, out_channel, kernel_size, padding=padding)),
            )
        self.convup = nn.Sequential(
                nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False),
                SpectralNorm(nn.Conv2d(out_channel, out_channel, kernel_size, padding=padding)),
                nn.LeakyReLU(0.2),
                SpectralNorm(nn.Conv2d(out_channel, out_channel, kernel_size, padding=padding)),
            )
        if self.noise_inject:
            self.noise1 = NoiseInjection(out_channel)

        self.lrelu1 = nn.LeakyReLU(0.2)

        self.ScaleModel1 = nn.Sequential(
            SpectralNorm(nn.Conv2d(in_channel,out_channel,3, 1, 1)),
            nn.LeakyReLU(0.2),
            SpectralNorm(nn.Conv2d(out_channel, out_channel, 3, 1, 1))
        )
        self.ShiftModel1 = nn.Sequential(
            SpectralNorm(nn.Conv2d(in_channel,out_channel,3, 1, 1)),
            nn.LeakyReLU(0.2),
            SpectralNorm(nn.Conv2d(out_channel, out_channel, 3, 1, 1)),
        )
       
    def forward(self, input, style):
        out = self.conv1(input)
        out = self.lrelu1(out)
        Shift1 = self.ShiftModel1(style)
        Scale1 = self.ScaleModel1(style)
        out = out * Scale1 + Shift1
        if self.noise_inject:
            out = self.noise1(out, noise=None)
        outup = self.convup(out)
        return outup


####################################################################
###############Face Dictionary Generator
####################################################################
def AttentionBlock(in_channel):
    return nn.Sequential(
        SpectralNorm(nn.Conv2d(in_channel, in_channel, 3, 1, 1)),
        nn.LeakyReLU(0.2),
        SpectralNorm(nn.Conv2d(in_channel, in_channel, 3, 1, 1)),
    )

class DilateResBlock(nn.Module):
    def __init__(self, dim, dilation=[5,3] ):
        super(DilateResBlock, self).__init__()
        self.Res = nn.Sequential(
            SpectralNorm(nn.Conv2d(dim, dim, 3, 1, ((3-1)//2)*dilation[0], dilation[0])),
            nn.LeakyReLU(0.2),
            SpectralNorm(nn.Conv2d(dim, dim, 3, 1, ((3-1)//2)*dilation[1], dilation[1])),
        )
    def forward(self, x):
        out = x + self.Res(x)
        return out


class KeyValue(nn.Module):
    def __init__(self, indim, keydim, valdim):
        super(KeyValue, self).__init__()
        self.Key = nn.Sequential(
            SpectralNorm(nn.Conv2d(indim, keydim, kernel_size=(3,3), padding=(1,1), stride=1)),
            nn.LeakyReLU(0.2),
            SpectralNorm(nn.Conv2d(keydim, keydim, kernel_size=(3,3), padding=(1,1), stride=1)),
        )
        self.Value = nn.Sequential(
            SpectralNorm(nn.Conv2d(indim, valdim, kernel_size=(3,3), padding=(1,1), stride=1)),
            nn.LeakyReLU(0.2),
            SpectralNorm(nn.Conv2d(valdim, valdim, kernel_size=(3,3), padding=(1,1), stride=1)),
        )
    def forward(self, x):  
        return self.Key(x), self.Value(x)

class MaskAttention(nn.Module):
    def __init__(self, indim):
        super(MaskAttention, self).__init__()
        self.conv1 = nn.Sequential(
            SpectralNorm(nn.Conv2d(indim, indim//3, kernel_size=(3,3), padding=(1,1), stride=1)),
            nn.LeakyReLU(0.2),
            SpectralNorm(nn.Conv2d(indim//3, indim//3, kernel_size=(3,3), padding=(1,1), stride=1)),
        )
        self.conv2 = nn.Sequential(
            SpectralNorm(nn.Conv2d(indim, indim//3, kernel_size=(3,3), padding=(1,1), stride=1)),
            nn.LeakyReLU(0.2),
            SpectralNorm(nn.Conv2d(indim//3, indim//3, kernel_size=(3,3), padding=(1,1), stride=1)),
        )
        self.conv3 = nn.Sequential(
            SpectralNorm(nn.Conv2d(indim, indim//3, kernel_size=(3,3), padding=(1,1), stride=1)),
            nn.LeakyReLU(0.2),
            SpectralNorm(nn.Conv2d(indim//3, indim//3, kernel_size=(3,3), padding=(1,1), stride=1)),
        )
        self.convCat = nn.Sequential(
            SpectralNorm(nn.Conv2d(indim//3 * 3, indim, kernel_size=(3,3), padding=(1,1), stride=1)),
            nn.LeakyReLU(0.2),
            SpectralNorm(nn.Conv2d(indim, indim, kernel_size=(3,3), padding=(1,1), stride=1)),
        )
    def forward(self, x, y, z):
        c1 = self.conv1(x)
        c2 = self.conv2(y)
        c3 = self.conv3(z)
        return self.convCat(torch.cat([c1,c2,c3], dim=1))

class Query(nn.Module):
    def __init__(self, indim, quedim):
        super(Query, self).__init__()
        self.Query = nn.Sequential(
            SpectralNorm(nn.Conv2d(indim, quedim, kernel_size=(3,3), padding=(1,1), stride=1)),
            nn.LeakyReLU(0.2),
            SpectralNorm(nn.Conv2d(quedim, quedim, kernel_size=(3,3), padding=(1,1), stride=1)),
        )
    def forward(self, x):
        return self.Query(x)

def roi_align_self(input, location, target_size):
    test = (target_size.item(),target_size.item())
    return torch.cat([F.interpolate(input[i:i+1,:,location[i,1]:location[i,3],location[i,0]:location[i,2]],test,mode='bilinear',align_corners=False) for i in range(input.size(0))],0)

class FeatureExtractor(nn.Module):
    def __init__(self, ngf = 64, key_scale = 4):#
        super().__init__()

        self.key_scale = 4
        self.part_sizes = np.array([80,80,50,110]) #
        self.feature_sizes = np.array([256,128,64]) # 

        self.conv1 = nn.Sequential(
                SpectralNorm(nn.Conv2d(3, ngf, 3, 2, 1)),
                nn.LeakyReLU(0.2),
                SpectralNorm(nn.Conv2d(ngf, ngf, 3, 1, 1)),
            )
        self.conv2 = nn.Sequential(
            SpectralNorm(nn.Conv2d(ngf, ngf, 3, 1, 1)),
            nn.LeakyReLU(0.2),
            SpectralNorm(nn.Conv2d(ngf, ngf, 3, 1, 1))
        )
        self.res1 = DilateResBlock(ngf, [5,3])
        self.res2 = DilateResBlock(ngf, [5,3])

        
        self.conv3 = nn.Sequential(
            SpectralNorm(nn.Conv2d(ngf, ngf*2, 3, 2, 1)),
            nn.LeakyReLU(0.2),
            SpectralNorm(nn.Conv2d(ngf*2, ngf*2, 3, 1, 1)),
            )
        self.conv4 = nn.Sequential(
            SpectralNorm(nn.Conv2d(ngf*2, ngf*2, 3, 1, 1)),
            nn.LeakyReLU(0.2),
            SpectralNorm(nn.Conv2d(ngf*2, ngf*2, 3, 1, 1))
        )
        self.res3 = DilateResBlock(ngf*2, [3,1])
        self.res4 = DilateResBlock(ngf*2, [3,1])

        self.conv5 = nn.Sequential(
            SpectralNorm(nn.Conv2d(ngf*2, ngf*4, 3, 2, 1)),
            nn.LeakyReLU(0.2),
            SpectralNorm(nn.Conv2d(ngf*4, ngf*4, 3, 1, 1)),
        )
        self.conv6 = nn.Sequential(
            SpectralNorm(nn.Conv2d(ngf*4, ngf*4, 3, 1, 1)),
            nn.LeakyReLU(0.2),
            SpectralNorm(nn.Conv2d(ngf*4, ngf*4, 3, 1, 1))
        )
        self.res5 = DilateResBlock(ngf*4, [1,1])
        self.res6 = DilateResBlock(ngf*4, [1,1])

        self.LE_256_Q = Query(ngf, ngf // self.key_scale)
        self.RE_256_Q = Query(ngf, ngf // self.key_scale)
        self.MO_256_Q = Query(ngf, ngf // self.key_scale)
        self.LE_128_Q = Query(ngf * 2, ngf * 2 // self.key_scale)
        self.RE_128_Q = Query(ngf * 2, ngf * 2 // self.key_scale)
        self.MO_128_Q = Query(ngf * 2, ngf * 2 // self.key_scale)
        self.LE_64_Q = Query(ngf * 4, ngf * 4 // self.key_scale)
        self.RE_64_Q = Query(ngf * 4, ngf * 4 // self.key_scale)
        self.MO_64_Q = Query(ngf * 4, ngf * 4 // self.key_scale)


    def forward(self, img, locs):
        le_location = locs[:,0,:].int().cpu().numpy()
        re_location = locs[:,1,:].int().cpu().numpy()
        no_location = locs[:,2,:].int().cpu().numpy()
        mo_location = locs[:,3,:].int().cpu().numpy()
        

        f1_0 = self.conv1(img) 
        f1_1 = self.res1(f1_0)
        f2_0 = self.conv2(f1_1)
        f2_1 = self.res2(f2_0)

        f3_0 = self.conv3(f2_1) 
        f3_1 = self.res3(f3_0)
        f4_0 = self.conv4(f3_1)
        f4_1 = self.res4(f4_0)

        f5_0 = self.conv5(f4_1) 
        f5_1 = self.res5(f5_0)
        f6_0 = self.conv6(f5_1)
        f6_1 = self.res6(f6_0)


        ####ROI Align
        le_part_256 = roi_align_self(f2_1.clone(), le_location//2, self.part_sizes[0]//2)
        re_part_256 = roi_align_self(f2_1.clone(), re_location//2, self.part_sizes[1]//2)
        mo_part_256 = roi_align_self(f2_1.clone(), mo_location//2, self.part_sizes[3]//2)

        le_part_128 = roi_align_self(f4_1.clone(), le_location//4, self.part_sizes[0]//4)
        re_part_128 = roi_align_self(f4_1.clone(), re_location//4, self.part_sizes[1]//4)
        mo_part_128 = roi_align_self(f4_1.clone(), mo_location//4, self.part_sizes[3]//4)

        le_part_64 = roi_align_self(f6_1.clone(), le_location//8, self.part_sizes[0]//8)
        re_part_64 = roi_align_self(f6_1.clone(), re_location//8, self.part_sizes[1]//8)
        mo_part_64 = roi_align_self(f6_1.clone(), mo_location//8, self.part_sizes[3]//8)


        le_256_q = self.LE_256_Q(le_part_256)
        re_256_q = self.RE_256_Q(re_part_256)
        mo_256_q = self.MO_256_Q(mo_part_256)

        le_128_q = self.LE_128_Q(le_part_128)
        re_128_q = self.RE_128_Q(re_part_128)
        mo_128_q = self.MO_128_Q(mo_part_128)

        le_64_q = self.LE_64_Q(le_part_64)
        re_64_q = self.RE_64_Q(re_part_64)
        mo_64_q = self.MO_64_Q(mo_part_64)

        return {'f256': f2_1, 'f128': f4_1, 'f64': f6_1,\
            'le256': le_part_256, 're256': re_part_256, 'mo256': mo_part_256, \
            'le128': le_part_128, 're128': re_part_128, 'mo128': mo_part_128, \
            'le64': le_part_64, 're64': re_part_64, 'mo64': mo_part_64, \
            'le_256_q': le_256_q, 're_256_q': re_256_q, 'mo_256_q': mo_256_q,\
            'le_128_q': le_128_q, 're_128_q': re_128_q, 'mo_128_q': mo_128_q,\
            'le_64_q': le_64_q, 're_64_q': re_64_q, 'mo_64_q': mo_64_q}


class DMDNet(nn.Module):
    def __init__(self, ngf = 64, banks_num = 128):
        super().__init__()
        self.part_sizes = np.array([80,80,50,110]) # size for 512
        self.feature_sizes = np.array([256,128,64]) # size for 512

        self.banks_num = banks_num
        self.key_scale = 4

        self.E_lq = FeatureExtractor(key_scale = self.key_scale)
        self.E_hq = FeatureExtractor(key_scale = self.key_scale)

        self.LE_256_KV = KeyValue(ngf, ngf // self.key_scale, ngf)
        self.RE_256_KV = KeyValue(ngf, ngf // self.key_scale, ngf)
        self.MO_256_KV = KeyValue(ngf, ngf // self.key_scale, ngf)

        self.LE_128_KV = KeyValue(ngf * 2 , ngf * 2 // self.key_scale, ngf * 2)
        self.RE_128_KV = KeyValue(ngf * 2 , ngf * 2 // self.key_scale, ngf * 2)
        self.MO_128_KV = KeyValue(ngf * 2 , ngf * 2 // self.key_scale, ngf * 2)

        self.LE_64_KV = KeyValue(ngf * 4 , ngf * 4 // self.key_scale, ngf * 4)
        self.RE_64_KV = KeyValue(ngf * 4 , ngf * 4 // self.key_scale, ngf * 4)
        self.MO_64_KV = KeyValue(ngf * 4 , ngf * 4 // self.key_scale, ngf * 4)


        self.LE_256_Attention = AttentionBlock(64)
        self.RE_256_Attention = AttentionBlock(64)
        self.MO_256_Attention = AttentionBlock(64)

        self.LE_128_Attention = AttentionBlock(128)
        self.RE_128_Attention = AttentionBlock(128)
        self.MO_128_Attention = AttentionBlock(128)

        self.LE_64_Attention = AttentionBlock(256)
        self.RE_64_Attention = AttentionBlock(256)
        self.MO_64_Attention = AttentionBlock(256)

        self.LE_256_Mask = MaskAttention(64)
        self.RE_256_Mask = MaskAttention(64)
        self.MO_256_Mask = MaskAttention(64)

        self.LE_128_Mask = MaskAttention(128)
        self.RE_128_Mask = MaskAttention(128)
        self.MO_128_Mask = MaskAttention(128)

        self.LE_64_Mask = MaskAttention(256)
        self.RE_64_Mask = MaskAttention(256)
        self.MO_64_Mask = MaskAttention(256)

        self.MSDilate = MSDilateBlock(ngf*4, dilation = [4,3,2,1])

        self.up1 = StyledUpBlock(ngf*4, ngf*2, noise_inject=False) #
        self.up2 = StyledUpBlock(ngf*2, ngf, noise_inject=False) #
        self.up3 = StyledUpBlock(ngf, ngf, noise_inject=False) #
        self.up4 = nn.Sequential( 
            SpectralNorm(nn.Conv2d(ngf, ngf, 3, 1, 1)),
            nn.LeakyReLU(0.2),
            UpResBlock(ngf),
            UpResBlock(ngf),
            SpectralNorm(nn.Conv2d(ngf, 3, kernel_size=3, stride=1, padding=1)),
            nn.Tanh()
        )
 
        # define generic memory, revise register_buffer to register_parameter for backward update
        self.register_buffer('le_256_mem_key', torch.randn(128,16,40,40))
        self.register_buffer('re_256_mem_key', torch.randn(128,16,40,40))
        self.register_buffer('mo_256_mem_key', torch.randn(128,16,55,55))
        self.register_buffer('le_256_mem_value', torch.randn(128,64,40,40))
        self.register_buffer('re_256_mem_value', torch.randn(128,64,40,40))
        self.register_buffer('mo_256_mem_value', torch.randn(128,64,55,55))
        

        self.register_buffer('le_128_mem_key', torch.randn(128,32,20,20))
        self.register_buffer('re_128_mem_key', torch.randn(128,32,20,20))
        self.register_buffer('mo_128_mem_key', torch.randn(128,32,27,27))
        self.register_buffer('le_128_mem_value', torch.randn(128,128,20,20))
        self.register_buffer('re_128_mem_value', torch.randn(128,128,20,20))
        self.register_buffer('mo_128_mem_value', torch.randn(128,128,27,27))

        self.register_buffer('le_64_mem_key', torch.randn(128,64,10,10))
        self.register_buffer('re_64_mem_key', torch.randn(128,64,10,10))
        self.register_buffer('mo_64_mem_key', torch.randn(128,64,13,13))
        self.register_buffer('le_64_mem_value', torch.randn(128,256,10,10))
        self.register_buffer('re_64_mem_value', torch.randn(128,256,10,10))
        self.register_buffer('mo_64_mem_value', torch.randn(128,256,13,13))

    
    def readMem(self, k, v, q):
        sim = F.conv2d(q, k)
        score = F.softmax(sim/sqrt(sim.size(1)), dim=1) #B * S * 1 * 1 6*128
        sb,sn,sw,sh = score.size()
        s_m = score.view(sb, -1).unsqueeze(1)#2*1*M
        vb,vn,vw,vh = v.size()
        v_in = v.view(vb, -1).repeat(sb,1,1)#2*M*(c*w*h)
        mem_out = torch.bmm(s_m, v_in).squeeze(1).view(sb, vn, vw,vh)
        max_inds = torch.argmax(score, dim=1).squeeze()
        return mem_out, max_inds
    

    def memorize(self, img, locs):
        fs = self.E_hq(img, locs)
        LE256_key, LE256_value = self.LE_256_KV(fs['le256'])
        RE256_key, RE256_value = self.RE_256_KV(fs['re256'])
        MO256_key, MO256_value = self.MO_256_KV(fs['mo256'])

        LE128_key, LE128_value = self.LE_128_KV(fs['le128'])
        RE128_key, RE128_value = self.RE_128_KV(fs['re128'])
        MO128_key, MO128_value = self.MO_128_KV(fs['mo128'])

        LE64_key, LE64_value = self.LE_64_KV(fs['le64'])
        RE64_key, RE64_value = self.RE_64_KV(fs['re64'])
        MO64_key, MO64_value = self.MO_64_KV(fs['mo64'])

        Mem256 = {'LE256Key': LE256_key, 'LE256Value': LE256_value, 'RE256Key': RE256_key, 'RE256Value': RE256_value,'MO256Key': MO256_key, 'MO256Value': MO256_value}
        Mem128 = {'LE128Key': LE128_key, 'LE128Value': LE128_value, 'RE128Key': RE128_key, 'RE128Value': RE128_value,'MO128Key': MO128_key, 'MO128Value': MO128_value}
        Mem64 = {'LE64Key': LE64_key, 'LE64Value': LE64_value, 'RE64Key': RE64_key, 'RE64Value': RE64_value,'MO64Key': MO64_key, 'MO64Value': MO64_value}
 
        FS256 = {'LE256F':fs['le256'], 'RE256F':fs['re256'], 'MO256F':fs['mo256']}
        FS128 = {'LE128F':fs['le128'], 'RE128F':fs['re128'], 'MO128F':fs['mo128']}
        FS64 = {'LE64F':fs['le64'], 'RE64F':fs['re64'], 'MO64F':fs['mo64']}
        
        return Mem256, Mem128, Mem64

    def enhancer(self, fs_in, sp_256=None, sp_128=None, sp_64=None):
        le_256_q = fs_in['le_256_q']
        re_256_q = fs_in['re_256_q']
        mo_256_q = fs_in['mo_256_q']

        le_128_q = fs_in['le_128_q']
        re_128_q = fs_in['re_128_q']
        mo_128_q = fs_in['mo_128_q']

        le_64_q = fs_in['le_64_q']
        re_64_q = fs_in['re_64_q']
        mo_64_q = fs_in['mo_64_q']

        
        ####for 256
        le_256_mem_g, le_256_inds = self.readMem(self.le_256_mem_key, self.le_256_mem_value, le_256_q)
        re_256_mem_g, re_256_inds = self.readMem(self.re_256_mem_key, self.re_256_mem_value, re_256_q)
        mo_256_mem_g, mo_256_inds = self.readMem(self.mo_256_mem_key, self.mo_256_mem_value, mo_256_q)

        le_128_mem_g, le_128_inds = self.readMem(self.le_128_mem_key, self.le_128_mem_value, le_128_q)
        re_128_mem_g, re_128_inds = self.readMem(self.re_128_mem_key, self.re_128_mem_value, re_128_q)
        mo_128_mem_g, mo_128_inds = self.readMem(self.mo_128_mem_key, self.mo_128_mem_value, mo_128_q)

        le_64_mem_g, le_64_inds = self.readMem(self.le_64_mem_key, self.le_64_mem_value, le_64_q)
        re_64_mem_g, re_64_inds = self.readMem(self.re_64_mem_key, self.re_64_mem_value, re_64_q)
        mo_64_mem_g, mo_64_inds = self.readMem(self.mo_64_mem_key, self.mo_64_mem_value, mo_64_q)

        if sp_256 is not None and sp_128 is not None and sp_64 is not None:
            le_256_mem_s, _ = self.readMem(sp_256['LE256Key'], sp_256['LE256Value'], le_256_q)
            re_256_mem_s, _ = self.readMem(sp_256['RE256Key'], sp_256['RE256Value'], re_256_q)
            mo_256_mem_s, _ = self.readMem(sp_256['MO256Key'], sp_256['MO256Value'], mo_256_q)
            le_256_mask = self.LE_256_Mask(fs_in['le256'],le_256_mem_s,le_256_mem_g)
            le_256_mem = le_256_mask*le_256_mem_s + (1-le_256_mask)*le_256_mem_g
            re_256_mask = self.RE_256_Mask(fs_in['re256'],re_256_mem_s,re_256_mem_g)
            re_256_mem = re_256_mask*re_256_mem_s + (1-re_256_mask)*re_256_mem_g
            mo_256_mask = self.MO_256_Mask(fs_in['mo256'],mo_256_mem_s,mo_256_mem_g)
            mo_256_mem = mo_256_mask*mo_256_mem_s + (1-mo_256_mask)*mo_256_mem_g

            le_128_mem_s, _ = self.readMem(sp_128['LE128Key'], sp_128['LE128Value'], le_128_q)
            re_128_mem_s, _ = self.readMem(sp_128['RE128Key'], sp_128['RE128Value'], re_128_q)
            mo_128_mem_s, _ = self.readMem(sp_128['MO128Key'], sp_128['MO128Value'], mo_128_q)
            le_128_mask = self.LE_128_Mask(fs_in['le128'],le_128_mem_s,le_128_mem_g)
            le_128_mem = le_128_mask*le_128_mem_s + (1-le_128_mask)*le_128_mem_g
            re_128_mask = self.RE_128_Mask(fs_in['re128'],re_128_mem_s,re_128_mem_g)
            re_128_mem = re_128_mask*re_128_mem_s + (1-re_128_mask)*re_128_mem_g
            mo_128_mask = self.MO_128_Mask(fs_in['mo128'],mo_128_mem_s,mo_128_mem_g)
            mo_128_mem = mo_128_mask*mo_128_mem_s + (1-mo_128_mask)*mo_128_mem_g

            le_64_mem_s, _ = self.readMem(sp_64['LE64Key'], sp_64['LE64Value'], le_64_q)
            re_64_mem_s, _ = self.readMem(sp_64['RE64Key'], sp_64['RE64Value'], re_64_q)
            mo_64_mem_s, _ = self.readMem(sp_64['MO64Key'], sp_64['MO64Value'], mo_64_q)
            le_64_mask = self.LE_64_Mask(fs_in['le64'],le_64_mem_s,le_64_mem_g)
            le_64_mem = le_64_mask*le_64_mem_s + (1-le_64_mask)*le_64_mem_g
            re_64_mask = self.RE_64_Mask(fs_in['re64'],re_64_mem_s,re_64_mem_g)
            re_64_mem = re_64_mask*re_64_mem_s + (1-re_64_mask)*re_64_mem_g
            mo_64_mask = self.MO_64_Mask(fs_in['mo64'],mo_64_mem_s,mo_64_mem_g)
            mo_64_mem = mo_64_mask*mo_64_mem_s + (1-mo_64_mask)*mo_64_mem_g
        else:
            le_256_mem = le_256_mem_g
            re_256_mem = re_256_mem_g
            mo_256_mem = mo_256_mem_g
            le_128_mem = le_128_mem_g
            re_128_mem = re_128_mem_g
            mo_128_mem = mo_128_mem_g
            le_64_mem = le_64_mem_g
            re_64_mem = re_64_mem_g
            mo_64_mem = mo_64_mem_g

        le_256_mem_norm = adaptive_instance_normalization_4D(le_256_mem, fs_in['le256'])
        re_256_mem_norm = adaptive_instance_normalization_4D(re_256_mem, fs_in['re256'])
        mo_256_mem_norm = adaptive_instance_normalization_4D(mo_256_mem, fs_in['mo256'])
        
        ####for 128
        le_128_mem_norm = adaptive_instance_normalization_4D(le_128_mem, fs_in['le128'])
        re_128_mem_norm = adaptive_instance_normalization_4D(re_128_mem, fs_in['re128'])
        mo_128_mem_norm = adaptive_instance_normalization_4D(mo_128_mem, fs_in['mo128'])
        
        ####for 64
        le_64_mem_norm = adaptive_instance_normalization_4D(le_64_mem, fs_in['le64'])
        re_64_mem_norm = adaptive_instance_normalization_4D(re_64_mem, fs_in['re64'])
        mo_64_mem_norm = adaptive_instance_normalization_4D(mo_64_mem, fs_in['mo64'])
    

        EnMem256 = {'LE256Norm': le_256_mem_norm, 'RE256Norm': re_256_mem_norm, 'MO256Norm': mo_256_mem_norm}
        EnMem128 = {'LE128Norm': le_128_mem_norm, 'RE128Norm': re_128_mem_norm, 'MO128Norm': mo_128_mem_norm}
        EnMem64 = {'LE64Norm': le_64_mem_norm, 'RE64Norm': re_64_mem_norm, 'MO64Norm': mo_64_mem_norm}
        Ind256 = {'LE': le_256_inds, 'RE': re_256_inds, 'MO': mo_256_inds}
        Ind128 = {'LE': le_128_inds, 'RE': re_128_inds, 'MO': mo_128_inds}
        Ind64 = {'LE': le_64_inds, 'RE': re_64_inds, 'MO': mo_64_inds}
        return EnMem256, EnMem128, EnMem64, Ind256, Ind128, Ind64

    def reconstruct(self, fs_in, locs, memstar):
        le_256_mem_norm, re_256_mem_norm, mo_256_mem_norm = memstar[0]['LE256Norm'], memstar[0]['RE256Norm'], memstar[0]['MO256Norm']
        le_128_mem_norm, re_128_mem_norm, mo_128_mem_norm = memstar[1]['LE128Norm'], memstar[1]['RE128Norm'], memstar[1]['MO128Norm']
        le_64_mem_norm, re_64_mem_norm, mo_64_mem_norm = memstar[2]['LE64Norm'], memstar[2]['RE64Norm'], memstar[2]['MO64Norm']

        le_256_final = self.LE_256_Attention(le_256_mem_norm - fs_in['le256']) * le_256_mem_norm + fs_in['le256']
        re_256_final = self.RE_256_Attention(re_256_mem_norm - fs_in['re256']) * re_256_mem_norm + fs_in['re256']
        mo_256_final = self.MO_256_Attention(mo_256_mem_norm - fs_in['mo256']) * mo_256_mem_norm + fs_in['mo256']
        
        le_128_final = self.LE_128_Attention(le_128_mem_norm - fs_in['le128']) * le_128_mem_norm + fs_in['le128']
        re_128_final = self.RE_128_Attention(re_128_mem_norm - fs_in['re128']) * re_128_mem_norm + fs_in['re128']
        mo_128_final = self.MO_128_Attention(mo_128_mem_norm - fs_in['mo128']) * mo_128_mem_norm + fs_in['mo128']
        
        le_64_final = self.LE_64_Attention(le_64_mem_norm - fs_in['le64']) * le_64_mem_norm + fs_in['le64']
        re_64_final = self.RE_64_Attention(re_64_mem_norm - fs_in['re64']) * re_64_mem_norm + fs_in['re64']
        mo_64_final = self.MO_64_Attention(mo_64_mem_norm - fs_in['mo64']) * mo_64_mem_norm + fs_in['mo64']


        le_location = locs[:,0,:]
        re_location = locs[:,1,:]
        mo_location = locs[:,3,:]

        # Somehow with latest Torch it doesn't like numpy wrappers anymore
        
        # le_location = le_location.cpu().int().numpy()
        # re_location = re_location.cpu().int().numpy()
        # mo_location = mo_location.cpu().int().numpy()
        le_location = le_location.cpu().int()
        re_location = re_location.cpu().int()
        mo_location = mo_location.cpu().int()

        up_in_256 = fs_in['f256'].clone()# * 0
        up_in_128 = fs_in['f128'].clone()# * 0
        up_in_64 = fs_in['f64'].clone()# * 0

        for i in range(fs_in['f256'].size(0)):
            up_in_256[i:i+1,:,le_location[i,1]//2:le_location[i,3]//2,le_location[i,0]//2:le_location[i,2]//2] = F.interpolate(le_256_final[i:i+1,:,:,:].clone(), (le_location[i,3]//2-le_location[i,1]//2,le_location[i,2]//2-le_location[i,0]//2),mode='bilinear',align_corners=False)
            up_in_256[i:i+1,:,re_location[i,1]//2:re_location[i,3]//2,re_location[i,0]//2:re_location[i,2]//2] = F.interpolate(re_256_final[i:i+1,:,:,:].clone(), (re_location[i,3]//2-re_location[i,1]//2,re_location[i,2]//2-re_location[i,0]//2),mode='bilinear',align_corners=False)
            up_in_256[i:i+1,:,mo_location[i,1]//2:mo_location[i,3]//2,mo_location[i,0]//2:mo_location[i,2]//2] = F.interpolate(mo_256_final[i:i+1,:,:,:].clone(), (mo_location[i,3]//2-mo_location[i,1]//2,mo_location[i,2]//2-mo_location[i,0]//2),mode='bilinear',align_corners=False)
            
            up_in_128[i:i+1,:,le_location[i,1]//4:le_location[i,3]//4,le_location[i,0]//4:le_location[i,2]//4] = F.interpolate(le_128_final[i:i+1,:,:,:].clone(), (le_location[i,3]//4-le_location[i,1]//4,le_location[i,2]//4-le_location[i,0]//4),mode='bilinear',align_corners=False)
            up_in_128[i:i+1,:,re_location[i,1]//4:re_location[i,3]//4,re_location[i,0]//4:re_location[i,2]//4] = F.interpolate(re_128_final[i:i+1,:,:,:].clone(), (re_location[i,3]//4-re_location[i,1]//4,re_location[i,2]//4-re_location[i,0]//4),mode='bilinear',align_corners=False)
            up_in_128[i:i+1,:,mo_location[i,1]//4:mo_location[i,3]//4,mo_location[i,0]//4:mo_location[i,2]//4] = F.interpolate(mo_128_final[i:i+1,:,:,:].clone(), (mo_location[i,3]//4-mo_location[i,1]//4,mo_location[i,2]//4-mo_location[i,0]//4),mode='bilinear',align_corners=False)

            up_in_64[i:i+1,:,le_location[i,1]//8:le_location[i,3]//8,le_location[i,0]//8:le_location[i,2]//8] = F.interpolate(le_64_final[i:i+1,:,:,:].clone(), (le_location[i,3]//8-le_location[i,1]//8,le_location[i,2]//8-le_location[i,0]//8),mode='bilinear',align_corners=False)
            up_in_64[i:i+1,:,re_location[i,1]//8:re_location[i,3]//8,re_location[i,0]//8:re_location[i,2]//8] = F.interpolate(re_64_final[i:i+1,:,:,:].clone(), (re_location[i,3]//8-re_location[i,1]//8,re_location[i,2]//8-re_location[i,0]//8),mode='bilinear',align_corners=False)
            up_in_64[i:i+1,:,mo_location[i,1]//8:mo_location[i,3]//8,mo_location[i,0]//8:mo_location[i,2]//8] = F.interpolate(mo_64_final[i:i+1,:,:,:].clone(), (mo_location[i,3]//8-mo_location[i,1]//8,mo_location[i,2]//8-mo_location[i,0]//8),mode='bilinear',align_corners=False)
        
        ms_in_64 = self.MSDilate(fs_in['f64'].clone())
        fea_up1 = self.up1(ms_in_64, up_in_64)
        fea_up2 = self.up2(fea_up1, up_in_128) #
        fea_up3 = self.up3(fea_up2, up_in_256) #
        output = self.up4(fea_up3) #
        return output

    def generate_specific_dictionary(self, sp_imgs=None, sp_locs=None):
        return self.memorize(sp_imgs, sp_locs)

    def forward(self, lq=None, loc=None, sp_256 = None, sp_128 = None, sp_64 = None):
        try:
            fs_in = self.E_lq(lq, loc) # low quality images
        except Exception as e:
            print(e)

        GeMemNorm256, GeMemNorm128, GeMemNorm64, Ind256, Ind128, Ind64 = self.enhancer(fs_in)
        GeOut = self.reconstruct(fs_in, loc, memstar = [GeMemNorm256, GeMemNorm128, GeMemNorm64])
        if sp_256 is not None and sp_128 is not None and sp_64 is not None:
            GSMemNorm256, GSMemNorm128, GSMemNorm64, _, _, _ = self.enhancer(fs_in, sp_256, sp_128, sp_64)
            GSOut = self.reconstruct(fs_in, loc, memstar = [GSMemNorm256, GSMemNorm128, GSMemNorm64])
        else:
            GSOut = None
        return GeOut, GSOut

class UpResBlock(nn.Module):
    def __init__(self, dim, conv_layer = nn.Conv2d, norm_layer = nn.BatchNorm2d):
        super(UpResBlock, self).__init__()
        self.Model = nn.Sequential(
            SpectralNorm(conv_layer(dim, dim, 3, 1, 1)),
            nn.LeakyReLU(0.2),
            SpectralNorm(conv_layer(dim, dim, 3, 1, 1)),
        )
    def forward(self, x):
        out = x + self.Model(x)
        return out

```

# roop\processors\Enhance_CodeFormer.py

```py
from typing import Any, List, Callable
import cv2 
import numpy as np
import onnxruntime
import roop.globals

from roop.typing import Face, Frame, FaceSet
from roop.utilities import resolve_relative_path

class Enhance_CodeFormer():
    model_codeformer = None

    plugin_options:dict = None

    processorname = 'codeformer'
    type = 'enhance'
    

    def Initialize(self, plugin_options:dict):
        if self.plugin_options is not None:
            if self.plugin_options["devicename"] != plugin_options["devicename"]:
                self.Release()

        self.plugin_options = plugin_options
        if self.model_codeformer is None:
            # replace Mac mps with cpu for the moment
            self.devicename = self.plugin_options["devicename"].replace('mps', 'cpu')
            model_path = resolve_relative_path('../models/CodeFormer/CodeFormerv0.1.onnx')
            self.model_codeformer = onnxruntime.InferenceSession(model_path, None, providers=roop.globals.execution_providers)
            self.model_inputs = self.model_codeformer.get_inputs()
            model_outputs = self.model_codeformer.get_outputs()
            self.io_binding = self.model_codeformer.io_binding()           
            self.io_binding.bind_cpu_input(self.model_inputs[1].name, np.array([0.5]))
            self.io_binding.bind_output(model_outputs[0].name, self.devicename)


    def Run(self, source_faceset: FaceSet, target_face: Face, temp_frame: Frame) -> Frame:
        input_size = temp_frame.shape[1]
        # preprocess
        temp_frame = cv2.resize(temp_frame, (512, 512), cv2.INTER_CUBIC)
        temp_frame = cv2.cvtColor(temp_frame, cv2.COLOR_BGR2RGB)
        temp_frame = temp_frame.astype('float32') / 255.0
        temp_frame = (temp_frame - 0.5) / 0.5
        temp_frame = np.expand_dims(temp_frame, axis=0).transpose(0, 3, 1, 2)
        
        self.io_binding.bind_cpu_input(self.model_inputs[0].name, temp_frame.astype(np.float32))
        self.model_codeformer.run_with_iobinding(self.io_binding)
        ort_outs = self.io_binding.copy_outputs_to_cpu()
        result = ort_outs[0][0]
        del ort_outs
        
        # post-process
        result = result.transpose((1, 2, 0))

        un_min = -1.0
        un_max = 1.0
        result = np.clip(result, un_min, un_max)
        result = (result - un_min) / (un_max - un_min)

        result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
        result = (result * 255.0).round()
        scale_factor = int(result.shape[1] / input_size)       
        return result.astype(np.uint8), scale_factor


    def Release(self):
        del self.model_codeformer
        self.model_codeformer = None
        del self.io_binding
        self.io_binding = None


```

# .github\workflows\stale.yml

```yml
# This workflow warns and then closes issues and PRs that have had no activity for a specified amount of time.
#
# You can adjust the behavior by modifying this file.
# For more information, see:
# https://github.com/actions/stale
name: Mark stale issues and pull requests

on:
  schedule:
  - cron: '32 0 * * *'

jobs:
  stale:

    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write

    steps:
    - uses: actions/stale@v5
      with:
        repo-token: ${{ secrets.GITHUB_TOKEN }}
        stale-issue-message: 'This issue is stale because it has been open 30 days with no activity. Remove stale label or comment or this will be closed in 5 days.'
        stale-pr-message: 'This PR is stale because it has been open 45 days with no activity. Remove stale label or comment or this will be closed in 10 days.'
        close-issue-message: 'This issue was closed because it has been stalled for 5 days with no activity.'
        days-before-stale: 30
        days-before-close: 5
        days-before-pr-close: -1

```

# .github\ISSUE_TEMPLATE\bug_report.md

```md
---
name: Bug report
about: Create a report to help us improve
title: ''
labels: ''
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Details**
What OS are you using?
- [ ] Linux
- [ ] Linux in WSL
- [ ] Windows 
- [ ] Mac

Are you using a GPU?
- [ ] No. CPU FTW
- [ ] NVIDIA
- [ ] AMD
- [ ] Intel
- [ ] Mac

**Which version of roop unleashed are you using?**

**Screenshots**
If applicable, add screenshots to help explain your problem.

```

