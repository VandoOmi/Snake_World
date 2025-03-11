import pygame
from Menu.ColorChooser import ColorChooser
from Menu.Einstllungen import Einstellungen
from Utils import Settings
from Utils.colors import *
from Utils.config import *


class Menu:

    def __init__(self, screen: pygame.Surface):
        self._screen = screen
        self._shouldClose = False
        self._surface = pygame.Surface(screen.get_size())
        
        self._isEinstellungenOffen = False
        
        self.config = Config()

        self._init_menu() #Init MenuOptions and Font
        
    def _init_menu(self):
        self.buttons = {}
        self.menu_font = pygame.font.SysFont("monospace", 50, True)
        self.info_font = pygame.font.SysFont("monospace", 30, True)
        self.menu_options = ["Start", "Einstellungen","Farb Wahl", "Beenden"]
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
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_option = (self.selected_option + 1)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.selected_option = (self.selected_option - 1)
                elif event.key == pygame.K_RETURN:
                    self._handleOptions(self.menu_options[self.selected_option])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for option in self.buttons:
                    if self.buttons[option][1].collidepoint(pygame.mouse.get_pos()):
                        self._handleOptions(option)

    def _handleOptions(self, option: str):
        match(option):
            case "Start":
                self._quit()
                return
            case "Einstellungen":
                ein = Einstellungen(self._screen)
                ein.run()
                if ein.windowShouldClose():
                    self._shouldClose = True
                return
            case "Farb Wahl":
                c = ColorChooser()
                c.run()
                return
            case "Beenden":
                self._quit()
                self._shouldClose = True
                return

    def _draw_background(self, surface):
        for y in range(0, int(Settings.grid_height)):
            for x in range(0, int(Settings.grid_width)):
                r = pygame.Rect((x * Settings.grid_size, y * Settings.grid_size),
                                (Settings.grid_size, Settings.grid_size))
                color = (93, 216, 228) if (x + y) % 2 == 0 else (84, 194, 205)
                pygame.draw.rect(surface, color, r)

    def _build_info_box(self):
        self.back_info_box = pygame.Surface((520, 180)).convert()
        self.back_info_box.fill('white')
        self.back_info_box.set_alpha(100)
        
        self.info_box = pygame.Surface((520, 180)).convert()
        self.info_box.fill('white')
        self.info_box.set_colorkey('white')
        
        self.info_bex_rect = self.info_box.get_rect()
        self.info_bex_rect.right = self.menu_surf_rect.left
        self.info_bex_rect.centery = Settings.screen_height//2
        
        text_color = (80, 80, 80)
        
        highscore = self.info_font.render(f"Highscore: {self.config.get_highscore()}", False, text_color)
        highscore_rect = highscore.get_rect(center=(520//2,  60))
        
        schwierigkeit = self.info_font.render(f"Schwierigkeit: {self.config.get_Difficulty().name}", False, text_color)
        schwierigkeit_rect = schwierigkeit.get_rect(center=(520//2, 120))
        
        self.info_box.blit(highscore, highscore_rect)
        self.info_box.blit(schwierigkeit, schwierigkeit_rect)
                
    def _update_screen(self):
        self._screen.blit(self._surface, (0, 0))
        
        back_menu_surf = pygame.Surface((520, 100 + (100*len(self.menu_options)))).convert()
        back_menu_surf.fill("white")
        back_menu_surf.set_alpha(100)
        self.menu_surf_rect = back_menu_surf.get_rect(center=(Settings.screen_width//2, Settings.screen_height//2))
        self._build_info_box()
        
        self._screen.blit(back_menu_surf, self.menu_surf_rect)
        self._screen.blit(self.back_info_box, self.info_bex_rect)
        
        menu_surf = pygame.Surface((520, 100 + (100*len(self.menu_options)))).convert()
        menu_surf.fill("white")
        menu_surf.set_colorkey('white')

        for i, option in enumerate(self.menu_options):
            color = 'black' if i == self.selected_option else (100, 100, 100)
            text = self.menu_font.render(option, False, color)
            text_rect = text.get_rect(center=(520//2,  100 + i * 100))
            self.buttons[option] = (text, text_rect)
        for text, rect in self.buttons.values():
            menu_surf.blit(text, rect)
            
        self._screen.blit(menu_surf, self.menu_surf_rect)
        self._screen.blit(self.info_box, self.info_bex_rect)

        pygame.display.update()

    def get_difficulty(self):
        return self.config.get_Difficulty()

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
