import pygame


class Slider:
    # max_value 262 nicht 255 weil das irgendwie 7 weniger als den max wert nimmt beim verschieben
    # man ist frei das zu ändern (mit 262 siehts kacke aus und mit 255 gehts nicht richtig)
    def __init__(self, rect, initial_value, min_value=0, max_value=262, ):
        self.rect = rect
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value

        # schieberegler
        self.slider_rect = pygame.Rect(
            rect.x + self.value * (rect.width / (max_value - min_value)), rect.y, 10, rect.height)
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (0, 0, 255),
                         self.slider_rect)  # Schieberegler

    def update(self, mouse_pos, mouse_pressed):
        if self.dragging:
            x = mouse_pos[0]
            # Schieberegler kann nicht über die Grenzen hinausgehen
            if x < self.rect.x:
                x = self.rect.x
            elif x > self.rect.right - 10:
                x = self.rect.right - 10
            self.slider_rect.x = x
            # Wert des Schiebereglers berechnen
            self.value = int((self.slider_rect.x - self.rect.x) /
                             (self.rect.width / (self.max_value - self.min_value)))

        if mouse_pressed[0]:
            if self.slider_rect.collidepoint(mouse_pos):
                self.dragging = True
        else:
            self.dragging = False

    def value(self):
        return self.value

    # Positioniere den Schieberegler auf der Y-Achse
    def set_y_position(self, y):
        self.slider_rect.y = y
