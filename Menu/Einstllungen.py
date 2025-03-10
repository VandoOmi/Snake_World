import pygame

from Utils import Config, Settings
from Utils.colors import RGBA_BLACK, RGBA_GREY


class Einstellungen:

    def __init__(self, screen):
        self._surface = pygame.Surface(screen.get_size())
        self._screen = screen
        self._shouldClose = False

        self.config = Config()

        self.buttons = {}

        pygame.font.init()

        self.font = pygame.font.SysFont("monospace", 50, True)

        self.menu_options = ["Schwer", "Mittel", "Leicht", "Zurück"]
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
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN:
                    self._handleOptions(self.menu_options[self.selected_option])

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for option in self.buttons:
                    if self.buttons[option][1].collidepoint(pygame.mouse.get_pos()):
                        self._handleOptions(option)

    def _handleOptions(self, option: str):
        match option.lower():
            case "schwer":
                self.config.set_Value("Difficulty", "SCHWER")
                self._quit()
            case "mittel":
                self.config.set_Value("Difficulty", "MITTEL")
                self._quit()
            case "leicht":
                self.config.set_Value("Difficulty", "LEICHT")
                self._quit()
                
            case "zurück":
                self._quit()



    def _draw_background(self, surface):
        for y in range(0, int(Settings.grid_height)):
            for x in range(0, int(Settings.grid_width)):
                r = pygame.Rect((x * Settings.grid_size, y * Settings.grid_size),
                                (Settings.grid_size, Settings.grid_size))
                color = (93, 216, 228) if (x + y) % 2 == 0 else (84, 194, 205)
                pygame.draw.rect(surface, color, r)

    def _update_screen(self):
        self._screen.blit(self._surface, (0, 0))

        menu_surf = pygame.Surface((520, 400)).convert()
        menu_surf.fill("white")
        menu_surf.set_alpha(80)
        menu_surf_rect = menu_surf.get_rect(
            center=(Settings.screen_width // 2, Settings.screen_height // 2))
        self._screen.blit(menu_surf, menu_surf_rect)

        for i, option in enumerate(self.menu_options):
            color = RGBA_BLACK if i == self.selected_option else RGBA_GREY
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(
                Settings.screen_width // 2, (Settings.screen_height - 400) // 2 + 100 + i * 100))
            self.buttons[option] = (text, text_rect)

        for text, rect in self.buttons.values():
            self._screen.blit(text, rect)

        pygame.display.update()

    def run(self):
        self._running = True

        while self._running:
            self._handleEvents()
            self._draw_background(self._surface)
            self._update_screen()

    def _quit(self):
        self._running = False
        self.config.close(True)

    def windowShouldClose(self) -> bool:
        return self._shouldClose
    
