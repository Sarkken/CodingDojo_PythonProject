#Sprite classes for the game.
import pygame as pg
from settings import *
from os import path
vector = pg.math.Vector2


# Asset Folder Paths
image_folder = path.join(path.dirname(__file__), 'images')

class Player (pg.sprite.Sprite): 
    # Player Character Sprite
    
    def __init__(self, game, spawn_x=40, spawn_y=500):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.stand_frame
        self.image.set_colorkey(MASK)
        self.rect = self.image.get_rect()
        #self.rect.midbottom = vector(WIDTH/2, HEIGHT) # Starting position
        self.position = vector(spawn_x, spawn_y)
        self.velocity = vector(0,0)
        self.acceleration = vector(0,0)
        self.is_grounded = False
        self.is_airborn = False
        self.has_doublejump = False
        self.mask = pg.mask.from_surface(self.image)
        self.health = PLAYER_HEALTH #Dan
        # self.vx = 0
        # self.vy = 0

    def load_images(self):
        self.stand_frame = pg.image.load(path.join(image_folder, "Ninja_Stand.png")).convert()
        self.stand_frame.set_colorkey(BLACK)


        self.walk_frames_r = [pg.image.load(path.join(image_folder,"Ninja_Walk_1.png")).convert(),
        pg.image.load(path.join(image_folder,"Ninja_Walk_2.png")).convert(),
        pg.image.load(path.join(image_folder,"Ninja_Walk_3.png")).convert(),
        pg.image.load(path.join(image_folder,"Ninja_Walk_2.png")).convert()]

        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(MASK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))

        
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
        self.animate()
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
        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0
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

    def animate(self):
        now = pg.time.get_ticks()
        if self.velocity.x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % 4
                bottom = self.rect.bottom
                if self.velocity.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.jumping and not self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                bottom = self.rect.bottom
                self.image = self.stand_frame
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom




class Mob(pg.sprite.Sprite):
    def __init__(self, spawn_x, spawn_y, distance):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(path.join(image_folder, "Enemy.png")).convert()
        self.image.set_colorkey(MASK)
        # self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.position = vector(spawn_x, spawn_y)
        self.distance = distance
        self.path = [spawn_x, (spawn_x+self.distance)]
        self.walkCount = 0
        self.move_tracker = 0    
        self.vel = 1
        
    def update(self):
        if self.vel > 0:
            if self.position.x < self.path[1] + self.vel:
                self.position.x += self.vel
            else:
                self.vel = self.vel * -1
                self.position.x += self.vel
                self.walkCount = 0
        else:
            if self.position.x > self.path[0] - self.vel:
                self.position.x += self.vel
            else:
                self.vel = self.vel * -1
                self.position.x += self.vel
                self.walkCount = 0
        self.rect.midbottom = self.position


class Platform(pg.sprite.Sprite): 
    # Main class for all static platforms. Currently only the ground platform uses this class, but 
    # the line-graph (the pointy ground) may also use this platform type if we can implement it. If 
    # we do we'll likely need to look at mask collision so the player can walk up the hills.
    
    def __init__ (self, x, y, w, h, img=None):
        pg.sprite.Sprite.__init__(self)
        if img == None:
            self.image = pg.Surface((w,h))
            self.image.fill(GRAPH_GREEN)
        else:    
            self.image = pg.image.load(path.join(image_folder, img)).convert()
            self.image.set_colorkey(MASK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class GraphPlatform(pg.sprite.Sprite):
    # Class for the Line Graph platforms, which will almost always be some kind of angle. Testing
    # for collision stuff.

    def __init__(self, x, y, w, h, slope):
        pg.sprite.Sprite.__init__(self)
        self.slope = slope
        if self.slope == "Down":
            self.image = pg.image.load(path.join(image_folder, "Slope_Down.png")).convert()
        if self.slope == "Up":
            self.image = pg.image.load(path.join(image_folder, "Slope_Up.png")).convert()
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
    
    def __init__ (self, x, y, w, h, v=PLATFORM_VELOCITY, d=PLATFORM_DISTANCE, i=1): 
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(path.join(image_folder, "Plat_vertical.png")).convert()
        # self.image.fill(GREEN)
        self.image.set_colorkey(MASK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.top_surface = vector(x, y)
        self.move_tracker = 0
        self.velocity = v
        self.distance = d
        self.initial_direction = i

    def update (self):
        # Moves platforms based on previously defined values
        if self.initial_direction > 0:
            if self.move_tracker < 0:
                self.top_surface.y += self.velocity
            elif 0 < self.move_tracker < self.distance:
                self.top_surface.y -= self.velocity
            elif self.move_tracker >= self.distance:
                self.move_tracker = self.distance * -1
        if self.initial_direction < 0:
            if self.move_tracker < 0:
                self.top_surface.y -= self.velocity
            elif 0 < self.move_tracker < self.distance:
                self.top_surface.y += self.velocity
            elif self.move_tracker >= self.distance:
                self.move_tracker = self.distance * -1
        self.move_tracker += 1
        self.rect.midtop = self.top_surface


class MovingPlatformHorizontal(pg.sprite.Sprite): 
    # Main class for all platforms that move horizontally (side to side). The graph "cell" elements 
    # will use this class. Sprites can have a custom velocity at which they move, and length path
    # which determines how far the platform moves. If no values are given for these, then the 
    # default values in the settings.py file are used.
    
    def __init__ (self, x, y, w, h, v=PLATFORM_VELOCITY, d=PLATFORM_DISTANCE, i=1):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(path.join(image_folder, "Plat_horizontal.png")).convert()
        # self.image.fill(GREEN)
        self.image.set_colorkey(MASK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.top_surface = vector(x, y)
        self.move_tracker = 0
        self.velocity = v
        self.distance = d
        self.initial_direction = i
        self.drag = 0

    def update (self):
        if self.initial_direction > 0:
            if self.move_tracker < 0:
                self.top_surface.x += self.velocity
                self.drag = self.velocity
            elif 0 < self.move_tracker < self.distance:
                self.top_surface.x -= self.velocity
                self.drag = self.velocity * -1
            elif self.move_tracker >= self.distance:
                self.move_tracker = self.distance * -1
        if self.initial_direction < 0:
            if self.move_tracker < 0:
                self.top_surface.x -= self.velocity
                self.drag = self.velocity * -1
            elif 0 < self.move_tracker < self.distance:
                self.top_surface.x += self.velocity
                self.drag = self.velocity
            elif self.move_tracker >= self.distance:
                self.move_tracker = self.distance * -1
        self.move_tracker += 1
        self.rect.midtop = self.top_surface
