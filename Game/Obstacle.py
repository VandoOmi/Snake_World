import pygame


class Obstacle:
    
    def __init__(self, position, texture_path: str = None, color: tuple[int, int, int] = None):
        self._position = position
        if texture_path:
            self._texture = pygame.image.load(texture_path).convert()
            self._texture.set_colorkey((255, 255, 255))
            x, y = self._texture.get_size()
            self._texture = pygame.transform.scale(self._texture, (x/9, y/9))
        elif color:
            self._color = color 
            
    def get_position(self):
        return self._position

    def set_position(self, pos):
        self._position = pos
        
    def draw(self, surface):
        pass
        