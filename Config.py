import json

class Config():

    def getItem(self, key):
        config = json.load(open('data.json'))
        return str(config[key])

    def updateItem(self, key, value):
        config = json.load(open('data.json'))
        config[key] = value
        with open("data.json", "w") as json_data:
            json.dump(config, json_data)
