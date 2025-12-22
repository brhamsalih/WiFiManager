from wifiManager import WiFiManager

wifi = WiFiManager()
mode = wifi.auto_connect()

print("Mode:", mode)
