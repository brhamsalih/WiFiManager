# WiFiManager (MicroPython – ESP32)

Smart Wi-Fi manager for ESP32 using MicroPython.
Auto-connect, scan, JSON storage, and AP fallback.

# Requirements

- ESP32 board
- MicroPython (v1.20 or later preferred)
- Storage space for the configuration file (wifi.json)

# Installation (via Thonny)

- Copy the entire wifiManager/ folder to the ESP32
- (Optional) Create a wifi.json file in the root directory
- The library is ready to use ✅

# Settings file (wifi.json)

```bash
{
  "networks": [
    { "ssid": "Home", "password": "12345678" },
    { "ssid": "Office", "password": "87654321" }
  ]
}
```

# How it Works

- Scan nearby networks
- Compare available networks with saved networks
- Select the network with the strongest signal
- Attempt to connect automatically
- If this fails → Turn on the Access Point

# Quick use

```bash
from wifi_manager import WiFiManager
wifi = WiFiManager()
```

# Automatic connection Start STA if faild --> AP

```bash
wifi.do_connect()
```

# Start AP

```bash
wifi.do_ap()
```

# Check is connecting

```bash
wifi.is_connected()
```

# Check status

```bash
wifi.status()
```

# Stop AP and STA

```bash
wifi.stop_all()
```

# Stop STA

```bash
wifi.stop_sta()
```

# Stop AP

```bash
wifi.stop_ap()
```

# Add Wi-Fi network

```bash
wifi.storage.save_network("MyWiFi", "password")
```

# Delete one network

```bash
wifi.storage.remove_network("Office")
```

# Delete all networks

```bash
wifi.storage.clear()
```

# Checking nearby networks

```bash
networks = wifi.scanner.scan()
```
