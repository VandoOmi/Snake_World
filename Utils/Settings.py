class Settings:
    screen_width = 1960
    screen_height = 1080

    grid_size = 20
    grid_width = screen_width / grid_size
    grid_height = screen_height / grid_size
    
    DEBUG_MODE = True

    up = (0, -1)
    down = (0, 1)
    left = (-1, 0)
    right = (1, 0)

    directions = [up, down, left, right]
