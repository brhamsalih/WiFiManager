from wifiManager import WiFiManager

wifi = WiFiManager()
wifi.storage.remove_network("Office")

print("networks removed")
