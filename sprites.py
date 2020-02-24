#Sprite classes for the game.
import pygame as pg
from settings import *
vector = pg.math.Vector2


class Player (pg.sprite.Sprite): 
    # Player Character Sprite
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30,40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.midbottom = vector(WIDTH/2, HEIGHT) # Starting position
        # self.velocity = vector(0, 0)
        # self.accelleration = vector(0, 0)
        self.vx = 0
        self.vy = 0
        
    def update(self):
        self.vx = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vx = -5
        if keys[pg.K_RIGHT]:
            self.vx = 5

        self.rect.x += self.vx
        self.rect.y += self.vy


class Platform(pg.sprite.Sprite): 
    # Main class for all platforms. Will likely work best for the bar graph sprites, may need a 
    # subclass or separate class for "ground" that players can walk up, i.e. the line graph in the 
    # example image. 
    
    def __init__ (self):
#         pg.sprite.Sprite.__init__(self):
        pass