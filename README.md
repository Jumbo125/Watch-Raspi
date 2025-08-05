
# 🖥️ Raspberry Watch Raspi/Linux Systems am Windows PC

Ein kleines Python-Tool zur transparenten Systemüberwachung eines entfernten Raspberry Pi direkt auf dem eigenen Desktop – mit CPU-, RAM- und Temperaturanzeige im Overlay + Systemtray-Integration.

## 🧠 Features

- 🔍 **Live-Monitoring**: Temperatur, CPU-Auslastung und RAM-Verbrauch
- 📡 **Verbindung per SSH**: Sichere Abfrage der Systemdaten
- 📦 **Kompakt & Transparent**: Overlay auf dem Desktop (horizontal oder vertikal)
- 🖱️ **Verschiebbar & Touch-freundlich**
- 🧲 **Taskbar-Symbol (System Tray)** mit IP-Anzeige und Beenden-Funktion
- ⚙️ **Konfigurierbar via `config.ini`**

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

1. **Projekt starten**

```bash
python pi_overlay.py
```

2. **Config anpassen**

Beim ersten Start wird eine Datei `config.ini` erstellt:

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
pyinstaller --noconfirm --onefile --windowed pi_overlay.py
```

---

## 🧑‍💻 Lizenz

MIT License – freie Nutzung & Weitergabe erwünscht 😊

---

## 💡 Autor

**[Dein Name oder GitHub-Link]**
