# MediaPipe-LiveLink-Python
Use MediaPipe video capture and send motion capture to LiveLink for VTubeing.

Designed to use webcams with Unreal Engine's Live Link Face plugin.


## Installation

Make sure you have Python 3 installed and available in the command line.

Open a command prompt navigate to the `MediaPipe-LiveLink-Python` directory and type:

```
python setup.py install
```

The setup.py will install dependancies (opencv-python, mediapipe, scipy, numpy)


## Run

After installing dependencies.

```
python run.py
```


## Usage

Press `ESC` key with the preview window selected to exit.

The first time the application is run it will create `WebCam_LiveLink.ini` with some settings that can be modified.


## Build Executable

Executable is built using pyinstaller (`pip install pyinstaller`).

```
pyinstaller --clean build.spec
```

The build will be in a `dist` folder as a single file executable.