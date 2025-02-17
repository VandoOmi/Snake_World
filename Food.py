import random

import pygame

from FoodType import FoodType
from Settings import Settings


class Food:
    def __init__(self, food_type):
        self.__position = (0, 0)
        self.__food_type = food_type
        self.__randomize_position()

    def get_position(self):
        return self.__position

    def get_food_type(self):
        return self.__food_type

    def set_position(self, pos):
        self.__position = pos

    def __randomize_position(self):
        self.__position = (random.randint(0, int(Settings.grid_width) - 1) * Settings.grid_size,
                           random.randint(0, int(Settings.grid_height) - 1) * Settings.grid_size)

    def draw(self, surface):
        r = pygame.Rect((self.__position[0], self.__position[1]), (Settings.grid_size, Settings.grid_size))
        pygame.draw.rect(surface, (255, 0, 0), r)
        if self.__food_type == FoodType.DOUBLE_UP:
            pygame.draw.rect(surface, (0, 0, 255), r)
        elif self.__food_type == FoodType.EXTRA_LIFE:
            pygame.draw.rect(surface, (0, 255, 0), r)
        else:
            pygame.draw.rect(surface, (255, 0, 0), r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)
