![PyPI version](https://img.shields.io/pypi/v/esp32-wifimanager)
![License](https://img.shields.io/pypi/l/esp32-wifimanager)

# WiFiManager (MicroPython – ESP32)

A smart and flexible Wi-Fi manager for ESP32 using MicroPython.
Supports auto-connect, AP fallback, JSON-based configuration, and dynamic network management.

---

## 🚀 Features

- Auto-connect to strongest saved network
- Fallback to Access Point (AP) mode
- JSON-based configuration (networks + AP settings)
- Quick connect to new networks
- Dynamic AP configuration
- Network scanning
- Lightweight and optimized for MicroPython

---

## 📦 Installation

```bash
pip install esp32-wifimanager
```

### Or manually:

- Copy `wifiManager/` folder to ESP32
- Create `wifi.json` file (optional)

---

## ⚙️ Configuration File (wifi.json)

```json
{
  "networks": [{ "ssid": "Home", "password": "12345678" }],
  "AP": {
    "essid": "ESP32_AP",
    "password": "12345678",
    "channel": 6
  }
}
```

---

## ⚡ Quick Start

```python
from wifiManager import WiFiManager

wifi = WiFiManager(debug=True)
print(wifi.connect())
```

---

## 🔌 Connection Flow

1. Scan nearby networks
2. Match with saved networks
3. Connect to strongest signal
4. If failed → Start AP mode

---

## 📡 Quick Connect (New 🔥)

Connect to a network and save it automatically:

```python
wifi.quick_connect("MyWiFi", "12345678")
```

---

## 📊 Status APIs

### STA Status

```python
wifi.status_sta()
```

Output:

```json
{
  "status": true,
  "ssid": "MyWiFi",
  "ip": "192.168.1.10"
}
```

### AP Status

```python
wifi.status_ap()
```

---

## 📡 Access Point Control

### Start AP

```python
wifi._ap()
```

### Update AP Settings

```python
wifi.update_ap(essid="NEW_AP", password="87654321", channel=11)
```

---

## 📁 Network Management

### Add Network

```python
wifi.add_network("MyWiFi", "12345678")
```

### Remove Network

```python
wifi.remove_network("MyWiFi")
```

### Clear All Networks

```python
wifi.clear_networks()
```

---

## ⛔ Stop Interfaces

```python
wifi.stop_all()
wifi.stop_sta()
wifi.stop_ap()
```

---

## 📡 Scan Networks

```python
wifi.scanner.scan()
```

---

## ⚠️ Migration Guide (v1 → v2)

### ❌ Old

```python
wifi = WiFiManager(ap_essid="ESP32", ap_password="12345678")
wifi.connect()
```

### ✅ New

```python
wifi = WiFiManager()
wifi.connect()
```

👉 AP settings are now stored in `wifi.json`

---

### ❌ Old Response

```json
{ "STATUS": "CONNECTED!", "IP": "..." }
```

### ✅ New Response

```json
{ "status": true, "ip": "..." }
```

---

## 🧠 Notes

- AP settings are persistent via JSON
- `quick_connect()` automatically saves networks
- Better memory handling and stability
- Designed for IoT production use

---

## 📜 License

MIT License
