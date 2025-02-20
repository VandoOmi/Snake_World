import sys
import pygame
from Menu import Menu

class Application:
    
    def __init__(self):
        pygame.init()

        self._screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self._surface = pygame.Surface(self._screen.get_size())
        self._surface = self._surface.convert()

    def run(self):
        self.running = True

        while self.running:

            menu = Menu(self._surface, self._screen)
            menu.run()
            self.running = menu.windowShouldClose()

            if self.running:
                pass # Game

                if self.running:
                    pass #GameOver

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()