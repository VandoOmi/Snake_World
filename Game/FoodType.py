import random
from enum import Enum
from .Difficulty import *


class FoodType(Enum):
    DOUBLE_UP = 1
    EXTRA_LIFE = 2
    NORMAL = 3


def random_food_type(difficulty):
    x = random.randint(1, 100)
    if x <= difficulty.blue_food:
        return FoodType.DOUBLE_UP
    elif x <= difficulty.extra_life_food + difficulty.blue_food:
        if difficulty.name != "schwer":
            return FoodType.EXTRA_LIFE

    return FoodType.NORMAL
