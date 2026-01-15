# OTA APP

This is an Over-The-Air (OTA) update application built with Python.

## Prerequisites

- Python 3.x
- Virtual environment (envota) is already set up

# OTA APP

A lightweight Python application for delivering and testing Over-The-Air (OTA) updates, with ESP32 firmware support.

## Overview

This repository contains the Python application source, a virtual environment folder, helper scripts to run the app, and ESP32 firmware for OTA updates.

## Prerequisites

- Python 3.8+ (or a compatible Python 3.x)
- Virtual environment (recommended)

## Install Dependencies

From the project root, install dependencies with:

```powershell
pip install -r requirements.txt
```

If you use a virtual environment, activate it first (Windows example):

```powershell
envota\Scripts\activate
```

## Running

1) Run with a visible terminal (for debugging):

```powershell
envota\Scripts\activate
python main.py
```

2) Run without a console window (recommended for end users):

- Use the provided `run.bat` which activates the virtual environment and launches the app using `pythonw`.
- To hide the batch window entirely, double-click `run.vbs`, which runs `run.bat` invisibly.

Notes:
- `pythonw` runs Python scripts without opening a console; use it only for GUI or background scripts.
- The `run.vbs` file hides the batch process window so no console appears at all.

## Files

- `main.py` — main application script
- `requirements.txt` — Python package dependencies
- `run.bat` — batch script to activate the virtual environment and run the app with `pythonw`
- `run.vbs` — VBScript wrapper to run `run.bat` invisibly
- `envota/` — virtual environment folder (optional; typically not committed)
- `esp32/src/main.cpp` — ESP32 firmware source code
- `esp32/platformio.ini` — PlatformIO configuration for ESP32

## Troubleshooting

- If double-clicking `run.vbs` does not start the app, try running `run.bat` from a command prompt to see error messages.
- Ensure `envota` contains `pythonw.exe` in `envota\Scripts`. If not, install a Python distribution that includes `pythonw`.
- Confirm dependencies are installed by running `pip install -r requirements.txt` inside the activated venv.

## Contributing

Make changes in a feature branch and submit a pull request. Keep the repository free of personal or sensitive information.

## ESP32 Firmware

This folder contains the ESP32 firmware for handling OTA updates.

### Prerequisites

- Arduino IDE with ESP32 board support installed (via Board Manager: `esp32` by Espressif), or
- PlatformIO (VS Code extension or CLI) for better project management.
- ESP32 development board (e.g., ESP32-WROOM-32).

### Libraries

The code uses built-in ESP32 libraries:
- `WiFi.h`
- `WebServer.h`
- `Update.h`

No additional libraries need to be installed.

### Setup and Upload

#### Option 1: Arduino IDE
1. Open `esp32/src/main.cpp` in Arduino IDE.
2. Replace `YOUR_WIFI` and `YOUR_PASSWORD` with your WiFi credentials.
3. Select your ESP32 board and port in Tools menu.
4. Upload the sketch to the ESP32.

#### Option 2: PlatformIO (Recommended)
1. Install PlatformIO (via VS Code extension or CLI).
2. Open the `esp32/` folder in VS Code with PlatformIO.
3. Replace `YOUR_WIFI` and `YOUR_PASSWORD` in `esp32/src/main.cpp`.
4. Build and upload: Use PlatformIO's build/upload buttons or run `pio run -t upload` in the `esp32/` directory.

### Usage

- The ESP32 will connect to WiFi and start a web server on port 80.
- Send a POST request to `/update` with the firmware binary to perform OTA update.
- Use the Python app to send updates to the ESP32's IP address.

## License

