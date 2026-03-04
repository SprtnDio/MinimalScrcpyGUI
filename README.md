# 🎮 Minimalistic Scrcpy GUI v1.0

A high-performance, minimalistic Graphical User Interface for [Scrcpy](https://github.com/Genymobile/scrcpy). 
This tool is specifically designed for **Handheld Gaming PCs** (MSI Claw, Legion Go, ROG Ally, Steam Deck, etc.) and users who want a seamless, wireless Android-to-PC experience with zero clutter.

---

## ✨ Highlights & Key Features

### 🚀 Smart Connection (Autorun & Auto-IP)
- **Automatic IP Discovery:** The tool automatically detects all available IP addresses of your Android device via USB. 
- **One-Click Wireless:** It enables TCP/IP via USB and switches to Wi-Fi mode instantly. You can unplug the cable right after the stream starts.
- **Device Management:** Save multiple devices with custom names (e.g., "Retroid Pocket", "Pixel 8", "Odin 2") to switch between them effortlessly.

### 📐 Optimized for Handhelds & High-DPI
- **DPI-Aware Rendering:** Perfectly scales on high-resolution displays (e.g., Legion Go's 1600p screen). Whether you use 125% or 150% scaling, the GUI stays sharp and correctly sized.
- **Dynamic Flyout UI:** A borderless sidebar that stays at the edge of your screen, acting like a native system overlay to save precious screen real estate.
- **Auto-Fit Height:** The window calculates its height dynamically based on the buttons shown—no wasted space!

### 🎮 Professional Streaming Controls
- **Display Presets:** Switch between Original resolution, Tablet Mode (1200x1920), or Ultra Mode (1450x1920) with one click.
- **Power Management:** Features "Screen Off" mode (keep the phone display off while streaming) and "Stay Awake" to prevent the device from locking.
- **Audio & Bitrate:** Real-time volume control and a bitrate slider (up to 150 Mbit/s) for crystal clear image quality.
- **System Navigation:** Dedicated buttons for Back, Home, Recent Apps, and Power toggle.

### 📋 Clipboard Synchronization
- Copy text on your PC and paste it onto your handheld (or vice versa). Perfect for long passwords, URLs, or coordinates.

---

## 🛠️ Installation & Usage (For Users)

This GUI is a **standalone extension**. You still need the original Scrcpy files for it to work.

1. Download the official **[Scrcpy for Windows](https://github.com/Genymobile/scrcpy/releases)** and extract the ZIP folder.
2. Go to the **[Releases](../../releases)** tab on this GitHub page and download `MinimalScrcpyGUI.exe`.
3. Move `MinimalScrcpyGUI.exe` into your extracted Scrcpy folder (where `scrcpy.exe` and `adb.exe` are located).
4. Run `MinimalScrcpyGUI.exe`.

### How to Connect for the First Time:
1. Enable **USB Debugging** in the Developer Options on your Android device.
2. Connect the device to your PC via USB.
3. Click ▶ in the GUI and select **Autorun**.
4. Allow the debugging prompt on your phone's screen.
5. Once the stream starts, you can unplug the USB cable and enjoy the wireless connection!

---

## 👨‍💻 For Developers (Source Code)

If you want to modify the code or build the executable yourself:

1. Install Python 3.x.
2. Install dependencies: `pip install pillow pyinstaller`.
3. Compile the EXE using the following command:
   ```bash
   pyinstaller --noconsole --onefile --icon="app_icon.ico" --add-data "app_icon.ico;." --name="MinimalScrcpyGUI" handheld_connect.py

📜 Credits & License:
   GUI & Logic: SprtnDio
   Core Technology: Scrcpy by Genymobile.
   License: MIT License (see LICENSE file).
   
Disclaimer: This tool is an unofficial community project and is not affiliated with Genymobile.