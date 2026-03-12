<div align="center">

# CYBERPUNK AR TARGET LOCK HUD

### `>>> TERMINATOR VISION SYSTEM v1.0 <<<`

**Real-time Augmented Reality Wi-Fi Radar powered by ESP32 & OpenCV**

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-CAM-E7352C?style=for-the-badge&logo=espressif&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<br/>

[![Demo](esp_demo.gif)](./esp_demo.gif)

Demo here. If it does not load on GitHub due to network/cache, click this file: [esp_demo.gif](./esp_demo.gif)
<br>
*Walk around. Detect Wi-Fi signals. Lock on targets. Feel like a Terminator.*

</div>

---

## What is this?

A Python-powered AR Heads-Up Display that transforms a live wireless video stream from an **ESP32-CAM** into a **Terminator-style vision system**. It dynamically detects surrounding Wi-Fi networks using an ESP32 DevKit's RSSI scanner and renders them as floating, animated lock-on target brackets right on the camera feed.

**Think of it as**: Iron Man's HUD meets a Wi-Fi analyzer, running on $10 worth of hardware.

---

## Key Features

| Feature | Description |
|---|---|
| **Live AR Overlay** | Real-time target brackets rendered on the ESP32-CAM video stream at 1280x720 |
| **Wi-Fi RSSI Radar** | Scans nearby Wi-Fi networks and maps signal strength to visual target size |
| **Dynamic Lock-On** | Targets grow, change color, and trigger a laser lock line when signal is strong (> -50 dBm) |
| **Cyberpunk Aesthetic** | Green-tinted overlay, floating brackets, pulsating animations |
| **Auto Simulation Mode** | No ESP32 DevKit? System auto-falls back to simulated Wi-Fi targets for demo |
| **Graceful Reconnect** | Camera stream drops? Auto-reconnects without crashing |

---

## How It Works

```
                                    +-----------------+
                                    |   ESP32-CAM     |
                                    |  (Video Stream) |
                                    +--------+--------+
                                             |
                                        Wi-Fi Stream
                                        (MJPEG/HTTP)
                                             |
                                             v
+-----------------+              +-----------+-----------+
|  ESP32 DevKit   |   Serial    |                       |
|  (Wi-Fi Radar)  +------------>+   Python + OpenCV     |
|  RSSI Scanner   |   USB       |   AR Processing       |
+-----------------+              |                       |
                                 +-----------+-----------+
                                             |
                                       AR HUD Output
                                             |
                                             v
                                    +-----------------+
                                    |    Display      |
                                    | Terminator HUD  |
                                    +-----------------+
```

### Signal Strength → Visual Feedback

| RSSI Range | Color | Bracket Size | Status |
|---|---|---|---|
| **> -50 dBm** (Strong) | Red | Large (up to 150px) | `LOCKED` + laser line |
| **-70 to -50 dBm** (Medium) | Orange/Yellow | Medium | Tracking |
| **< -70 dBm** (Weak) | Green | Small (down to 20px) | Scanning |

---

## Hardware Requirements

| Component | Role | Required? |
|---|---|---|
| **ESP32-CAM** (OV3660/OV2640) | Wireless camera eye — streams live video over Wi-Fi | Yes |
| **ESP32 DevKit V1** | Wi-Fi radar — scans nearby networks and outputs RSSI via serial | Optional* |
| **USB Cable** | Connects ESP32 DevKit to your computer | Optional* |
| **Mac / PC** | Runs the Python processing script | Yes |

> *\*If the ESP32 DevKit is not connected, the system automatically enters **Simulation Mode** with 3 fake Wi-Fi targets (`Hidden_5G`, `Cyber_Router`, `Neighbor_Net`) for demo/testing purposes.*

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/cyberpunk-ar-hud.git
cd cyberpunk-ar-hud
```

### 2. Set up virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install opencv-python numpy pyserial
```

### Dependencies breakdown

| Package | Version | Purpose |
|---|---|---|
| `opencv-python` | 4.x+ | Video capture, image processing, AR rendering |
| `numpy` | 1.x+ | Signal interpolation and math operations |
| `pyserial` | 3.x+ | Serial communication with ESP32 DevKit |

---

## Hardware Setup

### ESP32-CAM (Camera Module)

1. Open **Arduino IDE**
2. Flash the standard **`CameraWebServer`** example sketch
3. Open **Serial Monitor** at `115200` baud
4. Note the IP address printed (e.g., `192.168.2.11`)
5. Verify the stream works by visiting: `http://<IP>:81/stream` in a browser

### ESP32 DevKit V1 (Wi-Fi Radar) — *Optional*

1. Flash a Wi-Fi scanning sketch to the DevKit
2. The sketch must output data in this exact format via Serial:

