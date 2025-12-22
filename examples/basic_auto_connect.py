from wifi_manager import WiFiManager

wifi = WiFiManager()
mode = wifi.auto_connect()

print("Mode:", mode)
