import pygame
from Utils import Settings
from Utils.colors import *
from Utils.config import *

class Map_Select:

    def __init__(self, screen: pygame.Surface):
        self._surface = pygame.Surface(screen.get_size())
        self._screen = screen
        self._shouldClose = False

        self.config = Config()
        
        self.buttons = {}

        pygame.font.init()

        self.font = pygame.font.SysFont("monospace", 50, True)

        maps_File = open("Menu/maps.json", "r")
        print(maps_File)
        self.maps_Json = json.load(maps_File)

        self.menu_options = ["Zum Menu"]
        for map in maps_File:
            self.menu_options.append(map)

        self.choosen_Map = {}
        self.selected_option = 0

    def _handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
                self._shouldClose = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._quit()
                    self._shouldClose = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for option in self.buttons:
                    if self.buttons[option][1].collidepoint(pygame.mouse.get_pos()):
                        self._handleOptions(option)

    def _handleOptions(self, option: str):
        if option == "Zum Menu":
            print("Zum Menu")
        else:
            self.choosen_Map = json.load(self.maps_Json[option])

    def _draw_background(self, surface):
        for y in range(0, int(Settings.grid_height)):
            for x in range(0, int(Settings.grid_width)):
                r = pygame.Rect((x * Settings.grid_size, y * Settings.grid_size), (Settings.grid_size, Settings.grid_size))
                color = (93, 216, 228) if (x + y) % 2 == 0 else (84, 194, 205)
                pygame.draw.rect(surface, color, r)

    def _update_screen(self):
        self._screen.blit(self._surface, (0, 0))
        
        for i, option in enumerate(self.menu_options):
            color = RGBA_BLACK if i == self.selected_option else RGBA_GREY
            text = self.font.render(option, False, (0, 0, 0))
            text_rect = text.get_rect(center=(Settings.screen_width//2,  (Settings.screen_height-400)//2 + 100 + i * 100))
            self.buttons[option] = (text, text_rect)

        
        menu_surf = pygame.Surface((520, 100+len(self.buttons)*100)).convert()
        menu_surf.fill("white")
        menu_surf.set_alpha(80)
        menu_surf_rect = menu_surf.get_rect(center=(Settings.screen_width//2, Settings.screen_height//2))
            
        self._screen.blit(menu_surf, menu_surf_rect)

        for text, rect in self.buttons.values():
            self._screen.blit(text, rect)

        pygame.display.update()

    def run(self):
        self.running = True

        while self.running:

            self._handleEvents()

            self._draw_background(self._surface)

            self._update_screen()
        


    def _quit(self):
        self.running = False

    def windowShouldClose(self) -> bool:
        return self._shouldClose