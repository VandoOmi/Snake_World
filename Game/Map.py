import pygame

from Game import Colidable, Obstical
from Utils import Settings


class Map:
    
    def __init__(self,
                 surface: pygame.Surface,
                 background_colors: tuple[tuple[int, int, int], tuple[int, int, int]] = ((93, 216, 228), (84, 194, 205))):
        
        self._surface: pygame.Surface = surface
        self._background: pygame.Surface = pygame.Surface(self._surface)
        if background_colors: self._background_colors = background_colors 
        
        self._obstacles: list[Obstical] = []
        self._colidables: list[Colidable] = []
        
    def add_Obstacles(self, obs: Obstical):
        self._obstacles.append(obs)
    
    def add_Colidables(self, col: Colidable):
        self._obstacles.append(col)
    
    def remove_Obstacles(self, obs: Obstical):
        self._obstacles.remove(obs)
    
    def remove_Colidables(self, col: Colidable):
        self._obstacles.remove(col)
        
    def draw(self):
        
        self._build_background()
        self._surface.blit(self._background)
        
        for obs in self._obstacles:
            obs.draw(self._surface)
            
        for col in self._colidables:
            col.draw(self._surface)
            
    def _build_background(self):
        
        grid_height = Settings.grid_height
        grid_width = Settings.grid_height
        grid_size = Settings.grid_size
        
        for y in range(0, int(grid_height)):
            for x in range(0, int(grid_width)):
                r = pygame.Rect((x * grid_size, y * grid_size), (grid_size, grid_size))
                color = self._background_colors[0] if (x + y) % 2 == 0 else self._background_colors[1]
                pygame.draw.rect(self._background, color, r)
    