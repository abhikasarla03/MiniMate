## Screenshots

### Dashboard

![Dashboard](screenshots/dashboard.png)# MintMate

> A modern, polished productivity assistant for **Linux Mint** (and most Linux
> desktops) built with **Python** and **CustomTkinter**.

MintMate combines a beautiful dark dashboard, live system monitoring,
one-click application launchers, desktop utilities, and a built-in command
console into a single, fast, native-feeling desktop app.

---

## ✨ Features

- **Modern UI** — dark theme, rounded cards, sidebar navigation, header bar,
  status bar, hover effects, and tasteful typography.
- **Live Dashboard** — CPU, RAM, Disk, Battery, Time, and Date cards updated
  in real time with progress bars.
- **Application Launcher** — Chrome, Firefox, Terminal, File Manager,
  Calculator, VS Code, and System Settings, with automatic fallbacks across
  desktop environments (Cinnamon, GNOME, MATE, XFCE, KDE).
- **System Monitor page** — live progress bars and a system information panel
  (OS, kernel, CPU cores, uptime).
- **Desktop Utilities** — lock screen, restart, shutdown, screenshot, open
  Downloads/Documents/Home, empty trash, Google search.
- **Output Console** — terminal-style log panel with timestamps for every
  action.
- **Command Bar** — type commands like `open chrome`, `cpu`, `ram`, `disk`,
  `battery`, `google python tutorials`, `screenshot`, `clear`, `help`.
- **Settings** — appearance mode (dark / light / system) and UI scaling.
- **Modular architecture** — clean separation between UI (`gui.py`) and OS
  integrations (`modules/`).

## 🖼 Screenshots

> Add screenshots here after first run:
>
> - `docs/screenshot-dashboard.png`
> - `docs/screenshot-monitor.png`
> - `docs/screenshot-utilities.png`

## 🛠 Tech Stack

- **Python 3.10+**
- **CustomTkinter** — modern themed Tk widgets
- **psutil** — cross-platform system metrics
- **Pillow** — image support for CustomTkinter

## 📦 Installation

```bash
git clone https://github.com/your-username/mintmate.git
cd mintmate

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### Optional system packages (Linux Mint / Ubuntu)

For the best experience install these once:

```bash
sudo apt install gnome-screenshot xdg-utils trash-cli
```

## ▶️ Usage

```bash
python main.py
```

Then:

- Click items in the sidebar to switch between **Dashboard**, **Applications**,
  **System Monitor**, **Utilities**, **Settings**, and **About**.
- Type commands in the bottom command bar — try `help` to see all options.
- Every action is timestamped in the **Output Console**.

### Command reference

| Command                         | Action                              |
| ------------------------------- | ----------------------------------- |
| `open chrome`                   | Launch Google Chrome / Chromium     |
| `open firefox`                  | Launch Firefox                      |
| `open terminal`                 | Launch the system terminal          |
| `open files`                    | Launch the file manager             |
| `open calculator`               | Launch the calculator               |
| `open vscode`                   | Launch VS Code                      |
| `open settings`                 | Launch system settings              |
| `open downloads` / `documents` / `home` | Open common folders         |
| `lock` / `shutdown` / `restart` | Power options                       |
| `screenshot`                    | Save a screenshot to `~/Pictures`   |
| `trash`                         | Empty the trash                     |
| `cpu` / `ram` / `disk` / `battery` | Show current metric              |
| `sysinfo`                       | Show system summary                 |
| `google <query>`                | Search Google in the default browser|
| `clear`                         | Clear the console                   |
| `help`                          | Show this list inside the app       |

## 📁 Project Structure

```
mintmate/
├── main.py              # Entry point
├── gui.py               # CustomTkinter UI (pages, widgets, app shell)
├── config.py            # Theme, colors, fonts, navigation
├── modules/
│   ├── __init__.py
│   ├── apps.py          # Application launchers
│   ├── monitor.py       # CPU / RAM / Disk / Battery via psutil
│   ├── system.py        # Command interpreter
│   └── utilities.py     # Power, screenshots, folders, web search
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## 🚀 Future Improvements

The codebase is intentionally modular so that the following can be added
without major rewrites:

- 🎙 **Voice commands** (`speech_recognition`)
- 🗣 **Text-to-speech** notifications (`pyttsx3`)
- 🤖 **AI chatbot** integration via local LLMs (Ollama, llama.cpp)
- 🔌 **Plugin system** — drop new modules into `modules/` and register them
- 🎨 **Theme switching** with custom palettes in `config.py`
- 🔔 **Desktop notifications** (`notify2` / `plyer`)
- ⌨ **Global keyboard shortcuts** (`pynput` / `keyboard`)
- 📊 Historical metric charts on the Monitor page

## 📜 License

Released under the [MIT License](LICENSE).
