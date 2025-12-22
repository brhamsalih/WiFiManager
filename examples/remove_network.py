from wifi_manager import WiFiManager

wifi = WiFiManager()
wifi.storage.remove_network("Office")

print("networks removed")
