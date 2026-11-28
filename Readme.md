# LOLA by IOR-DOL – Education Edition

## About

**LOLA by IOR-DOL** is a software tool for **algorithmic facility location planning**
(Operations Research).
This **Education Edition** contains the Education Mode: it helps students explore and understand
algorithms for finding cost-optimal facility locations (planar, network and discrete problems)
and for districting.

The software is intended **exclusively for practice and learning purposes** and is currently
in a **testing phase**.

## ⚠️ Disclaimer

This software is still under development and testing. **We cannot guarantee that the solutions
provided by the program are always correct.** Please do not rely on the results for graded work
or critical applications.

If you believe you have found an error, or if the program crashes or becomes unresponsive,
please contact us — your feedback helps us improve the software:

📧 **Contact:** julius.hoffmann@kit.edu

> If the program freezes, close it via Task Manager (Windows) or Force Quit (macOS)
> and let us know what you were doing when it happened.

## Installation (once)

LOLA runs from its source code: you install Python and LOLA's packages once, then start LOLA from a terminal.
(Standalone apps are not offered for the time being; you can build one yourself, see "Optional: build an app".)

1. **Install Python 3.12** (LOLA is tested with it): https://www.python.org/downloads/
   - Windows: tick "Add python.exe to PATH" in the installer.
   - Linux: from the package manager, e.g. on Ubuntu 24.04: `sudo apt install python3.12 python3.12-venv`

2. **Download the source code** from GitHub:
   🔗 https://github.com/Julius2627/LOLA-Education
   (green "Code" button → "Download ZIP" and extract it, or `git clone https://github.com/Julius2627/LOLA-Education.git`)

3. **Open a terminal in the LOLA folder**: on Windows type `cmd` into the address bar of the folder and press Enter;
   on macOS right-click the folder → "New Terminal at Folder"; on Linux right-click → "Open in Terminal".

4. **Create LOLA's own Python environment and install the packages into it.** The environment is the folder `.venv`
   inside the LOLA folder, so nothing is installed elsewhere on the computer.
   - macOS and Linux:
     ```bash
     python3.12 -m venv .venv
     .venv/bin/python -m pip install -r requirements.txt
     ```
   - Windows:
     ```bat
     py -3.12 -m venv .venv
     .venv\Scripts\python -m pip install -r requirements.txt
     ```

## Starting LOLA (every time)

Open a terminal in the LOLA folder (as in step 3) and type:
- macOS and Linux:
  ```bash
  .venv/bin/python main.py
  ```
- Windows:
  ```bat
  .venv\Scripts\python main.py
  ```

To quit, close the LOLA window.

## Optional: build an app

With PyInstaller you can build an app that starts without a terminal, for your own computer. Build it on the system
it is for (an app for Windows on Windows, and so on), after the installation above. Passing the app on is another
matter: it contains the packages, so it would have to come with their license texts (e.g. PyQt5: GPL v3).

1. **Install PyInstaller** into LOLA's environment:
   - macOS and Linux: `.venv/bin/python -m pip install pyinstaller`
   - Windows: `.venv\Scripts\python -m pip install pyinstaller`

2. **Build the app**:
   - macOS and Linux:
     ```bash
     .venv/bin/pyinstaller main.py --name LOLA-Education --windowed --noconfirm
     ```
   - Windows:
     ```bat
     .venv\Scripts\pyinstaller main.py --name LOLA-Education --windowed --noconfirm
     ```

3. **The app** is in the folder `dist`: `dist/LOLA-Education.app` (macOS), `dist\LOLA-Education\LOLA-Education.exe`
   (Windows) or `dist/LOLA-Education/LOLA-Education` (Linux; on Windows and Linux the whole folder belongs to it).

## Open Source & License

The complete source code is open source and freely accessible:  
🔗 [https://github.com/Julius2627/LOLA-Education](https://github.com/Julius2627/LOLA-Education)

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

The packages that pip installs (e.g. PyQt5, NumPy, matplotlib) come from PyPI, each under its own license.

## Authors

Developed by Julius Hoffmann
IOR, Karlsruhe Institute of Technology (KIT)

---

Version: 0.9.1 (Beta) – Last updated: November 2026
