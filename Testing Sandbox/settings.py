# Game Settings and Attributes
TITLE = "Office Escape"
WIDTH = 1600
HEIGHT = 900
FPS = 60

# Player Properties Relating to Movement
PLAYER_HEIGHT = 40
PLAYER_WIDTH = 30
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.98
PLAYER_TERMINAL_VELOCITY = 15

# Platform Properties Relating to Movement (and possibly other stuff?)
PLATFORM_VELOCITY = 1
PLATFORM_DISTANCE = 75

PLATFORM_LIST = [(30, HEIGHT-80, 80, 20),
                 (0, HEIGHT-20, WIDTH * 2, 20),
                 (int(WIDTH*.5), HEIGHT-130, 20, 200), 
                 (1550, 75, 50, 20)]
                

VERTICAL_FLATFORM_LIST = [(int(WIDTH*.5), HEIGHT-130, 80, 20),
    (int(WIDTH*.5) + 200, HEIGHT-230, 80, 20),]

HORIZONTAL_FLATFORM_LIST = [(int(WIDTH*.75), HEIGHT-120, 80, 20)]



# Predefined Colors for Quick Reference
WHITE = (255,255,255)
GRAY = (128,128,128)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
DEATH_RED = (208,35,40)
LIGHT_RED = (200,0,0)
LIGHT_GREEN = (0,200,0)
MASK = (255,128,255)

