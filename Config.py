import json

class Config():

    epValidate = "printer/validate_token"
    epAuthorize = "printer/auth.json"
    epMenus = "printer/menu_options"
    epQueue = "printer/get_queue/" #menu ID
    epSetPrinted = "printer/set_printed/" #order ID

    def validateItem(self, key):
        config = json.load(open('data.json'))
        return key in config

    def getItem(self, key):
        config = json.load(open('data.json'))
        return str(config[key])

    def updateItem(self, key, value):
        config = json.load(open('data.json'))
        config[key] = value
        with open("data.json", "w") as json_data:
            json.dump(config, json_data)

    def writeWifiConfig(self):
        config = json.load(open('data.json'))
        wpa_file = ""
        with open('wpa_supplicant.conf') as file:
            for line in file:
                if "network" in line: break
                wpa_file += line
        wpa_file += "network={\n ssid=\""+config['ssid']+"\"\n psk=\""+config['psk']+"\"\n}"
        with open('wpa_supplicant.conf', 'w') as f:
            f.write(wpa_file)

    def loadWifiConfig(self):
        is_network_block = False
        network_block = ""
        # TODO add home path to wpa conf file
        with open('wpa_supplicant.conf') as file:
            for line in file:
                line = line.rstrip()
                if not is_network_block:
                    is_network_block = "network" in line
                if not is_network_block: continue
                is_network_block = not "}" in line
                network_block += line
        return self.parseNetworkString(network_block)

    def parseNetworkString(self,network_string):
        if not network_string: return None
        json_string = json.loads(network_string.replace("network=","").replace("=","\":").replace(" p",",\"p").replace(" s","\"s"))
        return json_string
