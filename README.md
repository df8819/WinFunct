# WinFunct

A Windows support tool. Scripts, shortcuts and system management in one place.

![Image](WinFunct.ico)

---

## What it does

- **Scripts tab** — Wi-Fi password extraction, DNS flush/renew, disk speedtest, system health restore, checksum verifier, user logoff, and more.
- **Options tab** — Quick buttons for stuff that's buried in Windows: Device Manager, Group Policy, Firewall, Registry, Environment Variables, etc.
- **Interactive shells** — Launch CTT WinUtils, MAS activation, or PowerShell/cmd as admin from one dropdown.
- **Theming** — Switch between dark/light themes on the fly. Add your own in `UI_themes.json`. Useless but I like it.

---

## Install

### Option A (User friendly): Download the exe

Grab the latest [Release](https://github.com/df8819/WinFunct/releases). Right-click → Run as administrator. Done.

### Option B (Dev friendly): Clone and run

```bash
git clone https://github.com/df8819/WinFunct.git
cd WinFunct
```

Then either:
- Double-click `Install.bat` (installs deps + optional desktop shortcut)
- Double-click `Run.bat` (auto-updates from git, launches the app)

Or manually:
```bash
pip install -r requirements.txt
python main.py
```

### Requirements (clone only)
- Python 3.10+
- Git (optional, for auto-updates)
- Windows 10/11

---

## Building an exe

Double-click `Pyinstall_script.bat` or run manually:

```bash
pip install pyinstaller
pyinstaller --onefile --icon=WinFunct.ico --add-data "UI_themes.json;." --add-data "gui;gui" --add-data "core;core" --add-data "config.py;." --name WinFunct main.py
```

---

## Project structure

```
WinFunct/
├── main.py              # Entry point
├── config.py            # Constants, links, option lists
├── requirements.txt
├── UI_themes.json       # Theme presets
├── gui/
│   ├── app.py           # Main window
│   ├── styles.py        # Theme engine
│   ├── widgets.py       # Reusable widget helpers
│   ├── theme_selector.py
│   └── dialogs.py       # All popup windows
├── core/
│   ├── admin.py         # UAC elevation
│   ├── system.py        # System info, DISM, icon cache
│   ├── network.py       # IP, Wi-Fi, ping, netstat
│   ├── disk.py          # Disk info, speedtest
│   └── utils.py         # Shared helpers
├── Run.bat
├── Install.bat
└── Pyinstall_script.bat
```

---

## Screenshots

![Scripts tab](GUI_Pics/placeholder_scripts.png)
![Options tab](GUI_Pics/placeholder_options.png)
![Theme selector](GUI_Pics/placeholder_theme.png)

---

## Notes

- Some functions need admin rights — the app self-elevates on launch.
- Add Windows Defender exclusion for the folder if you get false positives.
- Custom themes: edit `UI_themes.json`, pick colors in the Theme Selector.

---

## License

Do whatever you want with it. Feedback welcome ✌️
