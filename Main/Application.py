import sys
import pygame
from Menu import Menu
from Game import Schwierigkeit
from Game.SnakeGame import SnakeGame
from Utils import Settings

class Application:
    
    def __init__(self):
        pygame.init()

        self._screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        Settings.screen_width, Settings.screen_height = self._screen.get_size()
    
        Settings.grid_width = Settings.screen_width / Settings.grid_size
        Settings.grid_height = Settings.screen_height / Settings.grid_size


    def run(self):
        self.running = True

        while self.running:

            menu = Menu(self._screen)
            if Settings.DEBUG_MODE: print("Menu wurde erstellt.")
            menu.run()
            self.running = not menu.windowShouldClose()
            if Settings.DEBUG_MODE: print(f"Menu setzt self.running auf: {self.running}")

            if self.running:
                game = SnakeGame(Schwierigkeit.SCHWER, self._screen)
                if Settings.DEBUG_MODE: print("Game wurde erstellt.")
                game.run()
                self.running = not game.windowShouldClose()
                if Settings.DEBUG_MODE: print(f"Game setzt self.running auf: {self.running}")

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()