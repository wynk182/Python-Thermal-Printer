import json

config = json.load(open('data.json'))

class Config():

    def reload(self):
        config = json.load(open('data.json'))

    def getItem(self, key):
        self.reload()
        str(config[key])

    def updateItem(self, key, value):
        self.reload()
        config[key] = value
        with open("data.json", "w") as json_data:
            json_data.write(str(json_data))
