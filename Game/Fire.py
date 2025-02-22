import random

from Game import Obstical
from Utils import Settings


class Fire(Obstical):
    def __init__(self, position):
        super().__init__(position, "Game/textures/fire_pixel_art.jpeg")

    def draw(self, surface):
        surface.blit(self._texture, self._position)

    def get_random_nearby_position(self):
        match random.randint(0, 3):
            case 0:
                return self._position[0], self._position[1] + Settings.grid_size
            case 1:
                return self._position[0] + Settings.grid_size, self._position[1]
            case 2:
                return self._position[0], self._position[1] - Settings.grid_size
            case 3:
                return self._position[0] - Settings.grid_size, self._position[1]