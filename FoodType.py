import random
from enum import Enum


class FoodType(Enum):
    DOUBLE_UP = 1
    EXTRA_LIFE = 2
    NORMAL = 3

def random_food_type():
    if random.randint(1, 100) > 50:
        return FoodType.NORMAL
    if random.randint(1, 100) > 50:
        return FoodType.EXTRA_LIFE
    if random.randint(1, 100) > 50:
        return FoodType.DOUBLE_UP
    return FoodType.NORMAL