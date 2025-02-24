import random
import pygame

from Game import Colidable, Fire, Food, Obstacle
from Utils import Settings


class Map:
    
    def __init__(self,
                 surface: pygame.Surface,
                 background_colors: tuple = ((93, 216, 228), (84, 194, 205))):
        
        self._surface: pygame.Surface = surface
        
        self._background: pygame.Surface = pygame.Surface(self._surface.get_size())
        self._build_background(background_colors)
        
        self._obstacles: list[Obstacle] = []
        self._colidables: list[Colidable] = []
        self._food: list[Food] = []
        
    #food methodes
        
    def add_Food(self, food: Food):
        self._food.append(food)
        
    def add_Foods(self, foodList: list[Food]):
        for food in foodList:
            self._food.append(food)
    
    def remove_Food(self, food: Food):
        self._food.remove(food)
    

    def get_Foods(self, amount: int = None):
        if amount:
            return self._food[:amount+1]
        return self._food
            
    #obstacle methodes     
        
    def add_Obstacle(self, obs: Obstacle):
        self._obstacles.append(obs)
        
    def add_Obstacles(self, obsList: list[Obstacle]):
        for obs in obsList:
            self._obstacles.append(obs)
    
    def remove_Obstacle(self, obs: Obstacle):
        self._obstacles.remove(obs)
        
    def remove_random_Obstacle(self):
        if len(self._obstacles) > 1:
            random_obstacle = self._obstacles[random.randint(0, len(self._obstacles) - 1)]
            self._obstacles.remove(random_obstacle)
        
    #fire methodes    
        
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
            
    #coliable methodes        
    
    def add_Colidable(self, col: Colidable):
        self._obstacles.append(col)
    
    def add_Colidables(self, colList: list[Colidable]):
        for col in colList:
            self._obstacles.append(col)
        
    def remove_Colidable(self, col: Colidable):
        self._obstacles.remove(col)
    
    #map methodes
        
    def draw(self):
        
        self._surface.blit(self._background, (0, 0))
        
        for obs in self._obstacles:
            obs.draw(self._surface)
            
        for col in self._colidables:
            col.draw(self._surface)
            
        for food in self._food:
            food.draw(self._surface)
            
    def _build_background(self, back_colors):
        
        map_width, map_height = self._background.get_size()
        
        grid_size = Settings.grid_size
        grid_height = map_height / grid_size
        grid_width = map_width / grid_size
        
        for y in range(0, int(grid_height)):
            for x in range(0, int(grid_width)):
                r = pygame.Rect((x * grid_size, y * grid_size), (grid_size, grid_size))
                color = back_colors[0] if (x + y) % 2 == 0 else back_colors[1]
                pygame.draw.rect(self._background, color, r)
    
    def delete_all(self):
        self._obstacles = []
        self._colidables = []
        self._food = []
    