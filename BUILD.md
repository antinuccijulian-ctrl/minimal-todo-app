Create a clickable desktop app

Option A — Desktop shortcut (quick, recommended)

1. From the project folder, run the PowerShell script to create a Desktop shortcut:

```powershell
powershell -ExecutionPolicy Bypass -File "create_shortcut.ps1"
```

The script creates "Minimal To-Do.lnk" on your Desktop that launches `run_todo.bat`.

Option B — Standalone executable (single .exe)

1. Install PyInstaller:

```bash
pip install pyinstaller
```

2. Build a single-file GUI executable (no console) with an icon:

```bash
pyinstaller --noconsole --onefile --icon=assets/icon.ico todo.py
```

3. After building, copy `dist/todo.exe` to your Desktop and optionally rename it.

Notes

- `run_todo.bat` is a simple launcher that runs `python todo.py`.
- To run the shortcut script, you may need to run PowerShell as your user; the script writes the .lnk to the current user's Desktop.
