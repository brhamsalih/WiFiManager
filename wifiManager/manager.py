import machine, network
import time
import gc
from .scanner import WiFiScanner
from .storage import Storage


class WiFiManager():


    def __init__(self, config_file="wifi.json", sta_timeout=5, debug=False, hostname="esp32"):
        self.debug = debug
        self.storage = Storage(config_file)
        self.sta_timeout = sta_timeout
        
        self.settings = self.storage.load_settings()
        self.ap_cfg = self.settings.get("AP", {})
        self.ap_essid = self.ap_cfg.get("essid")
        self.ap_password = self.ap_cfg.get("password")
        self.ap_channel = self.ap_cfg.get("channel")
        
        self.wlan = network.WLAN(network.STA_IF)
        self.hostname = hostname
        self.scanner = WiFiScanner(self.wlan)
        self.ap = network.WLAN(network.AP_IF)
        
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
        if not self.is_ap_connected():
            self._reset(self.ap)
            self.ap.config(essid=self.ap_essid, password=self.ap_password, authmode=network.AUTH_WPA_WPA2_PSK)
            self.ap.config(channel=self.ap_channel)
        
            time.sleep(0.5)
            return self.status_ap()
        
        return self.status_ap()


    def quick_connect(self,ssid, pwd):
        self._reset(self.wlan)
        time.sleep(1)
        self.wlan.config(dhcp_hostname=self.hostname)
        if self.debug:
            print("Trying:", ssid)
        self.wlan.connect(ssid, pwd)
        start = time.ticks_ms()
        machine.idle()
        time.sleep(self.sta_timeout)
        delta = time.ticks_diff(time.ticks_ms(), start)
        status = self.wlan.status()
        if int(delta) >= self.sta_timeout:
            if status == self.STAT_GOT_IP:
                self.add_network(ssid, pwd)
                return self.status_sta()
            if status == self.STAT_WRONG_PASSWORD:
                self._reset(self.wlan)
                self.wlan.active(False)
                self.connect()
                return {"status": "WRONG PASSWORD!"}
            if status == self.STAT_NO_AP_FOUND:
                self._reset(self.wlan)
                self.wlan.active(False)
                self.connect()
                return {"status": "LAN NOT FOUND"}
    
    def connect(self):
        self.wlan.active(True)
        time.sleep(1)
        self.wlan.config(dhcp_hostname=self.hostname)
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
                        return self.status_sta() 
                    
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
                
            
        return self.status_sta()
    
    # ======================
    # STATUS
    # ======================

    def is_connected(self):
        return self.wlan.isconnected()
    
    def is_ap_connected(self):
        if self.ap.active():
            return True
        return False

    def status_sta(self):
        if self.wlan.isconnected():
            return {"status": True, "ssid": self.wlan.config('essid'), "ip": self.wlan.ifconfig()[0]}
        return {"status": False}
    
    def _format_mac(self, m):
        return ':'.join('{:02X}'.format(b) for b in m)

    def status_ap(self):
        if self.ap.active():
            current_channel = self.ap.config('channel')
            raw_clients = self.ap.status('stations')
            clients = [self._format_mac(c[0]) for c in raw_clients]

            ip, mask, gw, dns = self.ap.ifconfig()

            return {
                "status": True,
                "ip": ip,
                "netmask": mask,
                "gateway": gw,
                "dns": dns,
                "clients": len(clients),
                "channel": current_channel,
                "mac": clients
            }

        return {"status": False}

    
    # ======================
    # Utilities
    # ======================
    def update_ap(self,essid=None, password=None, channel=None):
        edit = self.storage.update_ap_settings(essid=essid, password=password, channel=channel)
        return edit
    def add_network(self, ssid, password):
        self.storage.save_network(ssid, password)
        return True
    def remove_network(self, ssid):
        remove_network = self.storage.remove_network(ssid)
        return remove_network
    def clear_networks(self):
        clear_networks = self.storage.clear()
        return clear_networks
    def stop_all(self):
        self.wlan.active(False)
        self.ap.active(False)
        return True
    def stop_sta(self):
        self.wlan.active(False)
        return True
    def stop_ap(self):
        self.ap.active(False)
        return True
        

