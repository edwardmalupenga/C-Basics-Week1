# C-Basics-Week

My first assignment.

## Online Banking GUI

This project is a Tkinter-based desktop application that simulates a simple online banking system. It supports account registration, login, deposits, withdrawals, transfers, and password changes.

### Requirements
- Python 3.9 or later (Tkinter is bundled with standard Python installers on Windows, macOS, and most Linux distributions)
- A desktop environment capable of running Tkinter GUIs

### Quick Start
1. Install Python if it is not already available on the target computer.
2. (Optional but recommended) Create and activate a virtual environment.
3. Install any dependencies with `pip install -r requirements.txt`. The project currently relies only on the Python standard library; this step will simply confirm the environment is ready.
4. Start the application with `python onlinebaking_gui.py`.

### Data Storage
- Account information is stored in a plain-text file located at:
  - Windows: `C:\Users\<USERNAME>\.online_banking\bank_data.txt`
  - macOS/Linux: `/Users/<username>/.online_banking/bank_data.txt`
- The directory is created automatically on first run.
- Set the `ONLINE_BANKING_DATA_DIR` environment variable if you prefer a custom location for the data file.

### Creating an Installable Build
- Install PyInstaller: `pip install pyinstaller`
- Build the distributable package:
  ```bash
  pyinstaller onlinebaking.spec
  ```
- The resulting files will be created in the `dist/online_banking` folder:
  - `online_banking.exe` (Windows one-file executable)
  - On macOS/Linux, the executable will be named `online_banking` (with no extension).
- Zip the `dist/online_banking` directory or wrap it in an installer of your choice (e.g., `msiexec`, `Inno Setup`, `pkgbuild`) before distributing it to other machines.
- First launch on a new machine will create the data directory automatically, so install packages do not need to ship `bank_data.txt`.

### Troubleshooting
- If the GUI fails to launch, confirm that Tkinter is installed with your Python distribution.
- To reset the application, delete the `bank_data.txt` file in the data directory. A fresh file will be created automatically when the app starts.