```
Muc tieu: <Network_Name> | RSSI): <value>dBm
```

**Example output:**
```
Muc tieu: MyHomeWiFi | RSSI): -45dBm
Muc tieu: Neighbor_5G | RSSI): -72dBm
Muc tieu: CoffeeShop | RSSI): -88dBm
```

3. Note the serial port (e.g., `/dev/cu.usbserial-0001` on macOS, `COM3` on Windows)

---

## Configuration

Open `main.py` and update these two variables at the top:

```python
# Replace with your ESP32-CAM's stream URL
cam_url = "http://192.168.2.11:81/stream"

# Replace with your ESP32 DevKit's serial port
esp_port = '/dev/cu.usbserial-0001'     # macOS
# esp_port = 'COM3'                     # Windows
# esp_port = '/dev/ttyUSB0'             # Linux
```

---

## Usage

```bash
python3 main.py
```

### What you'll see

```
>> [RADAR] Da ket noi DevKit V1!          # If ESP32 DevKit is connected
>> [RADAR] Chay gia lap song!             # If running in simulation mode
>> HE THONG TARGET LOCK DA KICH HOAT! Bam 'q' de tat.
```

### Controls

| Key | Action |
|---|---|
| `q` | Quit the HUD and release all resources |

### Tips for best results

- **Walk around** with the ESP32-CAM — the AR targets respond to real Wi-Fi signal changes
- **Get closer** to a Wi-Fi router to see the target bracket grow and turn **red**
- When RSSI exceeds **-50 dBm**, a **laser lock line** appears from the bottom center to the target
- Targets automatically **expire after 5 seconds** if the signal is lost
- The green tint overlay gives everything that **cyberpunk night-vision feel**

---

## Project Structure

```
cyberpunk-ar-hud/
├── main.py          # Core application — AR processing, rendering, serial I/O
├── esp_demo.gif     # Demo recording for README
├── README.md        # You are here
└── venv/            # Python virtual environment (not committed)
```

---

## Technical Details

### AR Rendering Pipeline

1. **Frame Capture** — Grab MJPEG frame from ESP32-CAM HTTP stream
2. **Resize** — Normalize to 1280x720 for consistent rendering
3. **RSSI Ingest** — Read serial data from ESP32 DevKit (or generate simulated data)
4. **Target Tracking** — Map each Wi-Fi network to a screen position with floating animation
5. **Signal Interpolation** — `numpy.interp()` maps RSSI [-95, -30] dBm → bracket size [20, 150] px
6. **Color Coding** — Red (locked) / Orange (tracking) / Green (scanning) based on signal strength
7. **Overlay Compositing** — Green-tinted cyberpunk overlay blended at 20% opacity
8. **Bracket Drawing** — Custom corner-bracket renderer for the lock-on effect
9. **Display** — Final composited frame shown via OpenCV `imshow`

### Simulation Mode

When no ESP32 DevKit is detected, the system generates 3 fake targets every 10 frames with random RSSI values between -90 and -40 dBm. This lets you develop and test the AR overlay without any hardware.

### Target Lifecycle

```
Signal Detected → Target Created (random screen position)
                → RSSI Updated (every scan cycle)
                → Target Expires (if no update for 5 seconds)
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| **Black screen / no video** | Check ESP32-CAM IP address. Visit `http://<IP>:81/stream` in browser first |
| **"Could not open video stream"** | Ensure ESP32-CAM and your computer are on the same Wi-Fi network |
| **Serial port not found** | Check port name: `ls /dev/cu.*` (macOS) or Device Manager (Windows) |
| **Laggy video feed** | Reduce resolution in ESP32-CAM web interface, or check Wi-Fi signal quality |
| **Targets not appearing** | Verify ESP32 DevKit serial output format matches expected pattern |
| **Script crashes on start** | Run `pip install opencv-python numpy pyserial` to ensure all deps are installed |

---

## Future Ideas

- [ ] Add sound effects (lock-on beep, scanning hum)
- [ ] Multi-camera support
- [ ] Record AR session to video file
- [ ] Web-based HUD via Flask/WebSocket
- [ ] Bluetooth device scanning overlay
- [ ] Distance estimation from RSSI using path-loss model
- [ ] Customizable HUD themes (Terminator, Iron Man, Cyberpunk 2077)

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

```bash
# Fork → Clone → Branch → Code → PR
git checkout -b feature/your-feature
git commit -m "Add: your feature description"
git push origin feature/your-feature
```

---

<div align="center">

**Built with caffeine and cyberpunk dreams**

`[ SYSTEM ONLINE ] [ TARGETS ACQUIRED ] [ HUD ACTIVE ]`

</div>

