# Mogue Motion Capture
General mocap solutions in python. Designed to work out-of-the-box with MikoVerse but configurable for other virtual avatar applications.

Currently:
* Uses *MediaPipe* video tracking.
* Send *Live Link Face* data

Executable release available here: 
[Releases](https://github.com/mogue/MediaPipe-LiveLink-Python/releases)

## Installation

Make sure you have Python 3 installed and available in the command line.

Open a command prompt navigate to the `MediaPipe-LiveLink-Python` directory and type:

```
pip install -r requirements.txt
```

pip will install dependancies (opencv-python, mediapipe, scipy, numpy, ttkbootstrap, pygrabber)

Or install the dependicies by yourself.

Can be done in one line:

```
pip install mediapipe opencv-python numpy scipy ttkbootstrap pygrabber
```

## Run

After installing dependencies type:

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


### Thanks for testing, suggesetions, help and support

Artelis, BelosJams, CandyZeus, CodeMiko, C1nder, Digy, DreadExcalibur, Emily, EmmeVT, Evekta, Galahad333, Grogdan, justmadeninjas, kyodamaru, Melokacool, M!LD, NyaTokki, OrbitaLinx, PenguinObscurus, peter_hank, proinpretius, Roach, Ryhverse, Sir Aythusa, SleepingJackel, TM, Trip and you!
