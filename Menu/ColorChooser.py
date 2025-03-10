import pygame
import sys

class ColorChooser:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.WIDTH, self.HEIGHT = width, height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pygame Color Chooser")

        self.font = pygame.font.Font(None, 36)
        self.color = [255, 255, 255]

    def draw_slider(self, x, y, value, label):
        pygame.draw.rect(self.screen, (200, 200, 200), (x, y, 256, 20))
        pygame.draw.rect(self.screen, (100, 100, 100), (x + value, y, 10, 20))
        text = self.font.render(f"{label}: {value}", True, (0, 0, 0))
        self.screen.blit(text, (x, y - 30))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    for i in range(3):
                        if 50 <= mx <= 306 and 100 + i * 100 <= my <= 120 + i * 100:
                            self.color[i] = mx - 50

            self.screen.fill(self.color)

            self.draw_slider(50, 100, self.color[0], "R")
            self.draw_slider(50, 200, self.color[1], "G")
            self.draw_slider(50, 300, self.color[2], "B")

            pygame.display.flip()

        pygame.quit()
        sys.exit()
