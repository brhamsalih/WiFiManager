import network
import time
import ujson
import os

from .storage import Storage
from .scanner import WiFiScanner

class WiFiManager:
    def __init__(self, config_file="/wifi.json", sta_timeout=15, ap_essid="ESP32_AP", ap_password="12345678", ap_channel=6):
        
        self.sta_timeout = sta_timeout
        self.ap_essid = ap_essid
        self.ap_password = ap_password
        self.ap_channel = ap_channel

        self.sta = network.WLAN(network.STA_IF)
        self.ap = network.WLAN(network.AP_IF)
        
        self.storage = Storage(config_file)
        self.scanner = WiFiScanner(self.sta)

    # ===============================
    # Rest Interface AP, STA
    # ===============================

    def _reset_iface(self, iface):
        iface.active(False)
        time.sleep(0.5)
        iface.active(True) 

    # ===============================
    # STA
    # ===============================

    def connect_sta(self, ssid, password):
        self._reset_iface(self.sta)

        if self.sta.isconnected():
            self.sta.disconnect()
            time.sleep(0.5)

        self.sta.connect(ssid, password)

        start = time.time()
        while not self.sta.isconnected():
            if time.time() - start > self.sta_timeout:
                return False
            time.sleep(0.2)

        return True

    # ===============================
    # AP
    # ===============================

    def start_ap(self):
        self._reset_iface(self.ap)

        self.ap.config(
            essid=self.ap_essid,
            password=self.ap_password,
            authmode=network.AUTH_WPA_WPA2_PSK,
            channel=self.ap_channel
        )

        timeout = 0
        while not self.ap.active() and timeout < 50:
            time.sleep(0.1)
            timeout += 1

        return self.ap.active()

    # ===============================
    # Auto Manager
    # ===============================

    def auto_connect(self):
        saved = self.storage.load_networks()
        available = self.scanner.scan()
        candidates = []
        for a in available:
            for s in saved:
                if a["ssid"] == s["ssid"]:
                    candidates.append({
                        "ssid": a["ssid"],
                        "password": s["password"],
                        "rssi": a["rssi"]
                    })

        candidates.sort(key=lambda x: x["rssi"], reverse=True)

        for net in candidates:
            if self.connect_sta(net["ssid"], net["password"]):
                return "STA"
        self.start_ap()
        return "AP"

    def set_wifi(self, ssid, password):
        self.storage.load_networks()
        return self.connect_sta(ssid, password)

    def status(self):
        if self.sta.isconnected():
            return {"mode": "STA", "ip": self.sta.ifconfig()}
        if self.ap.active():
            return {"mode": "AP", "ip": self.ap.ifconfig()}
        return {"mode": "OFF"}


    # ===============================
    # Stop All, AP and STA
    # ===============================

    def stop_all(self):
        self.sta.active(False)
        self.ap.active(False)
        
    def stop_sta(self):
        self.sta.active(False)
        
    def stop_ap(self):
        self.ap.active(False)

