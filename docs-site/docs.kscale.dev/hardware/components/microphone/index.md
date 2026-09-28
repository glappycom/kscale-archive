<!-- preserved from https://docs.kscale.dev/hardware/components/microphone via https://web.archive.org/web/20241015003545id_/https://docs.kscale.dev/hardware/components/microphone -->

# Microphone - K-Scale Labs Docs

Hardware

Components

Microphone

# Microphone

⚠️

This documentation is under construction and incomplete. We are in the process
of choosing a microphone that works well with our robots.

At the moment, we are using the this microphone from ReSpeaker ([1 (opens in a new tab)](https://www.seeedstudio.com/ReSpeaker-Mic-Array-v2-0.html))
It can be wired up to the Jetson Orin as such:

![Speaker and Mic Wiring](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fspeaker_and_mic_wiring.9a8ff9e1.png&w=1080&q=75)

Here is an example of code to play a wav file on the speaker:

```
import numpy as np
import sounddevice as sd
import soundfile as sf
 
dur_in_sec = 10.0
fs = 44100
 
print("Listening...")
audio_data = sd.rec(int(dur_in_sec * fs), samplerate=fs, channels=1, blocking=True)
sf.write("../play_audio/recorded_audio.wav", audio_data, 44100)
```

The default device that `sounddevice` use is most often the right one. Even if
two speakers are used, they will be both plugged into one amp. If additional speakers
or mics are plugged in or if default selection is incorrect, you can list the
available devices using `sd.query_devices()` and select one using `sd.default.device = ...`

### From Bits to Sound

This is the path sound takes on the linux system. It is similar to the speaker (in reverse).

1. **Microphone**: Captures sound and converts it to an electrical signal.
2. Sound Card acts as the Digital to Analog Converter (**DAC**)
3. **Driver**: The Advanced LInux Sound Architecture (ALSA) drives the digital
   to analog conversion and writes the bytes to the output.
4. **Sound Server**: Most basically, orchestrates device driver to work with

Our implementation uses `soundfile` and `sounddevice`, which are libraries built to
manipulate audio files. Their functionalities for interacting with the sound card and
getting processed data is through PortAudio, an abstraction layer atop of ALSA.
These can be set up on a fresh Jetson using `sudo apt-get install libportaudio2`
and `pip install soundfile sounddevice`. ALSA is built into the kernel on the Jetson
and does not need to be installed.

PortAudio lives here [github (opens in a new tab)](https://github.com/PortAudio/portaudiob).
ALSA lives here [github (opens in a new tab)](https://github.com/alsa-project/alsa-lib).

### With Digital MEMS Microphones

The ReSpeaker Microphone is a MEMS microphone. The mic sensor onboard is the MP34DT01
which outputs PDM (Pulse-Density Modulation) data. This is already digital data as opposed
to analog.

### Set up

Flash the jetson with Nvidia default image
[https://docs.nvidia.com/sdk-manager/download-run-sdkm/index.html (opens in a new tab)](https://docs.nvidia.com/sdk-manager/download-run-sdkm/index.html)

1. Download Jetson SDK manager, must be Ubuntu 20.0 system
2. For Orin, flash by shorting GND and FC REC, while plugged in power jack and connect to type C. For AGX just connect to USB C (must be the one next to the pins)
3. Jetpack 6.0. Follow the steps. On step 2, check everything

(download miniconda)

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh
chmod +x [Miniconda3-latest-Linux-aarch64.sh](http://miniconda3-latest-linux-aarch64.sh/)
./Miniconda3-latest-Linux-aarch64.sh
source ~/.bashrc
```

(download your code using soundfile, sounddevice)

```
git clone https://github.com/kscalelabs/functions.git
git branch -r
git checkout -b audio
```

download dependencies

```
conda create —name func_conda python=3.8.19
conda activate func_conda
pip install numpy sounddevice soundfile
sudo apt-get install libportaudio2
```

then run!
Note that the automatic sd.default.device is the right one. Comment out that line when running, unless running into issues.

[IMU](/hardware/components/imu "IMU")[LCD](/hardware/components/lcd "LCD")
