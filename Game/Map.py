import random
import pygame

from Game import Colidable, Fire, Obstical
from Utils import Settings


class Map:
    
    def __init__(self,
                 surface: pygame.Surface,
                 background_colors: tuple = ((93, 216, 228), (84, 194, 205))):
        
        self._surface: pygame.Surface = surface
        
        self._background: pygame.Surface = pygame.Surface(self._surface.get_size())
        self._build_background(background_colors)
        
        self._obstacles: list[Obstical] = []
        self._colidables: list[Colidable] = []
        
    def add_Obstacle(self, obs: Obstical):
        self._obstacles.append(obs)
        
    def add_Obstacles(self, obsList: list[Obstical]):
        for obs in obsList:
            self._obstacles.append(obs)
    
    def add_Colidable(self, col: Colidable):
        self._obstacles.append(col)
    
    def add_Colidables(self, colList: list[Colidable]):
        for col in colList:
            self._obstacles.append(col)
    
    def remove_Obstacle(self, obs: Obstical):
        self._obstacles.remove(obs)
        
    def remove_random_Obstacle(self):
        if len(self._obstacles) > 1:
            random_obstacle = self._obstacles[random.randint(0, len(self._obstacles) - 1)]
            self._obstacles.remove(random_obstacle)
        
    def remove_Colidable(self, col: Colidable):
        self._obstacles.remove(col)
        
    def spread_fire(self, snake_positions):
        fires = self.get_Fires()
        position = (0, 0)
        run = True
        while run:
            position = fires[random.randint(0, len(fires) - 1)].get_random_nearby_position()
            for snake_pos in snake_positions:
                run = position == snake_pos
        self.add_Obstacle(Fire(position))
        
    def get_Fires(self):
        fires = []
        for obs in self._obstacles:
            if isinstance(obs, Fire):
                fires.append(obs)
        return fires
        
    def draw(self):
        
        self._surface.blit(self._background)
        
        for obs in self._obstacles:
            obs.draw(self._surface)
            
        for col in self._colidables:
            col.draw(self._surface)
            
    def _build_background(self, back_colors):
        
        grid_height = Settings.grid_height
        grid_width = Settings.grid_height
        grid_size = Settings.grid_size
        
        for y in range(0, int(grid_height)):
            for x in range(0, int(grid_width)):
                r = pygame.Rect((x * grid_size, y * grid_size), (grid_size, grid_size))
                color = back_colors[0] if (x + y) % 2 == 0 else back_colors[1]
                pygame.draw.rect(self._background, color, r)
    