import pygame as pg
from settings import *
from sprites import *



class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init() # For audio
        pg.display.set_caption(TITLE)
        
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        

    def new (self):
        # Starts a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.moving_platforms = pg.sprite.Group()
        self.ground = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        ground_plat = Platform(0, HEIGHT-20, WIDTH, 20)
        self.all_sprites.add(ground_plat)
        self.ground.add(ground_plat)
        wall_plat = Platform(-20, HEIGHT-150, 60, 150)
        self.all_sprites.add(wall_plat)
        self.platforms.add(wall_plat)
        plat1 = Platform(int(WIDTH*.75), HEIGHT-60, 80, 20)
        self.all_sprites.add(plat1)
        self.platforms.add(plat1)
        plat2 = MovingPlatformVertical(int(WIDTH*.5), HEIGHT-120, 80, 20)
        self.all_sprites.add(plat2)
        self.platforms.add(plat2)
        self.moving_platforms.add(plat2)

    def run (self):
        # Runs the game
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


    def events (self):
        # Gets all the events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def update (self):
        # Process all the updates
        self.all_sprites.update()
        

        # Gather collision data
        collisions = pg.sprite.spritecollide(self.player, self.platforms, False)
        ground_collisions = pg.sprite.spritecollide(self.player, self.ground, False)
    
        # Checks collisions on player falling
        if self.player.velocity.y > 0:
            # Check for non-ground platform collisions first.
            if collisions:
                # Check to see if the player cleared the platform
                if self.player.position.y <= (collisions[0].rect.top + 15):
                    # Positions the player on the first platform they've collided with, and set them to be "grounded".
                    self.player.position.y = collisions[0].rect.top
                    self.player.velocity.y = 0
                    self.player.is_airborn = False
                    self.player.is_grounded = True
                    self.player.has_doublejump = True
                # Check if running left into a wall
                elif self.player.rect.left < collisions[0].rect.right and self.player.rect.left > collisions[0].rect.left:
                    self.player.position.x = collisions[0].rect.right + 20
                    self.player.position.y -= 7
                # Check if running right into a wall
                elif self.player.rect.right > collisions[0].rect.left and self.player.rect.right < collisions[0].rect.right:
                    self.player.position.x = collisions[0].rect.left - 20 
                    self.player.position.y -= 7 
            # Check for ground collision ater checking for platforms.
            if ground_collisions:
                # Positions the player on the ground platform they've collided with, and set them to be "grounded".
                self.player.position.y = ground_collisions[0].rect.top
                self.player.velocity.y = 0
                self.player.is_airborn = False
                self.player.is_grounded = True
                self.player.has_doublejump = True
        # Check collisions on player running or jumping into wall
        ### This currently prevents players from jumping through a platform they are under (think Smash Bros.)
        elif self.player.velocity.x != 0 and self.player.velocity.y <= 0:
            if collisions:
                # Check if jumping into underside of platform/object
                if self.player.rect.top <= collisions[0].rect.bottom and self.player.rect.bottom > collisions[0].rect.bottom:
                    self.player.position.y = collisions[0].rect.bottom + PLAYER_HEIGHT
                    self.player.velocity.y = 0 
                # Check if jumping left into a wall
                elif self.player.rect.left < collisions[0].rect.right and self.player.rect.left > collisions[0].rect.left:
                    self.player.position.x = collisions[0].rect.right + 20
                    self.player.velocity.x = 0
                    self.player.acceleration.x = 0
                # Check if jumping right into a wall
                elif self.player.rect.right > collisions[0].rect.left and self.player.rect.right < collisions[0].rect.right:
                    self.player.position.x = collisions[0].rect.left - 20 
                    self.player.acceleration.x = 0




    def draw (self):
        # Draws all the updates
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()
        

game = Game()

while game.running:
    game.new()
    game.run()
