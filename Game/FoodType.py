import random
from enum import Enum
from .Difficulty import *


class FoodType(Enum):
    DOUBLE_UP = 1
    EXTRA_LIFE = 2
    NORMAL = 3


def random_food_type(difficulty):
    x =random.randint(1,100)
    if x <= difficulty.normal_food:
        return FoodType.NORMAL
    if x <= difficulty.extra_life_food:
        return FoodType.EXTRA_LIFE
    if x <= difficulty.blue_food:
        return FoodType.DOUBLE_UP
    return FoodType.NORMAL

