#Sprite classes for the game.
import pygame as pg
from settings import *
from os import path
vector = pg.math.Vector2


# Asset Folder Paths
image_folder = path.join(path.dirname(__file__), 'images')

class Player (pg.sprite.Sprite): 
    # Player Character Sprite
    
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(path.join(image_folder, "Ninja_Stand.png")).convert()
        self.image.set_colorkey(MASK)
        self.rect = self.image.get_rect()
        #self.rect.midbottom = vector(WIDTH/2, HEIGHT) # Starting position
        self.position = vector(WIDTH/2, HEIGHT-30)
        self.velocity = vector(0,0)
        self.acceleration = vector(0,0)
        self.is_grounded = False
        self.is_airborn = False
        self.has_doublejump = False
        self.mask = pg.mask.from_surface(self.image)
        self.health = PLAYER_HEALTH #Dan
        # self.vx = 0
        # self.vy = 0
        
    def jump(self):
        # Check if player is currently grounded.
        if not self.is_airborn:
                self.velocity.y = -15
                self.is_grounded = False
                self.is_airborn = True
                self.game.jump_sound.play()
        # If player isn't grounded, check if they have a double-jump available.
        elif self.is_airborn:
            if self.has_doublejump:
                self.velocity.y = -12
                self.has_doublejump = False
                self.game.jump_sound.play()

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

        # # Block from going outside bounds.
        # if self.position.x > WIDTH or self.position.x < 0:
        #     self.acceleration.x = 0
        #     self.velocity.x = 0
        ### Removed in favor of using collisions with out of map bounding boxes.

    # def draw_health(self):
        #     if self.health >= 75:
        #         col = GREEN
        #     elif self.health >= 50:
        #         col = YELLOW
        #     else:
        #         col = RED
        #     width = int(self.rect.width * self.health/100)
        #     self.health_bar = pg.Rect(0, 0, width, 7)
        #     pg.draw.rect(self.image, col, self.health_bar)

#  class Enemy (pg.sprite.Sprite):
#      pass


class Mob(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, end):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30,40))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.end = end
        self.path = [x, self.end]
        self.walkCount = 0
        self.move_tracker = 0    
        self.vel = 1
        
    def update(self):
        if self.vel > 0:
            if self.rect.x < self.path[1] + self.vel:
                self.rect.x += self.vel
            else:
                self.vel = self.vel * -1
                self.rect.x += self.vel
                self.walkCount = 0
        else:
            if self.rect.x > self.path[0] - self.vel:
                self.rect.x += self.vel
            else:
                self.vel = self.vel * -1
                self.rect.x += self.vel
                self.walkCount = 0


class Platform(pg.sprite.Sprite): 
    # Main class for all static platforms. Currently only the ground platform uses this class, but 
    # the line-graph (the pointy ground) may also use this platform type if we can implement it. If 
    # we do we'll likely need to look at mask collision so the player can walk up the hills.
    
    def __init__ (self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class GraphPlatform(pg.sprite.Sprite):
    # Class for the Line Graph platforms, which will almost always be some kind of angle. Testing
    # for collision stuff.

    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(path.join(image_folder, "mask_test.png")).convert()
        self.image.set_colorkey(MASK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pg.mask.from_surface(self.image)

class MovingPlatformVertical(pg.sprite.Sprite): 
    # Main class for all platforms that move vertically (up and down). The Bar graph elements will
    # use this class. Sprites can have a custom velocity at which they move, and length path which
    # determines how far the platform moves. If no values are given for these, then the default
    # values in the settings.py file are used.
    
    def __init__ (self, x, y, w, h, v=PLATFORM_VELOCITY, d=PLATFORM_DISTANCE): #initial direction needed?
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.top_surface = vector(x, y)
        self.move_tracker = 0
        self.velocity = v
        self.distance = d

    def update (self):
        #testing moving platforms
        if self.move_tracker < 0:
            self.top_surface.y += self.velocity
        elif 0 < self.move_tracker < self.distance:
            self.top_surface.y -= self.velocity
        elif self.move_tracker >= self.distance:
            self.move_tracker = self.distance * -1
        self.move_tracker += 1
        self.rect.midtop = self.top_surface


class MovingPlatformHorizontal(pg.sprite.Sprite): 
    # Main class for all platforms that move horizontally (side to side). The graph "cell" elements 
    # will use this class. Sprites can have a custom velocity at which they move, and length path
    # which determines how far the platform moves. If no values are given for these, then the 
    # default values in the settings.py file are used.
    
    def __init__ (self, x, y, w, h, v=PLATFORM_VELOCITY, d=PLATFORM_DISTANCE): # initial direction needed?
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.top_surface = vector(x, y)
        self.move_tracker = 0
        self.velocity = v
        self.distance = d

    def update (self):
        #testing moving platforms
        if self.move_tracker < 0:
            self.velocity = 1
        elif 0 < self.move_tracker < self.distance:
            self.velocity = -1
        elif self.move_tracker >= self.distance:
            self.move_tracker = self.distance * -1
        self.top_surface.x += self.velocity
        self.move_tracker += 1
        self.rect.midtop = self.top_surface
