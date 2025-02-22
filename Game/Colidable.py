
import pygame
from Utils import Settings


class Colidable:
    
    def __init__(self, position: tuple[int, int], size: tuple[int, int], color: tuple[int, int, int]): #(0, 0) (2, 2)
        self._positionTopLeft = position
        self._size = size
        self._positions = []
        self._color = color
        
        for i in range(0, self._size[0]):
            for j in range(0, self._size[1]):
                self._positions.append(((self._positionTopLeft[0]+i*Settings.grid_size), (self._positionTopLeft[1]+j*Settings.grid_size)))
        
    def draw(self, surface):
        for pos in self._positions:
            r = pygame.Rect(pos, (Settings.grid_size, Settings.grid_size))
            pygame.draw.rect(surface,self._color, r)
            pygame.draw.rect(surface, (0, 0, 0), r, 1)

        
    def colidesWith(self, position):
        return position in self._positions