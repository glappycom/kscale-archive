<!-- preserved from http://firmware.kscale.dev/getting_started.html via https://web.archive.org/web/20250305004734id_/http://firmware.kscale.dev/getting_started.html -->

# Getting Started[¶](#getting-started "Link to this heading")

Instructions to quickly set up and run the firmware.

## Installation[¶](#installation "Link to this heading")

### Standard Installation[¶](#standard-installation "Link to this heading")

To install the package, run:

```
pip install -e .
```

### Installation for Jetson[¶](#installation-for-jetson "Link to this heading")

1. Install Conda:

   ```
   wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh
   chmod +x Miniforge3-Linux-aarch64.sh
   ./Miniforge3-Linux-aarch64.sh
   source ~/.bashrc
   ```
2. Create Conda environment and install package:

   ```
   conda create --name firmware python=3.11
   conda activate firmware
   make install-dev
   ```

## Working with CAN[¶](#working-with-can "Link to this heading")

1. Set up the CAN bus (this might already be happening in a systemctl service):

   ```
   sudo ip link set can0 up type can bitrate 1000000
   sudo ip link set can1 up type can bitrate 1000000
   sudo ip link set can... up type can bitrate 1000000
   sudo ifconfig can0 txqueuelen 65536
   sudo ifconfig can1 txqueuelen 65536
   sudo ifconfig can... txqueuelen 65536
   ```

## Development[¶](#development "Link to this heading")

To test C++ code and bindings quickly, run:

```
make build-ext
```
