import pygame

from Utils import Settings
from Utils.colors import *

class GameOver:
    
    def __init__(self, screen):
        self._screen = screen
        self._surface = pygame.Surface(self._screen.get_size())
        self._shouldClose = False
        self.backToMenu = False
        self._running = True
        
        self.buttons = []
        
        pygame.font.init()
        
        self.font = pygame.font.SysFont("monospace", 50)
        
        self.menu_options = ["Nochmal versuchen", "Zum Menu", "Beenden"]
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
                for text, text_rect, option in self.buttons:
                    if text_rect.collidepoint(pygame.mouse.get_pos()):
                        self._handleOptions(option)

    def _handleOptions(self, option: str):
        match(option):
            case "Nochmal versuchen":
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
                color = (43, 166, 178) if (x + y) % 2 == 0 else (34, 144, 155)
                pygame.draw.rect(surface, color, r)
                
    def _update_screen(self):
        self._screen.blit(self._surface, (0, 0))
        
        for i, option in enumerate(self.menu_options):
            color = RGBA_BLACK if i == self.selected_option else RGBA_GREY
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(Settings.screen_width//2,  Settings.screen_height//3 + i * 80))
            self.buttons.append((text, text_rect, option))
        for text, text_rect, option in self.buttons:
            self._screen.blit(text,text_rect)

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