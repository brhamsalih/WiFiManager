import machine, network
import time
import gc
from .scanner import WiFiScanner
from .storage import Storage


class WiFiManager():


    def __init__(self, config_file="/wifi.json", sta_timeout=10, ap_essid="ESP32_AP", ap_password="12345678", ap_channel=6, ap_max_clients=4, debug=False):
        self.debug = debug
        
        self.sta_timeout = sta_timeout
        self.ap_essid = ap_essid
        self.ap_password = ap_password
        self.ap_channel = ap_channel
        self.ap_hidden = False
        self.ap_max_clients = ap_max_clients
        
        self.wlan = network.WLAN(network.STA_IF)
        self.ap = network.WLAN(network.AP_IF)
  
        self.storage = Storage(config_file)
        self.scanner = WiFiScanner(self.wlan)
        
        self.STAT_GOT_IP = 1010
        self.STAT_WRONG_PASSWORD = 1001
        self.STAT_NO_AP_FOUND = 201

    def _load_candidates(self):
        saved = self.storage.load_networks()
        saved_dict = {n["ssid"]: n["password"] for n in saved}

        available = self.scanner.scan()
        nets = []

        for a in available:
            ssid = a["ssid"]
            if ssid in saved_dict:
                nets.append({
                    "ssid": ssid,
                    "password": saved_dict[ssid],
                    "rssi": a["rssi"],
                })

        nets.sort(key=lambda x: x["rssi"], reverse=True)
        gc.collect()
        return nets

   
    def _reset(self,mode):
        mode.active(False)
        time.sleep(1)
        mode.active(True)
        
    def _ap(self):
        self._reset(self.ap)

        self.ap.config(
            essid=self.ap_essid,
            password=self.ap_password,
            authmode=network.AUTH_WPA_WPA2_PSK,
            channel=self.ap_channel,
            max_clients=self.ap_max_clients 
        )

        self.ap.active(True)
        time.sleep(0.5)
        return {"status": "AP started", "IP": self.ap.ifconfig()[0]}

        
    

    def connect(self):
        self.wlan.active(True)
        time.sleep(1)
        
        if not self.wlan.isconnected():
            if self.debug:
                print('connecting to network...')
            candidates = self._load_candidates()
            
            if not candidates:
                self._ap()
                return{"STATUS": "NO LAN SAVED AROUND"}
                
                
            for net in candidates:
                if self.debug:
                    print("Trying:", net["ssid"], "RSSI:", net["rssi"])
                self.wlan.connect(net["ssid"], net["password"])
                    
                start = time.ticks_ms()
                machine.idle()
                time.sleep(self.sta_timeout)
                delta = time.ticks_diff(time.ticks_ms(), start)
                status = self.wlan.status()
                
                if int(delta) >= self.sta_timeout:
                    if status == self.STAT_GOT_IP:
                        return{"STATUS": "CONNECTED!","IP": self.wlan.ifconfig()[0]}
                    
                    if status == self.STAT_WRONG_PASSWORD:
                        self._reset(self.wlan)
                        self.wlan.active(False)
                        self._ap()
                        return {"STATUS": "WRONG PASSWORD!"}
                    
                    if status == self.STAT_NO_AP_FOUND:
                        self._reset(self.wlan)
                        self.wlan.active(False)
                        self._ap()
                        return {"STATUS": "LAN NOT FOUND"}
                    
                    self._ap()
                    return{"TIMEOUT": status}
                
            
        return{"STATUS": "CONNECTED!","IP": self.wlan.ifconfig()[0]}
    
    # ======================
    # STATUS
    # ======================

    def is_connected(self):
        return self.wlan.isconnected()

    def status(self):
        if self.wlan.isconnected():
            return {"MODE": "STA", "IP": self.wlan.ifconfig()}
        if self.ap.active():
            return {"MODE": "AP", "IP": self.ap.ifconfig()}
        return {"MODE": "OFF"}
    
    # ======================
    # Utilities
    # ======================
    def add_network(self, ssid, password):
        self.storage.save_network(ssid, password)
        return "OK"
    def remove_network(self, ssid):
        self.storage.remove_network(ssid)
        return "OK"
    def clear_networks(self):
        self.storage.clear()
        return "OK"
    def stop_all(self):
        self.wlan.active(False)
        self.ap.active(False)
        return "OK"
    def stop_sta(self):
        self.wlan.active(False)
        return "OK"
    def stop_ap(self):
        self.ap.active(False)
        return "OK"
        
