import tkinter as tk
import threading
import time
import paramiko
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import configparser
import os
import sys
import argparse

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)  # EXE
    else:
        return os.path.dirname(os.path.abspath(__file__))  # PY

def get_stats(ip, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password)

        # Temperatur
        stdin, stdout, _ = client.exec_command("vcgencmd measure_temp")
        temp_output = stdout.read().decode().strip()
        temp_c = temp_output.replace("temp=", "").replace("'C", "").replace(".", ",")

        # CPU-Auslastung mit vmstat
        stdin, stdout, _ = client.exec_command("vmstat 1 2 | tail -1 | awk '{print $15}'")
        idle_str = stdout.read().decode().strip()
        cpu_usage = round(100 - float(idle_str.replace(",", ".")), 1)

        # RAM-Verbrauch
        stdin, stdout, _ = client.exec_command("free -m")
        lines = stdout.readlines()
        mem_line = [line for line in lines if "Mem:" in line][0]
        mem_parts = mem_line.split()
        total = int(mem_parts[1])
        available = int(mem_parts[6])
        ram_usage = round(100 - (available / total * 100), 2)

        client.close()
        return temp_c, cpu_usage, ram_usage
    except Exception as e:
        return f"Fehler: {e}", "", ""

def create_tray_icon(app_ref):
    from pystray import Icon, MenuItem as item
    
    def on_quit(icon, item):
        app_ref.exit_app()

    # Icon aus Datei laden
    icon_path = get_resource_path("icon.ico")
    
    try:
        image = Image.open(icon_path)
    except Exception as e:
        print(f"[Tray Icon Fehler] {e}")
        image = Image.new("RGB", (64, 64), (255, 0, 0))  # Fallback

    icon_name = f"pi_monitor_{app_ref.ip.replace('.', '_')}"
    icon_title = f"Pi Monitor – {app_ref.ip}"

    menu = (
        item("Beenden", on_quit),
        item(f"IP: {app_ref.ip}", lambda *_: None, enabled=False),
    )

    tray_icon = Icon(icon_name, image, icon_title, menu)
    threading.Thread(target=tray_icon.run, daemon=True).start()

class TransparentMonitor:
    def __init__(self, config):
        self.ip = config["ip"]
        self.user = config["username"]
        self.pwd = config["password"]
        self.interval = int(config["interval"])
        self.layout = config.get("layout", "horizontal").lower()
        self.geometry = config.get("geometry", "+100+100")
        self.running = True
        self.touch_enabled = config.get("touch", "false").lower() == "true"

        self.root = tk.Tk()
        self.root.title("Pi Monitor Overlay")
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.7)
        self.root.overrideredirect(True)
        self.root.configure(bg='black')
        self.root.geometry(self.geometry)

        if self.layout == "vertikal":
            self.ip_label = tk.Label(self.root, text=self.ip, font=("Consolas", 12), fg="lime", bg="black")
            self.temp_label = tk.Label(self.root, text="🌡T: --°C", font=("Consolas", 12), fg="lime", bg="black")
            self.cpu_label = tk.Label(self.root, text="🧠C: --% CPU", font=("Consolas", 12), fg="lime", bg="black")
            self.ram_label = tk.Label(self.root, text="💾R: --% RAM", font=("Consolas", 12), fg="lime", bg="black")

            self.ip_label.pack(padx=8, pady=(4, 2))
            self.temp_label.pack(padx=8, pady=1)
            self.cpu_label.pack(padx=8, pady=1)
            self.ram_label.pack(padx=8, pady=1)

            for label in (self.ip_label, self.temp_label, self.cpu_label, self.ram_label):
                label.bind("<ButtonPress-1>", self.start_move)
                label.bind("<B1-Motion>", self.do_move)
                # Zusätzlich (für Touchscreens):
                if self.touch_enabled:
                    label.bind("<ButtonPress>", self.start_move)
                    label.bind("<Motion>", self.do_move)
                
        else:
            self.ip_label = tk.Label(self.root, text=self.ip, font=("Consolas", 12), fg="lime", bg="black")
            self.label = tk.Label(self.root, text="Starte...", font=("Consolas", 12), fg="lime", bg="black")

            self.ip_label.pack(padx=10, pady=(4, 1))
            self.label.pack(padx=10, pady=(0, 4))

            for label in (self.ip_label, self.label):
                label.bind("<ButtonPress-1>", self.start_move)
                label.bind("<B1-Motion>", self.do_move)
                # Zusätzlich (für Touchscreens):
                if self.touch_enabled:
                    label.bind("<ButtonPress>", self.start_move)
                    label.bind("<Motion>", self.do_move)

        create_tray_icon(self)
        self.update_loop()
        self.root.mainloop()

    def update_loop(self):
        def loop():
            while self.running:
                temp, cpu, ram = get_stats(self.ip, self.user, self.pwd)
                if self.layout == "vertikal":
                    self.ip_label.config(text=self.ip)
                    self.temp_label.config(text=f"🌡T: {temp}°C")
                    self.cpu_label.config(text=f"🧠C: {cpu}% CPU")
                    self.ram_label.config(text=f"💾R: {ram}% RAM")
                else:
                    self.ip_label.config(text=self.ip)
                    self.label.config(text=f"🌡T: {temp}°C | 🧠C: {cpu}% | 💾R: {ram}%")
                time.sleep(self.interval)
        threading.Thread(target=loop, daemon=True).start()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        # Wenn kein Startpunkt gesetzt wurde (z. B. durch Touch), initialisiere auf 0
        if not hasattr(self, "x") or not hasattr(self, "y"):
            self.x, self.y = event.x, event.y  # versuche mit dem aktuellen Punkt zu starten

        x = self.root.winfo_x() + (event.x - self.x)
        y = self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f"+{x}+{y}")

    def exit_app(self):
        self.running = False
        self.root.destroy()
        sys.exit()

def load_config(config_path=None):
    base_path = get_base_path()
    if not config_path:
        config_path = os.path.join(base_path, "config.ini")

    if not os.path.exists(config_path):
        config = configparser.ConfigParser()
        config["raspberry"] = {
            "ip": "192.168.178.100",
            "username": "pi",
            "password": "raspberry",
            "interval": "5",
            "layout": "horizontal",
            "geometry": "+100+100",
            "touch": "false"
        }
        with open(config_path, "w") as f:
            config.write(f)

    config = configparser.ConfigParser()
    config.read(config_path)

    section = config["raspberry"]
    section.setdefault("layout", "horizontal")
    section.setdefault("geometry", "+100+100")
    return section

def get_resource_path(filename):
    """Pfad zu Ressourcen, kompatibel mit PyInstaller-EXE"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="watch raspi")
    parser.add_argument(
        "--config",
        type=str,
        help="Pfad zur config.ini (optional)",
        default=None
    )
    args = parser.parse_args()
    cfg = load_config(args.config)
    TransparentMonitor(cfg)