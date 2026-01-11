# WiFiManager (MicroPython – ESP32)

Smart Wi-Fi manager for ESP32 using MicroPython.
Auto-connect, scan, JSON storage, and AP fallback.

# Requirements

- ESP32 board
- MicroPython (v1.20 or later preferred)
- Storage space for the configuration file (wifi.json)

## Installation

```bash
pip install esp32-wifimanager
```

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
from wifiManager import WiFiManager

wifi = WiFiManager(debug=True)
```

# Automatic connection Start STA if faild --> AP

```bash
print(wifi.connect())
```

# Start AP

```bash
print(wifi._ap())
```

# Check is connecting

```bash
print(wifi.is_connected())
```

# Check status

```bash
print(wifi.status())
```

# Stop AP and STA

```bash
print(wifi.stop_all())
```

# Stop STA

```bash
print(wifi.stop_sta())
```

# Stop AP

```bash
print(wifi.stop_ap())
```

# Add Wi-Fi network

```bash
print(wifi.add_network("MyWiFi", "11223344"))
```

# Delete one network

```bash
print(wifi.remove_network("Office"))
```

# Delete all networks

```bash
print(wifi.clear_networks())
```

# Checking nearby networks

```bash
print(wifi.scanner.scan())
```

# Show saved networks

```bash
print(wifi.storage.load_networks())
```
