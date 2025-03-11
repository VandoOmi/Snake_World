import json

from Game.Difficulty import Schwierigkeit


class Config:

    def __init__(self):
        self.update()
        
    def update(self):
        file = open("Utils/config.json", "r")
        self.config_dict = json.load(file)
        file.close()

    def get_Value(self, setting: str):
        return self.config_dict[setting]

    def set_Value(self, setting: str, value):
        self.config_dict[setting] = value

    def close(self):
        file = open("Utils/config.json", "r+")
        file.write(json.dump(self.config_dict))
        file.close()
    
    def close(self):
        with open("Utils/config.json", "w") as file:
            json.dump(self.config_dict, file, indent=4) 


    def get_Difficulty(self):
        if self.config_dict["Difficulty"] == "SCHWER":
            return Schwierigkeit(Schwierigkeit.SCHWER)
        elif self.config_dict["Difficulty"] == "LEICHT":
            return Schwierigkeit(Schwierigkeit.LEICHT)
        else:
            return Schwierigkeit(Schwierigkeit.MITTEL)
        
    def get_highscore(self):
        highscore = self.get_Value("highscore")
        return highscore[self.get_Difficulty().name]
    
    def set_highscore(self, value: int):
        highscore = self.get_Value("highscore")
        highscore[self.get_Difficulty().name] = max(value,highscore[self.get_Difficulty().name])
        
