import random
import Game
from Game.FoodType import random_food_type #function
from Utils.Settings import *
from Utils.colors import *

from GameOver import *

map_width = 1600
map_height = 600

def random_position():
    return (random.randint(0, int(map_width / Settings.grid_size) - 1) * Settings.grid_size,
            random.randint(0, int(map_height / Settings.grid_size) - 1) * Settings.grid_size)


class SnakeGame:
    def __init__(self, difficulty, screen):   
        
        from Game import Map     
        self._screen = screen
        self.shouldClose = False
        
        self._surface = pygame.Surface((map_width, map_height)).convert()
        
        self._screen_offset = self._init_screen_offset()

        self._running = True
        self._tick_speed = 5
        self._is_paused = False
        self._clock = pygame.time.Clock()
        self.gameOverBool = False
        
        self._map = Map(self._surface)
        
        self._map.add_Obstacles([Game.Fire(random_position()), Game.Fire(random_position())])
        
        self._foods = [Game.Food(random_food_type(difficulty), random_position()), Game.Food(random_food_type(difficulty), random_position()), Game.Food(random_food_type(difficulty), random_position())]
        
        self._snake = Game.Snake()
        
        self._my_font = pygame.font.SysFont("monospace", 16)
        
        self._difficulty = Game.Schwierigkeit(difficulty)
        
        self._snake.set_max_life(self._difficulty.max_life)
        
    def _init_screen_offset(self):
        screen_x, screen_y = self._screen.get_size()
        x_offset = (screen_x-map_width)//2
        y_offset = (screen_y-map_height)//2
        return (x_offset, y_offset)
        
    def _control_tick_amount(self):
        if self._tick_speed >= 50:
            self._tick_speed = 50
    
    def _handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
                self.shouldClose = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._quit()
                    self.shouldClose = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self._snake.turn(Settings.up)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:    
                    self._snake.turn(Settings.down)
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self._snake.turn(Settings.left)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self._snake.turn(Settings.right)
                if event.key == pygame.K_q:
                    self._is_paused = not self._is_paused
                    
    def _randomize_position_food(self):
        while True:
            pos = random_position()
            for position in self._snake.get_positions():
                if position != pos:
                    return pos

    def _check_snake_food_collision(self):
        for food in self._foods:
            if self._snake.get_head_position() == food.get_position():
                self._snake.increase_score(1)
                self._tick_speed = self._tick_speed + self._difficulty.speed
                if food.get_food_type() == Game.FoodType.DOUBLE_UP:
                    self._snake.half_length()
                    self._tick_speed = self._tick_speed + self._difficulty.speed*3
                if food.get_food_type() == Game.FoodType.EXTRA_LIFE:
                    self._snake.increase_life()
                    self._snake.increase_length()
                    self._tick_speed = self._tick_speed + self._difficulty.speed
                if food.get_food_type() == Game.FoodType.NORMAL:
                    self._snake.increase_length()
                self._foods.remove(food)
                self._foods.append(Game.Food(random_food_type(self._difficulty), self._randomize_position_food()))

    def _check_snake_fire_collision(self):
        fires = self._map.get_Fires()
        
        if fires:
            for fire in fires:
                if self._snake.get_head_position() == fire.get_position():
                    self.gameOverBool = self._snake.reset()
                
    def _check_fire_spreed(self):

        match random.randint(0, 10):
            case 1 | 3 | 5 | 7 | 9:
                self._map.spread_fire(self._snake.get_positions())
            case 2 | 4 | 6 | 8 | 10:
                self._map.remove_random_Obstacle()
            case 0:
                self._map.add_Obstacle(Game.Fire(random_position()))
                
    def _check_conditions(self):
        self._check_snake_fire_collision()
        self._check_snake_food_collision()
        self._check_fire_spreed()

    def _draw_objects(self):
        self._snake.draw(self._surface)
        for food in self._foods:
            food.draw(self._surface)

    def _update_screen(self):
        self._screen.fill(RGBA_WHITE)
        self._screen.blit(self._surface, self._screen_offset)
        text_score = self._my_font.render("Score: {0}".format(
            self._snake.get_score()), True, (0, 0, 0))
        text_extra_Life = self._my_font.render(
            "Extra Leben: {0}".format(self._snake.get_life()), True, (0, 0, 0))
        text_highscore = self._my_font.render("Highscore: {0}".format(
            self._snake.get_highscore()), True, (0, 0, 0))
        if Settings.DEBUG_MODE:
            text_speed = self._my_font.render(f"Speed: {self._tick_speed}", True, (0, 0, 0))

        text_score_rect = text_score.get_rect(topleft=(10, 10))
        text_extra_life_rect = text_extra_Life.get_rect(
            topleft=(text_score_rect.right + 10, 10))
        text_highscore_rect = text_highscore.get_rect(
            topleft=(text_extra_life_rect.right + 10, 10))
        if Settings.DEBUG_MODE:
            text_speed_rect = text_speed.get_rect(
                topleft=(text_highscore_rect.right + 10, 10)
            )

        self._screen.blit(text_score, text_score_rect)
        self._screen.blit(text_extra_Life, text_extra_life_rect)
        self._screen.blit(text_highscore, text_highscore_rect)
        self._screen.blit(text_speed, text_speed_rect)

        pygame.display.flip()

    def run(self):
        self._running = True

        if Settings.DEBUG_MODE: print("GameLoop started.")
        while self._running:
            self._control_tick_amount()
            self._clock.tick(self._tick_speed)
            self._handle_keys()
            if not self._is_paused:
                self._map.draw()
                madeMove = self._snake.move()
                if madeMove or self.gameOverBool:
                    self.gameOverBool = False
                    self._tick_speed = 5
                    gameOver = GameOver(self._screen)
                    gameOver.run()
                    self.shouldClose = gameOver.windowShouldClose()
                    if gameOver.shouldGoToMenu():
                        self._quit()
                        self.gameOverBool = False
                    gameOver = None
                    if self.shouldClose:
                        self._quit()
                else:
                    self._check_conditions()

                    self._draw_objects()
                    self._update_screen()
                    

    def windowShouldClose(self):
        return self.shouldClose
    
    def _quit(self):
        self._running = False