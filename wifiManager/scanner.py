import time
import gc

class WiFiScanner:
    def __init__(self, sta, debug=False):
        self.debug = debug
        self.sta = sta

    def scan(self, min_rssi=-90):
        if not self.sta.active():
            self.sta.active(True)
            time.sleep(0.3)

        nets = []

        try:
            scan_results = self.sta.scan()
            for n in scan_results:
                time.sleep(0) 

                try:
                    ssid = n[0].decode()
                    rssi = n[3]
                    auth = n[4]
                except:
                    continue

                if ssid and rssi >= min_rssi:
                    nets.append({
                        "ssid": ssid,
                        "rssi": rssi,
                        "auth": auth
                    })

        except Exception as e:
            if self.debug:
                print("WiFi scan error:", e)

        nets.sort(key=lambda x: x["rssi"], reverse=True)

        gc.collect() 

        return nets

