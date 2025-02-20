from enum import Enum


class Schwierigkeit(Enum):
    LEICHT = (float(0.25), int(5), float(50), float(40), float(10))
    MITTEL = (float(0.75), int(3), float(50), float(25), float(25))
    SCHWER = (float(1), int(1),  float(10),float (25), float(65))

    def __init__(self, speed, max_life, normal_food, extra_life_food, blue_food):
        self._speed = speed
        self._max_life = max_life
        self._normal_food = normal_food
        self._extra_life_food = extra_life_food
        self._blue_food = blue_food

    @property
    def speed(self):
        return self._speed

    @property
    def max_life(self):
        return self._max_life

    @property
    def normal_food(self):
        return self._normal_food

    @property
    def extra_life_food(self):
        return self._extra_life_food

    @property
    def blue_food(self):
        return  self._blue_food
