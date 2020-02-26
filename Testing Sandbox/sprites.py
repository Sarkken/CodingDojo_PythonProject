#Sprite classes for the game.
import pygame as pg
from settings import *
vector = pg.math.Vector2


class Player (pg.sprite.Sprite): 
    # Player Character Sprite
    
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((PLAYER_WIDTH,PLAYER_HEIGHT))
        self.image.fill(RED)
        self.game = game
        self.rect = self.image.get_rect()
        #self.rect.midbottom = vector(WIDTH/2, HEIGHT) # Starting position
        self.position = vector(WIDTH/2, HEIGHT-30)
        self.velocity = vector(0,0)
        self.acceleration = vector(0,0)
        self.is_grounded = False
        self.is_airborn = False
        self.has_doublejump = False
        
        # self.vx = 0
        # self.vy = 0
        
    def jump(self):
        # Check if player is currently grounded.
        if not self.is_airborn:
                self.velocity.y = -15
                self.is_grounded = False
                self.is_airborn = True
        # If player isn't grounded, check if they have a double-jump available.
        elif self.is_airborn:
            if self.has_doublejump:
                self.velocity.y = -12
                self.has_doublejump = False

    def update(self):
        self.acceleration = vector(0,PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        calc_move = vector(0,0)
        if keys[pg.K_LEFT]:
                self.acceleration.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
                self.acceleration.x = PLAYER_ACC

        # Movement calculations
        self.acceleration.x += self.velocity.x * PLAYER_FRICTION
        self.velocity += self.acceleration
        calc_move = self.velocity + 0.5 * self.acceleration
        # Prevent moving too fast from gravity
        if (self.velocity.y + 0.5 * self.acceleration.y) > PLAYER_TERMINAL_VELOCITY:
            calc_move.y = PLAYER_TERMINAL_VELOCITY
        
        self.position += calc_move
        self.rect.midbottom = self.position

        # Block from going outside bounds.
        if self.position.x > WIDTH or self.position.x < 0:
            self.acceleration.x = 0
            self.velocity.x = 0

    


class Platform(pg.sprite.Sprite): 
    # Main class for all platforms. Will likely work best for the bar graph sprites, may need a 
    # subclass or separate class for "ground" that players can walk up, i.e. the line graph in the 
    # example image. 
    
    def __init__ (self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_tracker = 0

class MovingPlatformVertical(pg.sprite.Sprite): 
    # Main class for all platforms. Will likely work best for the bar graph sprites, may need a 
    # subclass or separate class for "ground" that players can walk up, i.e. the line graph in the 
    # example image. 
    
    def __init__ (self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.top_surface = vector(x, y)
        self.move_tracker = 0
        self.velocity = 1

    def update (self):
        #testing moving platforms
        if self.move_tracker < 0:
            self.top_surface.y += self.velocity
        elif 0 < self.move_tracker < 60:
            self.top_surface.y -= self.velocity
        elif self.move_tracker >= 60:
            self.move_tracker = -60
        self.move_tracker += 1
        self.rect.midtop = self.top_surface

class MovingPlatformHorizontal(pg.sprite.Sprite): 
    # Main class for all platforms. Will likely work best for the bar graph sprites, may need a 
    # subclass or separate class for "ground" that players can walk up, i.e. the line graph in the 
    # example image. 
    
    def __init__ (self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.top_surface = vector(x, y)
        self.move_tracker = 0
        self.velocity = 1

    def update (self):
        #testing moving platforms
        if self.move_tracker < 0:
            self.velocity = 1
        elif 0 < self.move_tracker < 60:
            self.velocity = -1
        elif self.move_tracker >= 60:
            self.move_tracker = -60
        self.top_surface.x += self.velocity
        self.move_tracker += 1
        self.rect.midtop = self.top_surface