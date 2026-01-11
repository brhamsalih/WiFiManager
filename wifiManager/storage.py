import ujson


class Storage:
    def __init__(self, file):
        self.file = file

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

    def remove_network(self, ssid):
        nets = self.load_networks()
        new = [n for n in nets if n["ssid"] != ssid]

        if len(new) == len(nets):
            return False

        with open(self.file, "w") as f:
            ujson.dump({"networks": new}, f)

        return True

    def clear(self):
        with open(self.file, "w") as f:
            ujson.dump({"networks": []}, f)

