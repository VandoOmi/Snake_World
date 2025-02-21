import sys

from .Difficulty import *
from .Fire import *
from .Food import Food
from .FoodType import FoodType, random_food_type
from .Snake import *


def random_position():
    return (random.randint(0, int(Settings.grid_width) - 1) * Settings.grid_size,
            random.randint(0, int(Settings.grid_height) - 1) * Settings.grid_size)


class SnakeGame:
    def __init__(self, difficulty, surface, screen):
        pygame.init()

        self.__screen = screen
        self.__surface = surface
        self.shouldClose = False

        self.running = True

        self.__tick_speed = 5
        self.__is_paused = False
        self.__clock = pygame.time.Clock()

        self.__draw_grid(surface)
        self.__number_of_devoured_foods = 0
        self.__snake = Snake()

        self.__foods = [Food(random_food_type(difficulty)), Food(
            random_food_type(difficulty)), Food(random_food_type(difficulty))]
        self.__fires = [Fire(random_position()), Fire(random_position())]

        self.__my_font = pygame.font.SysFont("monospace", 16)
        
        self.__difficulty =Schwierigkeit (difficulty)
        self.__snake.set_max_life(difficulty.max_life)

    def __draw_grid(self, surface):
        for y in range(0, int(Settings.grid_height)):
            for x in range(0, int(Settings.grid_width)):
                r = pygame.Rect((x * Settings.grid_size, y * Settings.grid_size),
                                (Settings.grid_size, Settings.grid_size))
                color = (93, 216, 228) if (x + y) % 2 == 0 else (84, 194, 205)
                pygame.draw.rect(surface, color, r)

    def __quit(self):
        self.running = False

    def __handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__quit()
                self.shouldClose = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__quit()
                    self.shouldClose = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.__snake.turn(Settings.up)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:    
                    self.__snake.turn(Settings.down)
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.__snake.turn(Settings.left)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.__snake.turn(Settings.right)
                if event.key == pygame.K_q:
                    self.__is_paused = not self.__is_paused
                    

    def __randomize_position_food(self):
        while True:
            pos = (random.randint(0, int(Settings.grid_width) - 1) * Settings.grid_size,
                   random.randint(0, int(Settings.grid_height) - 1) * Settings.grid_size)
            for get_position in self.__snake.get_positions():
                if get_position != pos:
                    return pos

    def __check_snake_food_collision(self):
        for food in self.__foods:
            if self.__snake.get_head_position() == food.get_position():
                self.__snake.increase_score(1)
                self.__tick_speed = self.__tick_speed + self.__difficulty.speed
                self.__number_of_devoured_foods += 1
                if food.get_food_type() == FoodType.DOUBLE_UP:
                    self.__snake.half_length()
                    self.__tick_speed = self.__tick_speed + self.__difficulty.speed*3
                if food.get_food_type() == FoodType.EXTRA_LIFE:
                    self.__snake.increase_life()
                    self.__snake.increase_length()
                    self.__tick_speed = self.__tick_speed + self.__difficulty.speed
                if food.get_food_type() == FoodType.NORMAL:
                    self.__snake.increase_length()
                self.__foods.remove(food)
                self.__foods.append(Food(random_food_type(self.__difficulty)))
                food.set_position(self.__randomize_position_food())

    def __check_snake_fire_collision(self):
        for fire in self.__fires:

            if self.__snake.get_head_position() == fire.get_position():
                print("snake position: ", self.__snake.get_head_position(), "           fire postion: ",
                      fire.get_position(), "                 ")

                self.__snake.reset()

    def __draw_objects(self):
        self.__snake.draw(self.__surface)
        for food in self.__foods:
            food.draw(self.__surface)
        for fire in self.__fires:
            fire.draw(self.__surface)

    def __update_screen(self):
        self.__screen.blit(self.__surface, (0, 0))
        text_score = self.__my_font.render("Score: {0}".format(
            self.__snake.get_score()), True, (0, 0, 0))
        text_extra_Life = self.__my_font.render(
            "Extra Leben: {0}".format(self.__snake.get_life()), True, (0, 0, 0))
        text_highscore = self.__my_font.render("Highscore: {0}".format(
            self.__snake.get_highscore()), True, (0, 0, 0))

        text_score_rect = text_score.get_rect(topleft=(10, 10))
        text_extra_life_rect = text_extra_Life.get_rect(
            topleft=(text_score_rect.right + 10, 10))
        text_highscore_rect = text_highscore.get_rect(
            topleft=(text_extra_life_rect.right + 10, 10))

        self.__screen.blit(text_score, text_score_rect)
        self.__screen.blit(text_extra_Life, text_extra_life_rect)
        self.__screen.blit(text_highscore, text_highscore_rect)

        pygame.display.update()

    def __check_tick_amount(self):
        if self.__tick_speed >= 50:
            self.__tick_speed = 50

    def __check_fire_spreed(self):

        match random.randint(0, 10):
            case 1 | 3 | 5 | 7 | 9:
                self.__fires.append(
                    Fire(self.__fires[random.randint(0, len(self.__fires) - 1)].get_random_nearby_position()))
            case 2 | 4 | 6 | 8 | 10:
                if len(self.__fires) > 1:
                    self.__fires.remove(
                        self.__fires[random.randint(0, len(self.__fires) - 1)])
            case 0:
                self.__fires.append(Fire(random_position()))

    def run(self):
        self.running = True

        while self.running:
            self.__check_tick_amount()
            self.__clock.tick(self.__tick_speed)
            self.__handle_keys()
            if not self.__is_paused:
                self.__draw_grid(self.__surface)
                self.__snake.move()

                self.__check_snake_fire_collision()
                self.__check_snake_food_collision()
                self.__check_fire_spreed()

                self.__draw_objects()
                self.__update_screen()

    def windowShouldClose(self):
        return self.shouldClose