import json


class Config:

    def __init__(self):
        file = open("Utils/config.json", "r+")
        self.config_dict = json.load(file)
        file.close()

    def get_Value(self, setting: str):
        return self.config_dict[setting]
    
    def set_Value(self, setting: str, value):
        self.config_dict[setting] = value

    def close(self):
        file = open("Utils/config.json", "r+")
        file = json.dump(self.config_dict)
        file.close()
    