import random
import pygame

from Game import SnakeGame
from Utils import Settings


class Snake:
    def __init__(self,difficulty, color=(17, 47, 17)):
        self.__length = 1
        self.__positions = [((SnakeGame.map_width / 2),
                             (SnakeGame.map_height / 2))]
        self.__direction = random.choice(Settings.directions)
        self.__score = 0
        self.__life = 0
        self.__max_life = 0
        self.__temp_max_life = 0
        self.__color = (17, 47, 17)
        self.__difficulty = difficulty

    def turn(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.__direction:  # cannot do a 180
            self.__direction = new_direction

    def move(self):
        head_pos = self.get_head_position()
        x, y = self.__direction
        new = (((head_pos[0] + (x * Settings.grid_size)) % SnakeGame.map_width),
               (head_pos[1] + (y * Settings.grid_size)) % SnakeGame.map_height)
        if len(self.__positions) > 2 and new in self.__positions[2:]:
            self.decrease_life()
            if self.__life <= 0:
                return self.reset()

        else:
            self.__positions.insert(0, new)
            if len(self.__positions) > self.__length:
                self.__positions.pop()
            return False

    def decrease_life(self):
        if self.__life != 0:
            self.__life -= 1
        self.__max_life -= 1
        self.__positions = [((SnakeGame.map_width / 2),
                             (SnakeGame.map_height / 2))]

    def get_positions(self):
        return self.__positions

    def get_head_position(self):
        return self.__positions[0]

    def set_color(self, color):
        self.__color = color

    def set_max_life(self, max_life):
        self.__max_life = max_life
        self.__temp_max_life = max_life

    def reset(self):
        self.decrease_life()
        if Settings.DEBUG_MODE:
            print(f"Snake resets. ({self.get_life()})")
        if self.__life <= 0:
            self.reset_length()
            self.__positions = [
                ((SnakeGame.map_width / 2), (SnakeGame.map_height / 2))]
            self.__direction = random.choice(Settings.directions)
            self.saveHighscore()
            self.reset_variables()
            return True
        return False

    def get_highscore(self):
        with open("highscore/HighscoreSave", "r") as file:
            for line in file:
                    if ':' in line and f"highscore_{self.__difficulty.name}" in line:
                        highscore = int(line.split(':', 1)[1].strip())
                        break
        return highscore

    def saveHighscore(self):
        with open("highscore/HighscoreSave", "r") as datei:
            lines = datei.readlines()  
        highscore_updated = False
        for i, line in enumerate(lines):
            if ':' in line and f"highscore_{self.__difficulty.name}" in line:
                current_highscore = int(line.split(":")[1].strip()) 
                if self.get_score() > current_highscore:
                    lines[i] = f"highscore_{self.__difficulty.name}: {self.get_score()}\n" 
                    highscore_updated = True
                    break
        if highscore_updated:
            with open("highscore/HighscoreSave", "w") as datei:
                datei.writelines(lines) 


    def reset_variables(self):
        self.__score = 0
        self.__max_life = self.__temp_max_life
        self.__life = 0

    def increase_length(self, value=1):
        self.__length += value

    def half_length(self):
        self.__length = (self.__length - self.__length // 10) / 2
        self.__positions.__len__() / 2
        for i, __position in enumerate(self.__positions):
            if i > self.__length:
                self.__positions.pop(i)

                # Hallo Fabian

    def reset_length(self):
        self.__length = 1

    def increase_score(self, value):
        self.__score += value

    def get_score(self):
        return self.__score

    def reset_score(self):
        self.__score = 0

    def increase_life(self):
        if self.__life < self.__max_life:
            self.__life += 1

    def get_life(self):
        return self.__life

    def draw(self, surface):
        for pos in self.__positions:
            r = pygame.Rect((pos[0], pos[1]),
                            (Settings.grid_size, Settings.grid_size))
            pygame.draw.rect(surface, self.__color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)
