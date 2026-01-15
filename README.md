# OTA APP

This is an Over-The-Air (OTA) update application built with Python.

## Prerequisites

- Python 3.x
- Virtual environment (envota) is already set up

# OTA APP

A lightweight Python application for delivering and testing Over-The-Air (OTA) updates.

## Overview

This repository contains the application source, a virtual environment folder, and helper scripts to run the app either interactively or silently on Windows.

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

## Troubleshooting

- If double-clicking `run.vbs` does not start the app, try running `run.bat` from a command prompt to see error messages.
- Ensure `envota` contains `pythonw.exe` in `envota\Scripts`. If not, install a Python distribution that includes `pythonw`.
- Confirm dependencies are installed by running `pip install -r requirements.txt` inside the activated venv.

## Contributing

Make changes in a feature branch and submit a pull request. Keep the repository free of personal or sensitive information.

## License

This project is licensed under the MIT License. See the `LICENSE` file for the full license text and copyright notice.

