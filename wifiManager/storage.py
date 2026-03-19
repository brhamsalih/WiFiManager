import ujson
import os

class Storage:
    def __init__(self, file):
        self.file = file
    #AP Settings
    def load_settings(self):
        try:
            if not self.file or not self.file in os.listdir():
                return {}
            with open(self.file) as f:
                return ujson.loads(f.read())
        except:
            return {}

    def update_ap_settings(self,essid=None, password=None, channel=None):
        try:
            with open(self.file, "r") as f:
                settings = ujson.loads(f.read())
        except:
            settings = {}

        if "AP" not in settings:
            settings["AP"] = {}

        # essid
        if essid is not None:
            if essid.strip() != "":
                settings["AP"]["essid"] = essid
#             return {"STATUS": False, "ERROR": "ESSID cannot be empty."}


        # password
        if password is not None:
            if password.strip() != "":
                settings["AP"]["password"] = password
#             return {"STATUS": False, "ERROR": "Password cannot be empty."}
            

        # channel
        if channel is not None:
            if isinstance(channel, int) and channel in range(14):
                settings["AP"]["channel"] = channel
#             return {"STATUS": False, "ERROR": "Channel must be between 1 and 13."}

        with open(self.file, "w") as f:
            f.write(ujson.dumps(settings))

        return {"STATUS": True, "UPDATED": settings["AP"]}



    def load_networks(self):
        try:
            with open(self.file, "r") as f:
                data = ujson.load(f)
            return data.get("networks", [])
        except OSError:
            return []
        except ValueError:
            return []

    def save_network(self, ssid, password):
        data = {"networks": self.load_networks()}

        for n in data["networks"]:
            if n["ssid"] == ssid:
                n["password"] = password
                break
        else:
            data["networks"].append({
                "ssid": ssid,
                "password": password
            })

        with open(self.file, "w") as f:
            ujson.dump(data, f)
        return True
    
    def remove_network(self, ssid):
        nets = self.load_networks()
        new = [n for n in nets if n["ssid"] != ssid]

        if len(new) == len(nets):
            return False

        with open(self.file, "w") as f:
            ujson.dump({"networks": new}, f)

        return True

    def clear(self):
        try:
            with open(self.file, "r") as f:
                data = ujson.load(f)
        except:
            # في حال عدم وجود الملف نعيد بناءه
            data = {"networks": [], "AP": {}}
        data["networks"] = []
        with open(self.file, "w") as f:
            ujson.dump(data, f)
            
        return True


