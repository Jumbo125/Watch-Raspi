# 🖥️ Raspberry Watch Raspi/Linux Systems am Windows PC

Ein kleines Python-Tool zur transparenten Systemüberwachung eines entfernten Raspberry Pi direkt auf dem eigenen Desktop – mit CPU-, RAM- und Temperaturanzeige im Overlay + Systemtray-Integration.

## 🧠 Features

- 🔍 **Live-Monitoring**: Temperatur, CPU-Auslastung und RAM-Verbrauch
- 📡 **Verbindung per SSH**: Sichere Abfrage der Systemdaten
- 📦 **Kompakt & Transparent**: Overlay auf dem Desktop (horizontal oder vertikal)
- 🖱️ **Verschiebbar & Touch-freundlich**
- 🧲 **Taskbar-Symbol (System Tray)** mit IP-Anzeige und Beenden-Funktion
- ⚙️ **Konfigurierbar via `config.ini` oder Parameter**

---

## 📸 Vorschau

*(Hier kannst du später Screenshots einfügen)*

```bash
🌡T: 54,3°C | 🧠C: 21.3% | 💾R: 34.87%
```

---

## ⚙️ Voraussetzungen

Folgende Python-Pakete werden benötigt:

```bash
pip install paramiko pystray pillow
```

Außerdem benötigst du:

- Ein Raspberry Pi (oder ein anderes Gerät mit `vcgencmd`, `vmstat` und `free`)
- SSH-Zugang aktiviert
- Python 3.7+

---

## 🚀 Verwendung

1. **Projekt starten (Standard-Konfiguration)**

```bash
python pi_overlay.py
```

2. **Oder mit eigener Konfigurationsdatei**

```bash
python pi_overlay.py --config "C:/Pfad/zur/deiner_config.ini"
```

> 💡 Auch als `.exe` funktioniert das:
> `watch_raspi.exe --config "C:/Pfad/zur/deiner_config.ini"`

3. **Beim ersten Start wird automatisch `config.ini` erstellt**, falls keine vorhanden ist:

```ini
[raspberry]
ip = 192.168.178.100
username = pi
password = raspberry
interval = 5
layout = horizontal
geometry = +100+100
touch = false
```

### 🔧 Konfigurationsoptionen:

| Schlüssel     | Beschreibung                            |
|--------------|------------------------------------------|
| `ip`         | IP-Adresse deines Raspberry Pi           |
| `username`   | SSH-Benutzername                         |
| `password`   | SSH-Passwort                             |
| `interval`   | Abfrageintervall in Sekunden             |
| `layout`     | `horizontal` oder `vertikal`             |
| `geometry`   | Startposition des Fensters (z. B. `+100+100`) |
| `touch`      | `true` für Touchscreen-Kompatibilität    |

---

## 📁 Struktur

```text
pi_overlay/
├── pi_overlay.py         # Hauptprogramm
├── config.ini            # Konfigurationsdatei (wird erzeugt)
└── icon.ico              # (Optional) Tray-Icon
```

---

## 🛑 Beenden

- Rechtsklick auf das Tray-Icon → **"Beenden"**
- Oder `ALT + F4` / Taskmanager

---

## 🛠️ Technisches

Das Programm öffnet ein transparentes Overlay (`Tkinter`), verbindet sich per SSH (`paramiko`) zum Raspberry Pi, führt dort Systemkommandos aus und aktualisiert die Anzeige regelmäßig. Durch ein Icon im System-Tray (`pystray`) kann das Tool elegant im Hintergrund laufen.

Abgefragte Linux-Kommandos:

- Temperatur: `vcgencmd measure_temp`
- CPU-Last: `vmstat`
- RAM: `free -m`

---

## 📦 Packaging (optional)

Falls du das Tool als `.exe` verteilen willst, kannst du z. B. [PyInstaller](https://www.pyinstaller.org/) verwenden:

```bash
pyinstaller --noconfirm --onefile --windowed --add-data "icon.ico;." pi_overlay.py
```

---

## 🧑‍💻 Lizenz

MIT License – freie Nutzung & Weitergabe erwünscht 😊

---

## 💡 Autor

**Jumbo125**



# 🖥️ Raspberry Watch – Monitor Raspi/Linux Systems from a Windows PC

A lightweight Python tool that lets you monitor a remote Raspberry Pi (or Linux system) in real time, directly on your Windows desktop – showing CPU usage, RAM usage, and temperature in a transparent overlay, with system tray integration.

## 🧠 Features

- 🔍 **Live Monitoring**: Temperature, CPU load, and RAM usage
- 📡 **SSH Connection**: Secure data retrieval via SSH
- 📦 **Compact & Transparent**: Always-on-top overlay (horizontal or vertical)
- 🖱️ **Movable & Touchscreen-friendly**
- 🧲 **System Tray Icon**: With IP display and quit button
- ⚙️ **Fully configurable via `config.ini` or command-line**

---

## 📸 Preview

*(Add your own screenshots here later)*

```bash
🌡T: 54.3°C | 🧠C: 21.3% | 💾R: 34.87%
```

---

## ⚙️ Requirements

Install dependencies using pip:

```bash
pip install paramiko pystray pillow
```

Also needed:

- A Raspberry Pi (or any Linux system with `vcgencmd`, `vmstat`, and `free`)
- SSH access enabled
- Python 3.7 or newer

---

## 🚀 Usage

1. **Run the program (default config path)**

```bash
python pi_overlay.py
```

2. **Or use a custom config file**

```bash
python pi_overlay.py --config "C:/path/to/your_config.ini"
```

> 💡 This also works with the compiled `.exe`:
> `watch_raspi.exe --config "C:/path/to/your_config.ini"`

3. **First-time use? A `config.ini` will be created automatically**:

```ini
[raspberry]
ip = 192.168.178.100
username = pi
password = raspberry
interval = 5
layout = horizontal
geometry = +100+100
touch = false
```

### 🔧 Config Options

| Key         | Description                                |
|-------------|--------------------------------------------|
| `ip`        | IP address of your Raspberry Pi            |
| `username`  | SSH username                               |
| `password`  | SSH password                               |
| `interval`  | Update interval in seconds                 |
| `layout`    | `horizontal` or `vertical` overlay         |
| `geometry`  | Initial window position (e.g. `+100+100`)  |
| `touch`     | Set to `true` for touchscreen support      |

---

## 📁 Project Structure

```text
pi_overlay/
├── pi_overlay.py         # Main program
├── config.ini            # Configuration file (auto-generated)
└── icon.ico              # (Optional) System tray icon
```

---

## 🛑 Exiting the App

- Right-click the system tray icon → **"Quit"**
- Or use `ALT + F4` / Task Manager

---

## 🛠️ Under the Hood

The app opens a transparent `Tkinter` overlay and uses `paramiko` to connect to the Raspberry Pi via SSH. It fetches system stats and displays them in real time. `pystray` handles the tray icon.

Executed commands on the Pi:

- Temperature: `vcgencmd measure_temp`
- CPU usage: `vmstat`
- RAM usage: `free -m`

---

## 📦 Packaging (Optional)

To compile the program as a single `.exe`:

```bash
pyinstaller --noconfirm --onefile --windowed --add-data "icon.ico;." pi_overlay.py
```

---

## 🧑‍💻 License

MIT License – free to use, modify and distribute 😊

---

## 💡 Author

**Jumbo125**
