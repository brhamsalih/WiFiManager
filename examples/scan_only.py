from wifiManager import WiFiManager

wifi = WiFiManager()

for net in wifi.scanner.scan():
    print(net["ssid"], net["rssi"])
