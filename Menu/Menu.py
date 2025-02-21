import pygame
from Main.Application import *
from Utils.colors import *
from Game.Settings import *

SCREEN_WIDTH = 1960
SCREEN_HEIGTH = 1080

class Menu():

    def __init__(self, surface, screen):
        self.surface = surface
        self.screen = screen
        self.shouldClose = False
        self.buttons = []

        pygame.font.init()

        self.font = pygame.font.SysFont("monospace", 50)

        self.menu_options = ["Start", "Einstellungen", "Beenden"]
        self.selected_option = 0

    def _handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__quit()
                self.shouldClose = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__quit()
                    self.shouldClose = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for text, text_rect, option in self.buttons:
                    if text_rect.collidepoint(pygame.mouse.get_pos()):
                        self._handleOptions(option)

    def _handleOptions(self, option: str):
        match(option):
            case "Start":
                self.__quit()
            case "Beenden":
                self.__quit()
                self.shouldClose = True

    def __draw_grid(self, surface):
        for y in range(0, int(Settings.grid_height)):
            for x in range(0, int(Settings.grid_width)):
                r = pygame.Rect((x * Settings.grid_size, y * Settings.grid_size),
                                (Settings.grid_size, Settings.grid_size))
                color = (93, 216, 228) if (x + y) % 2 == 0 else (84, 194, 205)
                pygame.draw.rect(surface, color, r)

    def __update_screen(self):
        self.screen.blit(self.surface, (0, 0))

        for i, option in enumerate(self.menu_options):
            color = RGBA_Black if i == self.selected_option else RGBA_GREY
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2,  SCREEN_HEIGTH//3 + i * 80))
            self.buttons.append((text, text_rect, option))
        for text, text_rect, option in self.buttons:
            self.screen.blit(text,text_rect)

        pygame.display.update()

    def run(self):
        self.running = True

        while self.running:

            self._handleEvents()

            self.__draw_grid(self.surface)

            self.__update_screen()


    def __quit(self):
        self.running = False

    def windowShouldClose(self) -> bool:
        return self.shouldClose