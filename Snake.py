import random

import pygame

from Settings import Settings


class Snake:
    def __init__(self):
        self.__length = 1
        self.__positions = [((Settings.screen_width / 2), (Settings.screen_height / 2))]
        self.__direction = random.choice(Settings.directions)
        self.__color = (17, 24, 47)
        self.__score = 0
        self.__life = 0
        self.__max_life = 3

    def turn(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.__direction:  # cannot do a 180
            self.__direction = new_direction

    def move(self):
        head_pos = self.get_head_position()
        x, y = self.__direction
        new = (((head_pos[0] + (x * Settings.grid_size)) % Settings.screen_width),
               (head_pos[1] + (y * Settings.grid_size)) % Settings.screen_height)
        if len(self.__positions) > 2 and new in self.__positions[2:]:
            self.decrease_life()
            if self.__life == 0:
                self.reset()
                return False
        else:
            self.__positions.insert(0, new)
            if len(self.__positions) > self.__length:
                self.__positions.pop()
            return True

    def decrease_life(self):
        if self.__life != 0:
            self.__life -= 1
        self.__max_life -= 1
        self.__positions = [((Settings.screen_width / 2), (Settings.screen_height / 2))]

    def get_positions(self):
        return self.__positions

    def get_head_position(self):
        return self.__positions[0]

    def reset(self):
        self.decrease_life()
        if self.__life <= 0:
            self.reset_length()
            self.__positions = [((Settings.screen_width / 2), (Settings.screen_height / 2))]
            self.__direction = random.choice(Settings.directions)
            self.saveHighscore()
            self.reset_variables()
            

    def get_highscore(self):
        with open("highscore/HighscoreSave", "r") as file:
            line = file.readline().strip()  
            highscore = int(line.split(": ")[1]) 
        return highscore
            
    def saveHighscore(self):
        if self.get_score() > self.get_highscore():
            with open("highscore/HighscoreSave", "w") as file:
                file.write(f"highscore: {self.get_score()}")  

    def reset_variables(self):
        self.__score = 0
        self.__max_life = 3
        self.__life = 0

    def increase_length(self):
        self.__length += 1

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
            r = pygame.Rect((pos[0], pos[1]), (Settings.grid_size, Settings.grid_size))
            pygame.draw.rect(surface, self.__color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)
