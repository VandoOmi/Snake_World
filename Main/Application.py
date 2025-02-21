import sys
import pygame
from Menu import Menu
from Game.SnakeGame import *

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
            print("Menu wurde erstellt.")
            menu.run()
            self.running = not menu.windowShouldClose()
            print(f"Menu setzt self.running auf: {self.running}")

            if self.running:
                game = SnakeGame(Schwierigkeit.MITTEL, self._surface, self._screen)
                print("Game wurde erstellt.")
                game.run()
                self.running = not game.windowShouldClose()
                print(f"Game setzt self.running auf: {self.running}")

                if self.running:
                    pass #GameOver

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()