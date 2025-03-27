import pygame

from Utils import Settings
from Utils.colors import *

class GameOver:
    
    def __init__(self, screen):
        from Utils.config import Config
        self._screen = screen
        self._surface = pygame.Surface(self._screen.get_size())
        self._shouldClose = False
        self.backToMenu = False
        self._running = True
        
        self.buttons = {}
        
        self.config = Config()
        
        self.menu_font = pygame.font.SysFont("monospace", 50, True)
        self.info_font = pygame.font.SysFont("monospace", 30, True)
        
        self.menu_options = ["Neuer Versuch", "Zum Menu", "Beenden"]
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
                    # um wieder oben zu starten
                    if self.selected_option >= len(self.menu_options) - 1:
                        self.selected_option = 0
                    else:
                        self.selected_option = (self.selected_option + 1)
                        # um wieder unten zu starten
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if self.selected_option <= 0:
                        self.selected_option = len(self.menu_options) - 1
                    else:
                        self.selected_option = (self.selected_option - 1)
                elif event.key == pygame.K_RETURN:
                    self._handleOptions(self.menu_options[self.selected_option])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for option in self.buttons:
                    if self.buttons[option][1].collidepoint(pygame.mouse.get_pos()):
                        self._handleOptions(option)

    def _handleOptions(self, option: str):
        match(option):
            case "Neuer Versuch":
                self._quit()
            case "Zum Menu":
                self._quit()
                self.backToMenu = True
            case "Beenden":
                self._quit()
                self._shouldClose = True
                    
    def _draw_grid(self, surface):
        for y in range(0, int(Settings.grid_height)):
            for x in range(0, int(Settings.grid_width)):
                r = pygame.Rect((x * Settings.grid_size, y * Settings.grid_size),
                                (Settings.grid_size, Settings.grid_size))
                color = (93, 216, 228) if (x + y) % 2 == 0 else (84, 194, 205)
                pygame.draw.rect(surface, color, r)  
                  
    def _build_info_box(self):
        self.back_info_box = pygame.Surface((520, 120)).convert()
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
        highscore_rect = highscore.get_rect(center=(520//2,  30))
        
        schwierigkeit = self.info_font.render(f"Schwierigkeit: {self.config.get_Difficulty().name}", False, text_color)
        schwierigkeit_rect = schwierigkeit.get_rect(center=(520//2, 90))
        
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
    
    def run(self):
        self._running = True
        
        while self._running:
            self._handleEvents()
            
            self._draw_grid(self._surface)
            
            self._update_screen()
            
    def _quit(self):
        self._running = False

    
    def windowShouldClose(self):
        return self._shouldClose
    
    def shouldGoToMenu(self):
        return self.backToMenu