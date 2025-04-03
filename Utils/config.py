import json
import requests

from Game.Difficulty import Schwierigkeit

BASE_URL = "http://snakeworld.up.railway.app/highscore/"

class Config:

    def __init__(self):
        self.config_dict = None
        self.update()
        
    def pullHighscores(self):
        print("PULL")
        response = requests.get(BASE_URL+"leicht/highest")
        body = response.text
        if (response.ok) and body:
            self.config_dict["highscore"]["LEICHT"] = json.loads(body)["score"]
        else:
            print(f"Leicht Highscorce pull failed: {response.content}")
            
        response = requests.get(BASE_URL+"schwer/highest")
        body = response.text
        if (response.ok) and body:
            self.config_dict["highscore"]["SCHWER"] = json.loads(body)["score"]
        else:
            print(f"Schwer Highscorce pull failed: {response.content}")
            
        response = requests.get(BASE_URL+"mittel/highest")
        body = response.text
        if (response.ok) and body:
            self.config_dict["highscore"]["MITTEL"] = json.loads(body)["score"]
        else:
            print(f"Mittel Highscorce pull failed: {response.content}")
        
    def highscoreRequestPOST(self, highscore: int, name: str = "Unknown") -> requests.Response:
        data = {
            "score": highscore,
            "name": name
        }
        url = BASE_URL + f"{self.get_Difficulty().name.lower()}"
        response = requests.post(url, json = data)
        print("POST")
        if not (response.ok): 
            print(response.text)
        return response
        
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
        return self.config_dict["highscore"][self.get_Difficulty().name]
    
    def set_highscore(self, value: int, name = ""):
        if value > self.config_dict["highscore"][self.get_Difficulty().name]:
            response = self.highscoreRequestPOST(value, name)
            if response.ok:
                highscore = self.get_Value("highscore")
                highscore[self.get_Difficulty().name] = value
        
    def set_color(self, rot: int, gruen: int, blau: int):
        self.config_dict["color"] = [rot, gruen, blau]
        self.close()

