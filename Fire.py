import random
from unittest import case

import pygame
from annotated_types.test_cases import cases

from Settings import Settings


class Fire:
    def __init__(self, position):
        self.__position = position

    def get_position(self):
        return self.__position

    def set_position(self, pos):
        self.__position = pos

    def __randomize_position(self):
        self.__position = (random.randint(0, int(Settings.grid_width)-1) * Settings.grid_size,
                           random.randint(0, int(Settings.grid_height) - 1) * Settings.grid_size)

    def draw(self, surface):
        print(f"Fire position: {self.__position}, Type: {type(self.__position)}")

        pygame.draw.circle(surface, (255, 0, 0), (self.__position[0]-10, self.__position[1]-10), Settings.grid_size/2)

    def get_random_nearby_position(self):
        match random.randint(0, 3):
            case 0:
                return (self.__position[0], self.__position[1]+Settings.grid_size)
            case 1:
                return (self.__position[0]+Settings.grid_size, self.__position[1])
            case 2:
                return (self.__position[0], self.__position[1]-Settings.grid_size)
            case 3:
                return (self.__position[0]-Settings.grid_size, self.__position[1])