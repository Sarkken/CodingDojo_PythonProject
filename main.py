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
        self.player = Player()
        self.all_sprites.add(self.player)

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

    def update (self):
        # Process all the updates
        self.all_sprites.update()

    def draw (self):
        # Draws all the updates
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()
        

game = Game()

while game.running:
    game.new()
    game.run()
