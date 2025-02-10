from enum import Enum

from Food import Food
from FoodType import FoodType, random_food_type
from Snake import *

import pygame
import sys
import random


class SnakeGame:
    def __init__(self):
        pygame.init()

        self.__tick_speed = 5
        self.__is_paused = False
        self.__clock = pygame.time.Clock()
        self.__screen = pygame.display.set_mode((Settings.screen_width, Settings.screen_height), 0, 32)
        self.__surface = pygame.Surface(self.__screen.get_size())
        self.__surface = self.__surface.convert()

        self.__draw_grid(self.__surface)
        self.__number_of_devoured_foods = 0
        self.__snake = Snake()

        self.__foods = [Food(random_food_type()),Food(random_food_type()),Food(random_food_type())]


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
                elif event.key == pygame.K_ESCAPE:
                    self.__quit_game()
                elif event.key == pygame.K_q:
                    self.__is_paused = not self.__is_paused

    def __randomize_position_food(self):
        while True:
            pos =  (random.randint(0, int(Settings.grid_width)-1) * Settings.grid_size,
                               random.randint(0, int(Settings.grid_height) - 1) * Settings.grid_size)
            for get_position in self.__snake.get_positions():
                if get_position != pos:
                    return pos

    def __check_snake_food_collision(self):
        for food in self.__foods:
            if self.__snake.get_head_position() == food.get_position():
                self.__snake.increase_score(1)
                self.__tick_speed = self.__tick_speed + 1
                self.__number_of_devoured_foods += 1
                if food.get_food_type() == FoodType.DOUBLE_UP:
                    self.__snake.half_length()
                    self.__tick_speed = self.__tick_speed * 2
                if food.get_food_type() == FoodType.EXTRA_LIFE:
                    self.__snake.increase_length()
                if food.get_food_type() == FoodType.NORMAL:
                    self.__snake.increase_length()
                self.__foods.remove(food)
                self.__foods.append(Food(random_food_type()))
                food.set_position(self.__randomize_position_food())


    def __draw_objects(self):
        self.__snake.draw(self.__surface)
        for food in self.__foods:
            food.draw(self.__surface)


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
            if not self.__is_paused:
                self.__draw_grid(self.__surface)
                self.__snake.move()

                self.__check_snake_food_collision()

                self.__draw_objects()
                self.__update_screen()
