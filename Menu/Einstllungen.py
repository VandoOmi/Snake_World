import pygame

from Utils import Config, Settings
from Utils.colors import RGBA_BLACK, RGBA_GREY


class Einstellungen:

    def __init__(self, screen):
        self._surface = pygame.Surface(screen.get_size())
        self._screen = screen
        self._shouldClose = False

        self.config = Config()
        self._init_map()
        self.buttons = {}

        self.menu_font = pygame.font.SysFont("monospace", 50, True)
        self.info_font = pygame.font.SysFont("monospace", 30, True)

        self.menu_options = ["Schwer", "Mittel", "Leicht", "Zurück"]
        self.selected_option = 0
        

    def _init_map(self):
        from Game import Map
        self.snake_color = self.config.get_Value("color")
        self.primary_map_color = (
            255 - self.snake_color[0],
            255 - self.snake_color[1],
            255 - self.snake_color[2]
        )
        self.secoundary_map_color = (
            self.primary_map_color[0] - 20 if self.primary_map_color[0] -
            20 >= 0 else self.primary_map_color[0] + 20,
            self.primary_map_color[0] - 20 if self.primary_map_color[0] -
            20 >= 0 else self.primary_map_color[0] + 20,
            self.primary_map_color[0] - 20 if self.primary_map_color[0] -
            20 >= 0 else self.primary_map_color[0] + 20
        )

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
                    self.selected_option = (
                        (self.selected_option + 1) % len(self.menu_options))
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.selected_option = (
                        (self.selected_option - 1) % len(self.menu_options))
                elif event.key == pygame.K_RETURN:
                    self._handleOptions(
                        self.menu_options[self.selected_option])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for option in self.buttons:
                    if self.buttons[option][1].collidepoint(pygame.mouse.get_pos()):
                        self._handleOptions(option)

    def _handleOptions(self, option: str):
        match option:
            case "Schwer":
                self.config.set_Value("Difficulty", "SCHWER")
                self._quit()
            case "Mittel":
                self.config.set_Value("Difficulty", "MITTEL")
                self._quit()
            case "Leicht":
                self.config.set_Value("Difficulty", "LEICHT")
                self._quit()
            case "Zurück":
                self._quit()

    def _draw_background(self, surface):
        for y in range(0, int(Settings.grid_height)):
            for x in range(0, int(Settings.grid_width)):
                r = pygame.Rect((x * Settings.grid_size, y * Settings.grid_size),
                                (Settings.grid_size, Settings.grid_size))
                color = self.primary_map_color if (
                    x + y) % 2 == 0 else self.secoundary_map_color
                pygame.draw.rect(surface, color, r)

    def _build_info_box(self):
        self.config.update()
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

        schwierigkeit = self.info_font.render(
            f"Schwierigkeit: {self.config.get_Difficulty().name}", False, text_color)
        schwierigkeit_rect = schwierigkeit.get_rect(center=(520//2, 90))

        self.info_box.blit(schwierigkeit, schwierigkeit_rect)

    def _update_screen(self):
        self._screen.blit(self._surface, (0, 0))

        back_menu_surf = pygame.Surface(
            (520, 100 + (100*len(self.menu_options)))).convert()
        back_menu_surf.fill("white")
        back_menu_surf.set_alpha(100)
        self.menu_surf_rect = back_menu_surf.get_rect(
            center=(Settings.screen_width//2, Settings.screen_height//2))
        self._build_info_box()

        self._screen.blit(back_menu_surf, self.menu_surf_rect)
        self._screen.blit(self.back_info_box, self.info_bex_rect)

        menu_surf = pygame.Surface(
            (520, 100 + (100*len(self.menu_options)))).convert()
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
            self._draw_background(self._surface)
            self._update_screen()

    def _quit(self):
        self._running = False
        self.config.close()

    def windowShouldClose(self) -> bool:
        return self._shouldClose
