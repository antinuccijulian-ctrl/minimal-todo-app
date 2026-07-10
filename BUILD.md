Create a clickable desktop app

Option A — Desktop shortcut (quick, recommended)

1. From the project folder, run the PowerShell script to create a Desktop shortcut:

```powershell
powershell -ExecutionPolicy Bypass -File "create_shortcut.ps1"
```

The script creates "Minimal To-Do.lnk" on your Desktop that launches `run_todo.bat`.

Option B — Standalone executable (fast desktop launch)

1. Install PyInstaller:

```bash
pip install pyinstaller
```

2. Build a one-dir GUI executable package with an icon:

```bash
pyinstaller --noconsole todo.spec
```

3. After building, use the generated executable at `dist\todo\todo.exe`.

Notes

- The one-dir build is faster to launch than a one-file bundle because it avoids unpacking the app on every start.
- `run_todo.bat` is a simple launcher that runs `python todo.py`.
- To run the shortcut script, you may need to run PowerShell as your user; the script writes the .lnk to the current user's Desktop.
