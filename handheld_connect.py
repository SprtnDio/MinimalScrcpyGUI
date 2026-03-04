"""
🎮 Minimalistic Scrcpy GUI v1.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import json
import os
import sys
import re
import platform
import time
from pathlib import Path

# PIL Icon-Unterstützung
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# ======================================================
# KONFIGURATION & PFADE
# ======================================================
if getattr(sys, 'frozen', False):
    # BASE_DIR
    BASE_DIR = Path(sys.executable).parent
    # BUNDLE_DIR
    BUNDLE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).parent
    BUNDLE_DIR = BASE_DIR

CONFIG_FILE = BASE_DIR / "config.json"
ADB_PATH = BASE_DIR / "adb.exe"
SCRCPY_PATH = BASE_DIR / "scrcpy.exe"
# Das Icon wird jetzt aus dem Bundle geladen!
ICON_PATH = BUNDLE_DIR / "app_icon.ico"

DEFAULT_CONFIG = {
    "last_ip": "",
    "bitrate": 6,
    "mode": "1",
    "orientation": "0",
    "screen_off": True,
    "stay_awake": True,
    "window_alpha": 0.95,
    "topmost": True,
    "language": "de",
    "fullscreen": False,
    "saved_ips": []  # Liste von {"name": str, "ip": str}
}

# ======================================================
# SPRACHTEXTE (DE / EN)
# ======================================================
STRINGS = {
    "de": {
        "connected": "● Verbunden",
        "disconnected": "● Offline",
        "status_connecting": "Verbinde...\nLese Config...",
        "status_check_ip": "Prüfe letzte IP:\n{}",
        "status_connected": "Erfolgreich verbunden!",
        "status_no_device": "Kein Gerät gefunden!\nBitte USB-Kabel anschließen.",
        "status_ip_found": "IP gefunden: {}\nAktiviere TCP/IP...",
        "status_connect_wifi": "Verbinde über WLAN...",
        "status_start_stream": "Erfolgreich verbunden!\nStarte Stream...",
        "status_error": "Fehler:\n{}",
        "status_copied": "✅ Erfolgreich auf PC kopiert!",
        "status_clipboard_empty": "ℹ️ Zwischenablage ist leer.",
        "status_pasted": "✅ Auf Handy eingefügt!",
        "status_not_connected": "Gerät nicht verbunden!",
        "title_display": "Anzeige",
        "title_controls": "Steuerung & Clipboard",
        "title_audio": "Lautstärke",
        "title_settings": "Einstellungen",
        "title_info": "Info",
        "title_exit": "Anwendung Beenden?",
        "title_connection": "Verbindung",
        "autorun_btn": "Autorun",
        "manual_ip": "Manuelle IP:",
        "connect_btn": "Verbinden",
        "disconnect_btn": "Trennen",
        "clear_ip_btn": "Clear last IP",
        "new_device_hint": "Neues Gerät verbinden: Clear last IP und Autorun drücken",
        "saved_ips": "Gespeicherte IPs:",
        "name_label": "Name:",
        "save_btn": "Speichern",
        "delete_btn": "Löschen",
        "ip_hint": "Falls Autorun fehlschlägt,\nIP manuell eingeben.",
        "disp_original": "📱 Original",
        "disp_tablet": "📊 Tablet",
        "disp_ultra": "📺 Ultra",
        "orient_portrait": "📱 Hoch",
        "orient_landscape": "↔ Quer",
        "orient_rotate": "🔄 Drehen",
        "ctrl_back": "◀ Zurück",
        "ctrl_home": "⏺ Home",
        "ctrl_recent": "⬛ Letzte Apps",
        "ctrl_power": "⏻ Power / Display",
        "clip_copy": "📥 Auf PC kopieren",
        "clip_paste": "📤 Auf Handy einfügen",
        "fullscreen_toggle": "🖥️ Vollbild",
        "windowed_toggle": "🪟 Fenstermodus",
        "audio_volume": "Lautstärke",
        "set_bitrate": "Bitrate (1-150 Mbit/s)",
        "set_transparency": "Transparenz",
        "set_topmost": "📌 Immer im Vordergrund",
        "set_screen_off": "🌙 Bildschirm aus",
        "set_stay_awake": "⚡ Immer entsperrt",
        "set_language": "Sprache",
        "exit_yes": "Ja",
        "exit_no": "Nein",
        "info_text": (
            "Minimalistic Scrcpy GUI v2.2\n\n"
            "by SprtnDio\n\n"
            "WICHTIG VOR DEM START:\n"
            "1. Gehe in die Android Einstellungen\n"
            "2. Info > 7x auf Build-Nummer tippen\n"
            "3. Entwickleroptionen öffnen\n"
            "4. 'USB-Debugging' aktivieren\n\n"
            "VERBINDEN:\n"
            "- Gerät per USB-Kabel an den PC anschließen\n"
            "- Auf ▶ klicken, dann 'Autorun' oder manuelle IP\n"
            "- Berechtigung auf dem Handy erlauben\n"
            "- Das Kabel kann danach entfernt werden!\n"
        ),
    },
    "en": {
        "connected": "● Connected",
        "disconnected": "● Offline",
        "status_connecting": "Connecting...\nReading config...",
        "status_check_ip": "Checking last IP:\n{}",
        "status_connected": "Successfully connected!",
        "status_no_device": "No device found!\nPlease connect USB cable.",
        "status_ip_found": "IP found: {}\nEnabling TCP/IP...",
        "status_connect_wifi": "Connecting via Wi‑Fi...",
        "status_start_stream": "Connected successfully!\nStarting stream...",
        "status_error": "Error:\n{}",
        "status_copied": "✅ Copied to PC!",
        "status_clipboard_empty": "ℹ️ Clipboard is empty.",
        "status_pasted": "✅ Pasted to phone!",
        "status_not_connected": "Device not connected!",
        "title_display": "Display",
        "title_controls": "Controls & Clipboard",
        "title_audio": "Volume",
        "title_settings": "Settings",
        "title_info": "Info",
        "title_exit": "Exit Application?",
        "title_connection": "Connection",
        "autorun_btn": "Autorun",
        "manual_ip": "Manual IP:",
        "connect_btn": "Connect",
        "disconnect_btn": "Disconnect",
        "clear_ip_btn": "Clear last IP",
        "new_device_hint": "To connect a new device: Click Clear last IP then Autorun",
        "saved_ips": "Saved IPs:",
        "name_label": "Name:",
        "save_btn": "Save",
        "delete_btn": "Delete",
        "ip_hint": "If autorun fails,\nenter IP manually.",
        "disp_original": "📱 Original",
        "disp_tablet": "📊 Tablet",
        "disp_ultra": "📺 Ultra",
        "orient_portrait": "📱 Portrait",
        "orient_landscape": "↔ Landscape",
        "orient_rotate": "🔄 Rotate",
        "ctrl_back": "◀ Back",
        "ctrl_home": "⏺ Home",
        "ctrl_recent": "⬛ Recent Apps",
        "ctrl_power": "⏻ Power / Display",
        "clip_copy": "📥 Copy to PC",
        "clip_paste": "📤 Paste to phone",
        "fullscreen_toggle": "🖥️ Fullscreen",
        "windowed_toggle": "🪟 Windowed",
        "audio_volume": "Volume",
        "set_bitrate": "Bitrate (1-150 Mbit/s)",
        "set_transparency": "Transparency",
        "set_topmost": "📌 Always on top",
        "set_screen_off": "🌙 Turn screen off",
        "set_stay_awake": "⚡ Stay awake",
        "set_language": "Language",
        "exit_yes": "Yes",
        "exit_no": "No",
        "info_text": (
            "Minimalistic Scrcpy GUI v1.0\n\n"
            "by SprtnDio\n\n"
            "BEFORE START:\n"
            "1. Go to Android Settings\n"
            "2. About phone > tap Build number 7 times\n"
            "3. Enable Developer options\n"
            "4. Enable 'USB debugging'\n\n"
            "CONNECT:\n"
            "- Connect device via USB cable\n"
            "- Click ▶, then choose 'Autorun' or manual IP\n"
            "- Allow debugging on the phone\n"
            "- You can now disconnect the cable!\n"
        ),
    }
}

# ======================================================
# DEVICE MANAGER
# ======================================================
class DeviceManager:
    def __init__(self):
        self.current_ip = None

    def get_all_phone_ips_via_adb(self):
        try:
            flags = subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            result = subprocess.run([str(ADB_PATH), "devices"], capture_output=True, text=True, creationflags=flags)
            device_serial = None
            for line in result.stdout.split("\n"):
                if "\tdevice" in line and ":" not in line and "emulator" not in line:
                    device_serial = line.split("\t")[0]
                    break
            if not device_serial:
                return []
            ip_result = subprocess.run([str(ADB_PATH), "-s", device_serial, "shell", "ip", "-4", "addr", "show"],
                                       capture_output=True, text=True, timeout=10, creationflags=flags)
            ips = []
            pattern = re.compile(r"inet\s+(\d+\.\d+\.\d+\.\d+)")
            for line in ip_result.stdout.split("\n"):
                match = pattern.search(line)
                if match:
                    ip = match.group(1)
                    if not ip.startswith("127."):
                        ips.append(ip)
            return ips
        except Exception as e:
            print(f"ADB Error: {e}")
            return []

    def connect_wireless(self, ip, port=5555):
        try:
            flags = subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            subprocess.run([str(ADB_PATH), "disconnect"], capture_output=True, creationflags=flags)
            result = subprocess.run([str(ADB_PATH), "connect", f"{ip}:{port}"], capture_output=True, text=True, creationflags=flags)
            if "connected" in result.stdout.lower() or "already" in result.stdout.lower():
                self.current_ip = ip
                return True
            return False
        except:
            return False

    def enable_tcpip_via_usb(self):
        try:
            flags = subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            subprocess.run([str(ADB_PATH), "tcpip", "5555"], capture_output=True, creationflags=flags)
            time.sleep(2)
            return True
        except:
            return False

    def disconnect(self):
        try:
            flags = subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            subprocess.run([str(ADB_PATH), "disconnect"], capture_output=True, creationflags=flags)
            self.current_ip = None
            return True
        except:
            return False

# ======================================================
# CLIPBOARD, DISPLAY, AUDIO, SYSTEMCONTROL, SCRCPY MANAGER
# ======================================================
class ClipboardManager:
    def __init__(self, ip): self.ip = ip
    def copy_to_pc(self):
        try:
            flags = subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            result = subprocess.run([str(ADB_PATH), "-s", f"{self.ip}:5555", "shell", "cmd", "clipboard", "getClipboard"],
                                   capture_output=True, text=True, timeout=5, creationflags=flags)
            if result.returncode == 0 and result.stdout.strip():
                text = result.stdout.strip()
                try: import pyperclip; pyperclip.copy(text)
                except: pass
                return text
        except: pass
        return None
    def paste_to_phone(self):
        try:
            flags = subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            subprocess.run([str(ADB_PATH), "-s", f"{self.ip}:5555", "shell", "input", "keyevent", "279"],
                           capture_output=True, creationflags=flags)
            return True
        except: return False

class DisplayManager:
    def __init__(self, ip): self.ip = ip
    def set_resolution(self, mode):
        flags = subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
        if mode == "1":
            subprocess.run([str(ADB_PATH), "-s", f"{self.ip}:5555", "shell", "wm", "size", "reset"], capture_output=True, creationflags=flags)
            subprocess.run([str(ADB_PATH), "-s", f"{self.ip}:5555", "shell", "wm", "density", "reset"], capture_output=True, creationflags=flags)
        elif mode == "2":
            subprocess.run([str(ADB_PATH), "-s", f"{self.ip}:5555", "shell", "wm", "size", "1200x1920"], capture_output=True, creationflags=flags)
            subprocess.run([str(ADB_PATH), "-s", f"{self.ip}:5555", "shell", "wm", "density", "300"], capture_output=True, creationflags=flags)
        elif mode == "3":
            subprocess.run([str(ADB_PATH), "-s", f"{self.ip}:5555", "shell", "wm", "size", "1450x1920"], capture_output=True, creationflags=flags)
            subprocess.run([str(ADB_PATH), "-s", f"{self.ip}:5555", "shell", "wm", "density", "300"], capture_output=True, creationflags=flags)
    def set_orientation(self, orientation):
        def _rotate():
            flags = subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            subprocess.run([str(ADB_PATH), "-s", f"{self.ip}:5555", "shell", "settings", "put", "system", "accelerometer_rotation", "0"], capture_output=True, creationflags=flags)
            time.sleep(0.2)
            subprocess.run([str(ADB_PATH), "-s", f"{self.ip}:5555", "shell", "settings", "put", "system", "user_rotation", orientation], capture_output=True, creationflags=flags)
        threading.Thread(target=_rotate, daemon=True).start()
    def reset_on_exit(self):
        flags = subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
        subprocess.run([str(ADB_PATH), "-s", f"{self.ip}:5555", "shell", "wm", "size", "reset"], capture_output=True, creationflags=flags)
        subprocess.run([str(ADB_PATH), "-s", f"{self.ip}:5555", "shell", "wm", "density", "reset"], capture_output=True, creationflags=flags)

class AudioManager:
    def __init__(self, ip): self.ip = ip
    def change_volume(self, delta):
        try:
            flags = subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            keycode = "24" if delta > 0 else "25"
            subprocess.run([str(ADB_PATH), "-s", f"{self.ip}:5555", "shell", "input", "keyevent", keycode], capture_output=True, creationflags=flags)
        except: pass

class SystemControlManager:
    def __init__(self, ip): self.ip = ip
    def send_key(self, keycode):
        def _send():
            try:
                flags = subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
                subprocess.run([str(ADB_PATH), "-s", f"{self.ip}:5555", "shell", "input", "keyevent", str(keycode)], capture_output=True, creationflags=flags)
            except: pass
        threading.Thread(target=_send, daemon=True).start()

class ScrcpyManager:
    def __init__(self):
        self.process = None
        self.is_running = False

    def start(self, ip, bitrate="6M", mode="1", screen_off=True, stay_awake=True, fullscreen=False):
        if self.is_running:
            self.stop()
        try:
            cmd = [str(SCRCPY_PATH), f"--tcpip={ip}:5555", "--audio-source=playback", "--audio-buffer=250",
                   "--video-buffer=50", f"--video-bit-rate={bitrate}", "--video-codec=h264", "--window-h=950",
                   "--window-title=Minimalistic Scrcpy GUI", "--power-off-on-close"]
            if screen_off:
                cmd.append("--turn-screen-off")
            if stay_awake:
                cmd.append("--stay-awake")
            if fullscreen:
                cmd.append("--fullscreen")
            flags = subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            self.process = subprocess.Popen(cmd, creationflags=flags)
            self.is_running = True
            return True
        except Exception as e:
            print(f"Scrcpy Error: {e}")
            return False

    def stop(self):
        if not self.process:
            return False
        try:
            if self.process.poll() is None:
                self.process.terminate()
                try:
                    self.process.wait(timeout=3)
                except:
                    self.process.kill()
            self.process = None
            self.is_running = False
            return True
        except:
            return False

# ======================================================
# MAIN APPLICATION
# ======================================================
class HandheldConnect:
    def __init__(self, root):
        self.root = root
        # Fenster verstecken, während es aufgebaut wird (gegen sichtbares Flackern)
        self.root.withdraw()
        self.root.title("Minimalistic Scrcpy GUI")

        # DPI-Skalierungsfaktor ermitteln
        self.root.update_idletasks()
        self.dpi_scale = self.root.winfo_fpixels('1i') / 96.0

        # Breite fixieren
        self.w_scaled = int(60 * self.dpi_scale)
        self.root.resizable(False, False)
        self.root.overrideredirect(True)

        self.colors = {
            "bg": "#0f0f1e",
            "sidebar": "#1a1a2e",
            "sidebar_hover": "#252542",
            "primary": "#6366f1",
            "success": "#10b981",
            "error": "#ef4444",
            "warning": "#f59e0b",
            "text": "#ffffff",
            "flyout": "#16213e",
            "border": "#2a2a4a"
        }

        self.root.config(bg=self.colors["sidebar"])
        self.config = self.load_config()

        self.language = self.config.get("language", "de")
        self.strings = STRINGS[self.language]

        self.topmost_var = tk.BooleanVar(value=self.config.get("topmost", True))
        self.root.attributes("-topmost", self.topmost_var.get())
        self.root.attributes("-alpha", self.config.get("window_alpha", 0.95))

        self.fullscreen_var = tk.BooleanVar(value=self.config.get("fullscreen", False))

        self.device_mgr = DeviceManager()
        self.clipboard_mgr = None
        self.scrcpy_mgr = ScrcpyManager()
        self.display_mgr = None
        self.audio_mgr = None
        self.sys_control_mgr = None

        self.is_connected = False
        self.ip_address = ""
        self.target_ip = None
        self.active_flyout = None
        self.active_flyout_btn = None

        self.mode_var = tk.StringVar(value=self.config.get("mode", "1"))
        self.bit_var = tk.IntVar(value=self.config.get("bitrate", 6))
        self.alpha_var = tk.DoubleVar(value=self.config.get("window_alpha", 0.95))
        self.screen_off_var = tk.BooleanVar(value=self.config.get("screen_off", True))
        self.stay_awake_var = tk.BooleanVar(value=self.config.get("stay_awake", True))

        self.saved_ips = self.config.get("saved_ips", [])

        self.flyout_win = tk.Toplevel(self.root)
        self.flyout_win.withdraw()
        self.flyout_win.overrideredirect(True)
        self.flyout_win.config(bg=self.colors["flyout"])
        self.flyout_win.attributes("-topmost", self.topmost_var.get())
        self.flyout_win.attributes("-alpha", self.config.get("window_alpha", 0.95))

        # 1. Benutzeroberfläche erschaffen (Buttons stapeln sich automatisch)
        self.create_ui()

        # 2. Exakte Höhe des erstellten Inhalts messen
        self.root.update_idletasks()
        h_scaled = self.sidebar.winfo_reqheight()

        # 3. Fenster haargenau auf diese gemessene Höhe anpassen
        self.root.geometry(f"{self.w_scaled}x{h_scaled}+100+100")
        
        # 4. Fenster jetzt erst anzeigen
        self.root.deiconify()

    # ================== HILFSFUNKTIONEN ==================
    def tr(self, key):
        return self.strings.get(key, key)

    def set_language(self, lang):
        if lang == self.language:
            return
        self.language = lang
        self.strings = STRINGS[lang]
        self.config["language"] = lang
        self.save_config()
        if self.active_flyout and self.active_flyout_btn:
            self.toggle_flyout(self.active_flyout, self.active_flyout_btn)

    def load_config(self):
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    for k, v in DEFAULT_CONFIG.items():
                        if k not in cfg:
                            cfg[k] = v
                    return cfg
            except:
                pass
        return DEFAULT_CONFIG.copy()

    def save_config(self):
        try:
            self.config["fullscreen"] = self.fullscreen_var.get()
            self.config["bitrate"] = self.bit_var.get()
            self.config["saved_ips"] = self.saved_ips
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
        except:
            pass

    # ================== IP-VERWALTUNG ==================
    def update_saved_ips_dropdown(self):
        if hasattr(self, 'saved_ips_combo') and self.saved_ips_combo.winfo_exists():
            names = [entry["name"] for entry in self.saved_ips]
            self.saved_ips_combo['values'] = names
            if names:
                self.saved_ips_combo.set('')
            else:
                self.saved_ips_combo.set('')

    def on_saved_ip_selected(self, event):
        selected_name = self.saved_ips_combo.get()
        for entry in self.saved_ips:
            if entry["name"] == selected_name:
                self.manual_ip_var.set(entry["ip"])
                break

    def save_current_ip(self):
        name = self.name_entry.get().strip()
        ip = self.manual_ip_var.get().strip()
        if not name or not ip:
            messagebox.showwarning("Warning", "Bitte Name und IP eingeben." if self.language=='de' else "Please enter name and IP.")
            return
        for i, entry in enumerate(self.saved_ips):
            if entry["name"] == name:
                self.saved_ips[i]["ip"] = ip
                self.save_config()
                self.update_saved_ips_dropdown()
                return
        self.saved_ips.append({"name": name, "ip": ip})
        self.save_config()
        self.update_saved_ips_dropdown()
        self.name_entry.delete(0, tk.END)

    def delete_selected_ip(self):
        selected_name = self.saved_ips_combo.get()
        if not selected_name:
            return
        self.saved_ips = [e for e in self.saved_ips if e["name"] != selected_name]
        self.save_config()
        self.update_saved_ips_dropdown()

    def clear_ip_history(self):
        self.config["last_ip"] = ""
        self.save_config()
        self.manual_ip_var.set("")
        self.hide_flyout()

    # ================== UI AUFBAU ==================
    def create_ui(self):
        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], highlightbackground=self.colors["border"], highlightthickness=1)
        self.sidebar.pack(fill=tk.BOTH, expand=True)

        self.sidebar.bind("<ButtonPress-1>", self.start_move)
        self.sidebar.bind("<B1-Motion>", self.do_move)

        # Logo mit DPI-Skalierung
        if PIL_AVAILABLE and ICON_PATH.exists():
            try:
                img = Image.open(ICON_PATH)
                icon_size = int(32 * self.dpi_scale)
                img = img.resize((icon_size, icon_size), Image.LANCZOS)
                self.icon_image = ImageTk.PhotoImage(img)
                self.logo_label = tk.Label(self.sidebar, image=self.icon_image, bg=self.colors["sidebar"])
            except Exception as e:
                print("Icon konnte nicht geladen werden:", e)
                self.logo_label = tk.Label(self.sidebar, text="🎮", font=("Segoe UI", 16), bg=self.colors["sidebar"])
        else:
            self.logo_label = tk.Label(self.sidebar, text="🎮", font=("Segoe UI", 16), bg=self.colors["sidebar"])
            
        self.logo_label.pack(side=tk.TOP, pady=(15, 10))
        self.logo_label.bind("<ButtonPress-1>", self.start_move)
        self.logo_label.bind("<B1-Motion>", self.do_move)

        self.separator = tk.Frame(self.sidebar, bg=self.colors["border"], height=1)
        self.separator.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        self.separator.bind("<ButtonPress-1>", self.start_move)
        self.separator.bind("<B1-Motion>", self.do_move)

        self.btn_connect = self.create_nav_button("▶", self.toggle_connection, bg_col=self.colors["success"])
        self.btn_display = self.create_nav_button("📐", lambda: self.toggle_flyout("display", self.btn_display))
        self.btn_controls = self.create_nav_button("🎮", lambda: self.toggle_flyout("controls", self.btn_controls))
        self.btn_audio = self.create_nav_button("🔊", lambda: self.toggle_flyout("audio", self.btn_audio))
        self.btn_settings = self.create_nav_button("⚙", lambda: self.toggle_flyout("settings", self.btn_settings))
        self.btn_info = self.create_nav_button("ℹ", lambda: self.toggle_flyout("info", self.btn_info))

        # Dynamischer Leerraum (Spacer) vor dem Exit-Button. 
        
        spacer = tk.Frame(self.sidebar, bg=self.colors["sidebar"], height=int(25 * self.dpi_scale))
        spacer.pack(side=tk.TOP)

        self.btn_exit = tk.Button(self.sidebar, text="✕", command=lambda: self.toggle_flyout("exit", self.btn_exit),
                                  bg=self.colors["sidebar"], fg=self.colors["error"],
                                  font=("Segoe UI", 13), relief=tk.FLAT, cursor="hand2", width=3,
                                  activebackground=self.colors["sidebar_hover"], activeforeground="white")
        # Wird nahtlos nach den anderen Buttons (und dem Spacer) angedockt
        self.btn_exit.pack(side=tk.TOP, anchor="center", pady=(0, 15))

    def create_nav_button(self, text, command, bg_col=None, fg_col=None):
        btn = tk.Button(self.sidebar, text=text, command=command,
                        bg=bg_col if bg_col else self.colors["sidebar"],
                        fg=fg_col if fg_col else self.colors["text"],
                        font=("Segoe UI", 13), relief=tk.FLAT, cursor="hand2", width=3,
                        activebackground=self.colors["sidebar_hover"], activeforeground="white")
        btn.pack(side=tk.TOP, anchor="center", pady=3)
        return btn

    # ================== FENSTER VERSCHIEBEN ==================
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = self.root.winfo_x() + event.x - self.x
        y = self.root.winfo_y() + event.y - self.y
        self.root.geometry(f"+{x}+{y}")
        self.hide_flyout()

    # ================== STATUS FLYOUT ==================
    def show_status_flyout(self, msg_key, is_error=False, anchor_widget=None, format_arg=None):
        if anchor_widget is None:
            anchor_widget = self.btn_connect
        msg = self.tr(msg_key)
        if format_arg is not None:
            msg = msg.format(format_arg)
        self.root.after(0, lambda: self._show_status_flyout_ui(msg, is_error, anchor_widget))

    def _show_status_flyout_ui(self, msg, is_error, anchor_widget):
        if self.active_flyout != "status":
            self.hide_flyout()
            self.active_flyout = "status"
            for widget in self.flyout_win.winfo_children():
                widget.destroy()
            container = tk.Frame(self.flyout_win, bg=self.colors["flyout"], highlightbackground=self.colors["border"], highlightthickness=1)
            container.pack(fill=tk.BOTH, expand=True)
            self.status_lbl = tk.Label(container, text=msg, bg=self.colors["flyout"],
                                       fg=self.colors["error"] if is_error else self.colors["success"],
                                       font=("Segoe UI", 9, "bold"), justify=tk.LEFT, wraplength=180)
            self.status_lbl.pack(pady=15, padx=15)
            self.position_flyout(anchor_widget, "status")
            self.flyout_win.deiconify()
        else:
            if hasattr(self, "status_lbl") and self.status_lbl.winfo_exists():
                self.status_lbl.config(text=msg, fg=self.colors["error"] if is_error else self.colors["success"])
                self.position_flyout(anchor_widget, "status")

    # ================== FLYOUT LOGIK ==================
    def toggle_flyout(self, flyout_type, btn_widget):
        if self.active_flyout == flyout_type:
            self.hide_flyout()
            return
        self.hide_flyout()
        self.active_flyout = flyout_type
        self.active_flyout_btn = btn_widget
        self.highlight_button(flyout_type)

        for widget in self.flyout_win.winfo_children():
            widget.destroy()

        container = tk.Frame(self.flyout_win, bg=self.colors["flyout"], highlightbackground=self.colors["border"], highlightthickness=1)
        container.pack(fill=tk.BOTH, expand=True)

        if flyout_type == "display":
            self.build_display(container)
        elif flyout_type == "controls":
            self.build_controls(container)
        elif flyout_type == "audio":
            self.build_audio(container)
        elif flyout_type == "settings":
            self.build_settings(container)
        elif flyout_type == "info":
            self.build_info(container)
        elif flyout_type == "exit":
            self.build_exit(container)
        elif flyout_type == "connection":
            self.build_connection(container)

        self.position_flyout(btn_widget, flyout_type)
        self.flyout_win.deiconify()

    def position_flyout(self, anchor_widget, flyout_type):
        self.flyout_win.update_idletasks()
        f_width = self.flyout_win.winfo_reqwidth()
        f_height = self.flyout_win.winfo_reqheight()

        target_x = self.root.winfo_rootx() + self.root.winfo_width() + 2
        screen_width = self.root.winfo_screenwidth()
        if target_x + f_width > screen_width:
            target_x = self.root.winfo_rootx() - f_width - 2

        root_y = self.root.winfo_rooty()
        root_height = self.root.winfo_height()

        if flyout_type == "controls":
            ideal_y = root_y + (root_height - f_height) // 2
        else:
            ideal_y = anchor_widget.winfo_rooty()
            screen_height = self.root.winfo_screenheight()
            if ideal_y + f_height > screen_height:
                ideal_y = (anchor_widget.winfo_rooty() + anchor_widget.winfo_height()) - f_height

        target_y = max(root_y, min(ideal_y, root_y + root_height - f_height))

        self.flyout_win.geometry(f"{f_width}x{f_height}+{target_x}+{target_y}")

    def hide_flyout(self):
        self.flyout_win.withdraw()
        self.active_flyout = None
        self.active_flyout_btn = None
        for btn in [self.btn_display, self.btn_audio, self.btn_controls, self.btn_settings, self.btn_info]:
            btn.config(bg=self.colors["sidebar"], fg=self.colors["text"])
        self.btn_exit.config(bg=self.colors["sidebar"], fg=self.colors["error"])

    def highlight_button(self, flyout_type):
        btn_map = {"display": self.btn_display, "controls": self.btn_controls,
                   "audio": self.btn_audio, "settings": self.btn_settings, "info": self.btn_info}
        if flyout_type == "exit":
            self.btn_exit.config(bg=self.colors["error"], fg="white")
        elif flyout_type in btn_map:
            btn_map[flyout_type].config(bg=self.colors["primary"], fg="white")

    # ================== FLYOUT-INHALTE ==================
    def build_display(self, parent):
        tk.Label(parent, text=self.tr("title_display"), bg=self.colors["flyout"], fg="white", font=("Segoe UI", 9, "bold")).pack(pady=(10, 5), padx=15)
        for txt_key, val in [("disp_original", "1"), ("disp_tablet", "2"), ("disp_ultra", "3")]:
            tk.Radiobutton(parent, text=self.tr(txt_key), variable=self.mode_var, value=val,
                          bg=self.colors["flyout"], fg="white", selectcolor=self.colors["primary"],
                          command=self.on_mode_change, activebackground=self.colors["flyout"], activeforeground="white").pack(anchor="w", padx=15, pady=2)
        tk.Frame(parent, bg=self.colors["flyout"], height=10).pack()
        tk.Button(parent, text=self.tr("orient_portrait"), command=lambda: self.set_orientation("0"), bg=self.colors["primary"], fg="white", width=12, relief=tk.FLAT, cursor="hand2").pack(pady=3, padx=15)
        tk.Button(parent, text=self.tr("orient_landscape"), command=lambda: self.set_orientation("1"), bg=self.colors["primary"], fg="white", width=12, relief=tk.FLAT, cursor="hand2").pack(pady=3, padx=15)
        tk.Button(parent, text=self.tr("orient_rotate"), command=self.rotate_screen, bg=self.colors["warning"], fg="white", width=12, relief=tk.FLAT, cursor="hand2").pack(pady=(3, 15), padx=15)

    def build_controls(self, parent):
        tk.Label(parent, text=self.tr("title_controls"), bg=self.colors["flyout"], fg="white", font=("Segoe UI", 9, "bold")).pack(pady=(10, 5), padx=15)

        tk.Button(parent, text=self.tr("ctrl_back"), command=lambda: self.send_system_control(4), bg=self.colors["primary"], fg="white", width=14, relief=tk.FLAT, cursor="hand2").pack(pady=3, padx=15)
        tk.Button(parent, text=self.tr("ctrl_home"), command=lambda: self.send_system_control(3), bg=self.colors["primary"], fg="white", width=14, relief=tk.FLAT, cursor="hand2").pack(pady=3, padx=15)
        tk.Button(parent, text=self.tr("ctrl_recent"), command=lambda: self.send_system_control(187), bg=self.colors["primary"], fg="white", width=14, relief=tk.FLAT, cursor="hand2").pack(pady=3, padx=15)
        tk.Button(parent, text=self.tr("ctrl_power"), command=lambda: self.send_system_control(26), bg=self.colors["warning"], fg="white", width=14, relief=tk.FLAT, cursor="hand2").pack(pady=3, padx=15)

        tk.Frame(parent, bg=self.colors["flyout"], height=10).pack()

        tk.Button(parent, text=self.tr("clip_copy"), command=self.copy_clipboard, bg=self.colors["primary"], fg="white", width=18, relief=tk.FLAT, cursor="hand2").pack(pady=3, padx=15)
        tk.Button(parent, text=self.tr("clip_paste"), command=self.paste_clipboard, bg=self.colors["primary"], fg="white", width=18, relief=tk.FLAT, cursor="hand2").pack(pady=3, padx=15)

        tk.Frame(parent, bg=self.colors["flyout"], height=10).pack()

        if self.fullscreen_var.get():
            btn_text = self.tr("windowed_toggle")
        else:
            btn_text = self.tr("fullscreen_toggle")
        tk.Button(parent, text=btn_text, command=self.toggle_fullscreen_and_close,
                  bg=self.colors["primary"], fg="white", width=18, relief=tk.FLAT, cursor="hand2").pack(pady=(3, 15), padx=15)

    def build_audio(self, parent):
        tk.Label(parent, text=self.tr("title_audio"), bg=self.colors["flyout"], fg="white", font=("Segoe UI", 9, "bold")).pack(pady=(10, 5), padx=15)
        vol_frame = tk.Frame(parent, bg=self.colors["flyout"])
        vol_frame.pack(pady=10, padx=15)
        tk.Button(vol_frame, text="🔉 -", command=lambda: self.change_volume(-1), bg=self.colors["sidebar"], fg="white", width=6, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Button(vol_frame, text="🔊 +", command=lambda: self.change_volume(1), bg=self.colors["primary"], fg="white", width=6, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Frame(parent, bg=self.colors["flyout"], height=5).pack()

    def build_settings(self, parent):
        tk.Label(parent, text=self.tr("title_settings"), bg=self.colors["flyout"], fg="white", font=("Segoe UI", 9, "bold")).pack(pady=(10, 5), padx=15)

        tk.Label(parent, text=self.tr("set_bitrate"), bg=self.colors["flyout"], fg="#aaa", font=("Segoe UI", 8)).pack(anchor="w", padx=15)
        bitrate_frame = tk.Frame(parent, bg=self.colors["flyout"])
        bitrate_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        tk.Scale(bitrate_frame, from_=1, to=150, orient=tk.HORIZONTAL, variable=self.bit_var,
                 bg=self.colors["flyout"], fg="white", troughcolor=self.colors["sidebar"],
                 command=lambda v: self.on_bitrate_change()).pack(fill=tk.X)
        self.bitrate_label = tk.Label(bitrate_frame, text=f"{self.bit_var.get()} Mbit/s", bg=self.colors["flyout"], fg="white", font=("Segoe UI", 8))
        self.bitrate_label.pack()

        tk.Label(parent, text=self.tr("set_transparency"), bg=self.colors["flyout"], fg="#aaa", font=("Segoe UI", 8)).pack(anchor="w", padx=15)
        trans_frame = tk.Frame(parent, bg=self.colors["flyout"])
        trans_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        tk.Scale(trans_frame, from_=0.3, to=1.0, orient=tk.HORIZONTAL, variable=self.alpha_var,
                 bg=self.colors["flyout"], fg="white", troughcolor=self.colors["sidebar"],
                 resolution=0.01, command=self.update_transparency).pack(fill=tk.X)
        self.trans_label = tk.Label(trans_frame, text=f"{self.alpha_var.get():.2f}", bg=self.colors["flyout"], fg="white", font=("Segoe UI", 8))
        self.trans_label.pack()

        tk.Checkbutton(parent, text=self.tr("set_topmost"), variable=self.topmost_var, command=self.update_topmost,
                       bg=self.colors["flyout"], fg="white", selectcolor=self.colors["primary"], activebackground=self.colors["flyout"]).pack(anchor="w", padx=15, pady=2)
        tk.Checkbutton(parent, text=self.tr("set_screen_off"), variable=self.screen_off_var,
                       bg=self.colors["flyout"], fg="white", selectcolor=self.colors["primary"], activebackground=self.colors["flyout"]).pack(anchor="w", padx=15, pady=2)
        tk.Checkbutton(parent, text=self.tr("set_stay_awake"), variable=self.stay_awake_var,
                       bg=self.colors["flyout"], fg="white", selectcolor=self.colors["primary"], activebackground=self.colors["flyout"]).pack(anchor="w", padx=15, pady=2)

        lang_frame = tk.Frame(parent, bg=self.colors["flyout"])
        lang_frame.pack(anchor="w", padx=15, pady=(10, 15))
        tk.Label(lang_frame, text=self.tr("set_language") + ":", bg=self.colors["flyout"], fg="#aaa", font=("Segoe UI", 8)).pack(side=tk.LEFT, padx=(0, 10))
        btn_de = tk.Button(lang_frame, text="🇩🇪", command=lambda: self.set_language("de"),
                           bg=self.colors["primary"] if self.language=="de" else self.colors["sidebar"],
                           fg="white", width=3, relief=tk.FLAT, cursor="hand2")
        btn_de.pack(side=tk.LEFT, padx=2)
        btn_en = tk.Button(lang_frame, text="🇬🇧", command=lambda: self.set_language("en"),
                           bg=self.colors["primary"] if self.language=="en" else self.colors["sidebar"],
                           fg="white", width=3, relief=tk.FLAT, cursor="hand2")
        btn_en.pack(side=tk.LEFT, padx=2)

    def build_info(self, parent):
        status_text = self.tr("connected") if self.is_connected else self.tr("disconnected")
        status_color = self.colors["success"] if self.is_connected else self.colors["error"]
        tk.Label(parent, text=status_text, bg=self.colors["flyout"], fg=status_color, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20, pady=(15, 5))
        tk.Label(parent, text=self.tr("info_text"), bg=self.colors["flyout"], fg="#ccc", font=("Segoe UI", 9), justify=tk.LEFT).pack(anchor="w", padx=20, pady=(0, 15))

    def build_exit(self, parent):
        tk.Label(parent, text=self.tr("title_exit"), bg=self.colors["flyout"], fg="white", font=("Segoe UI", 10, "bold")).pack(pady=(15, 10), padx=20)
        btn_frame = tk.Frame(parent, bg=self.colors["flyout"])
        btn_frame.pack(pady=(0, 15), padx=15)
        tk.Button(btn_frame, text=self.tr("exit_yes"), command=self.close_app, bg=self.colors["error"], fg="white", width=8, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text=self.tr("exit_no"), command=self.hide_flyout, bg=self.colors["sidebar_hover"], fg="white", width=8, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)

    def build_connection(self, parent):
        tk.Label(parent, text=self.tr("title_connection"), bg=self.colors["flyout"], fg="white", font=("Segoe UI", 9, "bold")).pack(pady=(10, 5), padx=15)

        # Autorun-Button
        btn_autorun = tk.Button(parent, text=self.tr("autorun_btn"), command=self.connect,
                                bg=self.colors["success"], fg="white", width=15, relief=tk.FLAT, cursor="hand2")
        btn_autorun.pack(pady=5, padx=15)

        # Manuelle IP
        ip_frame = tk.Frame(parent, bg=self.colors["flyout"])
        ip_frame.pack(anchor="w", padx=15, pady=5, fill=tk.X)
        tk.Label(ip_frame, text=self.tr("manual_ip"), bg=self.colors["flyout"], fg="#aaa", font=("Segoe UI", 8)).pack(anchor="w")
        self.manual_ip_var = tk.StringVar(value=self.config.get("last_ip", ""))
        entry_ip = tk.Entry(ip_frame, textvariable=self.manual_ip_var, bg=self.colors["sidebar"], fg="white",
                            insertbackground="white", relief=tk.FLAT, width=20)
        entry_ip.pack(fill=tk.X, pady=2)

        # Hinweistext für neues Gerät
        hint_label = tk.Label(parent, text=self.tr("new_device_hint"), bg=self.colors["flyout"], fg="#aaa",
                              font=("Segoe UI", 8), justify=tk.LEFT)
        hint_label.pack(anchor="w", padx=15, pady=(5, 5))

        # Connect/Disconnect und Clear last IP nebeneinander
        action_frame = tk.Frame(parent, bg=self.colors["flyout"])
        action_frame.pack(pady=5, padx=15, fill=tk.X)

        if not self.is_connected:
            btn_connect = tk.Button(action_frame, text=self.tr("connect_btn"), command=self.manual_connect,
                                    bg=self.colors["primary"], fg="white", width=12, relief=tk.FLAT, cursor="hand2")
            btn_connect.pack(side=tk.LEFT, padx=(0,5))
        else:
            btn_disconnect = tk.Button(action_frame, text=self.tr("disconnect_btn"), command=self.disconnect,
                                       bg=self.colors["error"], fg="white", width=12, relief=tk.FLAT, cursor="hand2")
            btn_disconnect.pack(side=tk.LEFT, padx=(0,5))

        btn_clear = tk.Button(action_frame, text=self.tr("clear_ip_btn"), command=self.clear_ip_history,
                              bg=self.colors["sidebar_hover"], fg="white", width=12, relief=tk.FLAT, cursor="hand2")
        btn_clear.pack(side=tk.LEFT)

        # Gespeicherte IPs
        tk.Label(parent, text=self.tr("saved_ips"), bg=self.colors["flyout"], fg="#aaa", font=("Segoe UI", 8)).pack(anchor="w", padx=15, pady=(10,0))
        combo_frame = tk.Frame(parent, bg=self.colors["flyout"])
        combo_frame.pack(fill=tk.X, padx=15, pady=5)
        self.saved_ips_combo = ttk.Combobox(combo_frame, values=[entry["name"] for entry in self.saved_ips], state="readonly", width=18)
        self.saved_ips_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.saved_ips_combo.bind("<<ComboboxSelected>>", self.on_saved_ip_selected)

        btn_delete = tk.Button(combo_frame, text=self.tr("delete_btn"), command=self.delete_selected_ip,
                               bg=self.colors["error"], fg="white", width=8, relief=tk.FLAT, cursor="hand2")
        btn_delete.pack(side=tk.RIGHT, padx=(5,0))

        # Name und Speichern
        name_frame = tk.Frame(parent, bg=self.colors["flyout"])
        name_frame.pack(fill=tk.X, padx=15, pady=5)
        tk.Label(name_frame, text=self.tr("name_label"), bg=self.colors["flyout"], fg="#aaa", font=("Segoe UI", 8)).pack(anchor="w")
        inner_frame = tk.Frame(name_frame, bg=self.colors["flyout"])
        inner_frame.pack(fill=tk.X)
        self.name_entry = tk.Entry(inner_frame, bg=self.colors["sidebar"], fg="white",
                                    insertbackground="white", relief=tk.FLAT, width=15)
        self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        btn_save = tk.Button(inner_frame, text=self.tr("save_btn"), command=self.save_current_ip,
                             bg=self.colors["primary"], fg="white", width=8, relief=tk.FLAT, cursor="hand2")
        btn_save.pack(side=tk.RIGHT, padx=(5,0))

        # Hinweis
        tk.Label(parent, text=self.tr("ip_hint"), bg=self.colors["flyout"], fg="#aaa",
                 font=("Segoe UI", 8), justify=tk.LEFT).pack(anchor="w", padx=15, pady=(10, 15))

    # ================== VERBINDUNGSFUNKTIONEN ==================
    def toggle_connection(self):
        self.toggle_flyout("connection", self.btn_connect)

    def manual_connect(self):
        ip = self.manual_ip_var.get().strip()
        if ip:
            self.target_ip = ip
            self.connect(ip=ip)
            self.hide_flyout()

    def connect(self, ip=None):
        self.target_ip = ip
        self.btn_connect.config(text="⏳", bg=self.colors["warning"])
        threading.Thread(target=self._connect_thread, daemon=True).start()

    def _connect_thread(self):
        try:
            if self.target_ip:
                self.show_status_flyout("status_connect_wifi", False, format_arg=self.target_ip)
                if not self.device_mgr.enable_tcpip_via_usb():
                    raise Exception("TCP/IP fehlgeschlagen")
                if self.device_mgr.connect_wireless(self.target_ip):
                    self.ip_address = self.target_ip
                    self.show_status_flyout("status_connected", False)
                    time.sleep(1)
                    self._connection_success()
                    return
                else:
                    raise Exception(f"Verbindung zu {self.target_ip} fehlgeschlagen")
            else:
                self.show_status_flyout("status_connecting", False)
                saved_ip = self.config.get("last_ip", "")
                if saved_ip:
                    self.show_status_flyout("status_check_ip", False, format_arg=saved_ip)
                    if self.device_mgr.connect_wireless(saved_ip):
                        self.ip_address = saved_ip
                        self.show_status_flyout("status_connected", False)
                        time.sleep(1)
                        self._connection_success()
                        return
                self.show_status_flyout("status_no_device", False)
                ips = self.device_mgr.get_all_phone_ips_via_adb()
                if not ips:
                    self.show_status_flyout("status_no_device", True)
                    self.root.after(3000, self.hide_flyout)
                    self.root.after(0, lambda: self.btn_connect.config(text="▶", bg=self.colors["success"]))
                    return
                if not self.device_mgr.enable_tcpip_via_usb():
                    raise Exception("TCP/IP fehlgeschlagen")
                for ip in ips:
                    self.show_status_flyout("status_connect_wifi", False, format_arg=ip)
                    if self.device_mgr.connect_wireless(ip):
                        self.ip_address = ip
                        self.show_status_flyout("status_connected", False)
                        time.sleep(1)
                        self._connection_success()
                        return
                raise Exception("Keine der gefundenen IPs konnte verbunden werden.")
        except Exception as e:
            self.show_status_flyout("status_error", True, format_arg=str(e))
            self.root.after(3000, self.hide_flyout)
            self.root.after(0, lambda: self.btn_connect.config(text="▶", bg=self.colors["success"]))

    def _connection_success(self):
        self.is_connected = True
        self.clipboard_mgr = ClipboardManager(self.ip_address)
        self.display_mgr = DisplayManager(self.ip_address)
        self.audio_mgr = AudioManager(self.ip_address)
        self.sys_control_mgr = SystemControlManager(self.ip_address)
        self.config["last_ip"] = self.ip_address
        self.save_config()
        mode = self.mode_var.get()
        self.display_mgr.set_resolution(mode)
        self.display_mgr.set_orientation(self.config.get("orientation", "0"))
        self.root.after(0, lambda: self.btn_connect.config(text="■", bg=self.colors["error"]))
        self.root.after(0, self.hide_flyout)
        self.scrcpy_mgr.start(self.ip_address, f"{self.bit_var.get()}M", mode,
                              self.screen_off_var.get(), self.stay_awake_var.get(),
                              self.fullscreen_var.get())

    def disconnect(self):
        self.btn_connect.config(text="⏳")
        if self.display_mgr:
            self.display_mgr.reset_on_exit()
        self.device_mgr.disconnect()
        self.scrcpy_mgr.stop()
        self.is_connected = False
        self.clipboard_mgr = None
        self.display_mgr = None
        self.audio_mgr = None
        self.sys_control_mgr = None
        self.ip_address = ""
        self.root.after(0, lambda: self.btn_connect.config(text="▶", bg=self.colors["success"]))
        self.hide_flyout()

    # ================== WEITERE FUNKTIONEN ==================
    def on_mode_change(self):
        mode = self.mode_var.get()
        self.config["mode"] = mode
        self.save_config()
        if self.display_mgr and self.is_connected:
            self.display_mgr.set_resolution(mode)

    def on_bitrate_change(self):
        self.bitrate_label.config(text=f"{self.bit_var.get()} Mbit/s")
        self.config["bitrate"] = self.bit_var.get()
        self.save_config()

    def update_transparency(self, value):
        alpha = float(value)
        self.root.attributes("-alpha", alpha)
        self.flyout_win.attributes("-alpha", alpha)
        self.config["window_alpha"] = alpha
        self.save_config()
        self.trans_label.config(text=f"{alpha:.2f}")

    def update_topmost(self):
        is_top = self.topmost_var.get()
        self.root.attributes("-topmost", is_top)
        self.flyout_win.attributes("-topmost", is_top)
        self.config["topmost"] = is_top
        self.save_config()

    def toggle_fullscreen_and_close(self):
        self.fullscreen_var.set(not self.fullscreen_var.get())
        self.save_config()
        if self.is_connected:
            self.scrcpy_mgr.stop()
            self.scrcpy_mgr.start(self.ip_address, f"{self.bit_var.get()}M", self.mode_var.get(),
                                  self.screen_off_var.get(), self.stay_awake_var.get(),
                                  self.fullscreen_var.get())
        self.hide_flyout()

    def set_orientation(self, orientation):
        if not self.is_connected or not self.display_mgr:
            return
        self.display_mgr.set_orientation(orientation)
        self.config["orientation"] = orientation
        self.save_config()

    def rotate_screen(self):
        if not self.is_connected or not self.display_mgr:
            return
        current = self.config.get("orientation", "0")
        new = str((int(current) + 1) % 4)
        self.set_orientation(new)

    def change_volume(self, delta):
        if not self.is_connected or not self.audio_mgr:
            return
        self.audio_mgr.change_volume(delta)

    def send_system_control(self, keycode):
        if not self.is_connected or not self.sys_control_mgr:
            self.show_status_flyout("status_not_connected", True, self.btn_controls)
            self.root.after(2000, self.hide_flyout)
            return
        self.sys_control_mgr.send_key(keycode)

    def copy_clipboard(self):
        if not self.is_connected or not self.clipboard_mgr:
            self.show_status_flyout("status_not_connected", True, self.btn_controls)
            self.root.after(2000, self.hide_flyout)
            return
        text = self.clipboard_mgr.copy_to_pc()
        if text:
            self.show_status_flyout("status_copied", False, self.btn_controls)
        else:
            self.show_status_flyout("status_clipboard_empty", True, self.btn_controls)
        self.root.after(2000, self.hide_flyout)

    def paste_clipboard(self):
        if not self.is_connected or not self.clipboard_mgr:
            self.show_status_flyout("status_not_connected", True, self.btn_controls)
            self.root.after(2000, self.hide_flyout)
            return
        self.clipboard_mgr.paste_to_phone()
        self.show_status_flyout("status_pasted", False, self.btn_controls)
        self.root.after(2000, self.hide_flyout)

    def close_app(self):
        if self.is_connected:
            if self.display_mgr:
                self.display_mgr.reset_on_exit()
            self.device_mgr.disconnect()
            self.scrcpy_mgr.stop()
        self.root.quit()

# ======================================================
# MAIN
# ======================================================
if __name__ == "__main__":
    import platform
    if platform.system() == "Windows":
        try:
            from ctypes import windll
            # Windows mitteilen, dass die App Per-Monitor DPI-aware ist
            try:
                windll.shcore.SetProcessDpiAwareness(2)
            except Exception:
                windll.user32.SetProcessDPIAware()
        except Exception:
            pass

    root = tk.Tk()
    
    # Tkinter zwingen, den echten DPI-Wert des Monitors für Schriften zu nutzen
    dpi = root.winfo_fpixels('1i')
    root.tk.call('tk', 'scaling', dpi / 72.0)

    app = HandheldConnect(root)
    root.mainloop()