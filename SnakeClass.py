from enum import Enum

import pygame
import sys
import random


class Snake:
    def __init__(self):
        self.__length = 1
        self.__positions = [((Settings.screen_width/2), (Settings.screen_height/2))]
        self.__direction = random.choice(Settings.directions)
        self.__color = (17, 24, 47)
        self.__score = 0

    def turn(self, new_direction):
        if (new_direction[0]*-1, new_direction[1]*-1) != self.__direction:  # cannot do a 180
            self.__direction = new_direction

    def move(self):
        head_pos = self.get_head_position()
        x, y = self.__direction
        new = (((head_pos[0] + (x * Settings.grid_size)) % Settings.screen_width),
               (head_pos[1] + (y * Settings.grid_size)) % Settings.screen_height)
        if len(self.__positions) > 2 and new in self.__positions[2:]:
            self.reset()
        else:
            self.__positions.insert(0, new)
            if len(self.__positions) > self.__length:
                self.__positions.pop()

    def get_positions(self):
        return self.__positions

    def get_head_position(self):
        return self.__positions[0]

    def reset(self):
        self.reset_length()
        self.__positions = [((Settings.screen_width/2), (Settings.screen_height/2))]
        self.__direction = random.choice(Settings.directions)
        self.__score = 0

    def increase_length(self):
        self.__length += 1

    def half_length(self):
        self.__length = (self.__length - self.__length // 10) / 2
        self.__positions.__len__()/2
        for i, __position in enumerate(self.__positions):
            if i > self.__length:
                self.__positions.pop(i)

                # Hallo Fabian

    def reset_length(self):
        self.__length = 1

    def increase_score(self, value):
        self.__score += value

    def get_score(self):
        return self.__score

    def reset_score(self):
        self.__score = 0

    def draw(self, surface):
        for pos in self.__positions:
            r = pygame.Rect((pos[0], pos[1]), (Settings.grid_size, Settings.grid_size))
            pygame.draw.rect(surface, self.__color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)


class FoodType(Enum):
    DOUBLE_UP = 1
    EXTRA_LIFE = 2
    NORMAL = 3

def random_food_type():
    if random.randint(1, 100) > 50:
        return FoodType.NORMAL
    if random.randint(1, 100) > 50:
        return FoodType.EXTRA_LIFE
    if random.randint(1, 100) > 50:
        return FoodType.DOUBLE_UP
    return FoodType.NORMAL

class Food:
    def __init__(self, food_type):
        self.__position = (0, 0)
        self.__food_type = food_type
        self.__randomize_position()

    def get_position(self):
        return self.__position

    def get_food_type(self):
        return self.__food_type

    def set_position(self, pos):
        self.__position = pos

    def __randomize_position(self):
        self.__position = (random.randint(0, int(Settings.grid_width)-1) * Settings.grid_size,
                           random.randint(0, int(Settings.grid_height) - 1) * Settings.grid_size)

    def draw(self, surface):
        r = pygame.Rect((self.__position[0], self.__position[1]), (Settings.grid_size, Settings.grid_size))
        pygame.draw.rect(surface, (255, 0, 0), r)
        if self.__food_type == FoodType.DOUBLE_UP:
            pygame.draw.rect(surface, (0, 0, 255), r)
        elif self.__food_type == FoodType.EXTRA_LIFE:
            pygame.draw.rect(surface, (0, 255, 0), r)
        else:
            pygame.draw.rect(surface, (255, 0, 0), r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)


class Settings:
    screen_width = 480
    screen_height = 480

    grid_size = 20
    grid_width = screen_width / grid_size
    grid_height = screen_height / grid_size

    up = (0, -1)
    down = (0, 1)
    left = (-1, 0)
    right = (1, 0)

    directions = [up, down, left, right]

class SnakeGame:
    def __init__(self):
        pygame.init()

        self.__tick_speed = 5;
        self.__clock = pygame.time.Clock()
        self.__screen = pygame.display.set_mode((Settings.screen_width, Settings.screen_height), 0, 32)
        self.__surface = pygame.Surface(self.__screen.get_size())
        self.__surface = self.__surface.convert()

        self.__draw_grid(self.__surface)
        self.__number_of_devoured_foods = 0
        self.__snake = Snake()

        self.__food = Food(random_food_type())


        self.__my_font = pygame.font.SysFont("monospace", 16)

    def __draw_grid(self, surface):
        for y in range(0, int(Settings.grid_height)):
            for x in range(0, int(Settings.grid_width)):
                r = pygame.Rect((x * Settings.grid_size, y * Settings.grid_size),
                                (Settings.grid_size, Settings.grid_size))
                color = (93, 216, 228) if (x+y) % 2 == 0 else (84, 194, 205)
                pygame.draw.rect(surface, color, r)

    def __quit_game(self):
        pygame.quit()
        sys.exit()

    def __handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.__snake.turn(Settings.up)
                elif event.key == pygame.K_DOWN:
                    self.__snake.turn(Settings.down)
                elif event.key == pygame.K_LEFT:
                    self.__snake.turn(Settings.left)
                elif event.key == pygame.K_RIGHT:
                    self.__snake.turn(Settings.right)

    def __randomize_position_food(self):
        while True:
            pos =  (random.randint(0, int(Settings.grid_width)-1) * Settings.grid_size,
                               random.randint(0, int(Settings.grid_height) - 1) * Settings.grid_size)
            for get_position in self.__snake.get_positions():
                if get_position != pos:
                    return pos

    def __check_snake_food_collision(self):
        if self.__snake.get_head_position() == self.__food.get_position():
            self.__snake.increase_score(1)
            self.__tick_speed = self.__tick_speed + 1
            self.__number_of_devoured_foods += 1
            if self.__food.get_food_type() == FoodType.DOUBLE_UP:
                self.__snake.half_length()
                self.__tick_speed = self.__tick_speed * 2
            if self.__food.get_food_type() == FoodType.EXTRA_LIFE:
                self.__snake.increase_length()
            if self.__food.get_food_type() == FoodType.NORMAL:
                self.__snake.increase_length()
            self.__food = Food(random_food_type())
            self.__food.set_position(self.__randomize_position_food())


    def __draw_objects(self):
        self.__snake.draw(self.__surface)
        self.__food.draw(self.__surface)


    def __update_screen(self):
        self.__screen.blit(self.__surface, (0, 0))
        text = self.__my_font.render("Score {0}".format(self.__snake.get_score()), True, (0, 0, 0))
        self.__screen.blit(text, (5, 10))
        pygame.display.update()

    def __check_tick_amount(self):
        if self.__tick_speed >= 50:
            self.__tick_speed =  50

    def main_loop(self):
        while True:
            self.__check_tick_amount()
            self.__clock.tick(self.__tick_speed)
            self.__handle_keys()
            self.__draw_grid(self.__surface)
            self.__snake.move()

            self.__check_snake_food_collision()

            self.__draw_objects()
            self.__update_screen()


game = SnakeGame()
game.main_loop()
