
import pygame

from Utils import Config


class Einstellungen:

    def __init__(self, screen):
        self._surface = pygame.Surface(screen.get_size())
        self._screen = screen
        self._shouldClose = False

        self.config = Config()
        
        self.buttons = {}

        pygame.font.init()

        self.font = pygame.font.SysFont("monospace", 50, True)

        self.menu_options = ["SnakeColor", "Einstellungen", "Beenden"]
        self.selected_option = 0