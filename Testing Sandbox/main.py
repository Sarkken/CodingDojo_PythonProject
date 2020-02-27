import pygame as pg
from settings import *
from sprites import *
import time



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
        self.moving_platforms_vertical = pg.sprite.Group()
        self.moving_platforms_horizontal = pg.sprite.Group()
        self.ground = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        ground_plat = Platform(0, HEIGHT-20, WIDTH, 20)
        self.all_sprites.add(ground_plat)
        self.ground.add(ground_plat)
        wall_plat1 = Platform(-20, HEIGHT-250, 60, 250)
        self.all_sprites.add(wall_plat1)
        self.platforms.add(wall_plat1)
        wall_plat2 = Platform(WIDTH-40, HEIGHT-250, 60, 250)
        self.all_sprites.add(wall_plat2)
        self.platforms.add(wall_plat2)
        plat1 = Platform(int(WIDTH*.25), HEIGHT-60, 80, 20)
        self.all_sprites.add(plat1)
        self.platforms.add(plat1)
        plat2 = MovingPlatformVertical(int(WIDTH*.5), HEIGHT-120, 80, 20)
        self.all_sprites.add(plat2)
        self.platforms.add(plat2)
        self.moving_platforms_vertical.add(plat2)
        plat3 = MovingPlatformHorizontal(int(WIDTH*.75), HEIGHT-120, 80, 20)
        self.all_sprites.add(plat3)
        self.platforms.add(plat3)
        self.moving_platforms_horizontal.add(plat3)

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
        platform_collisions = pg.sprite.spritecollide(self.player, self.platforms, False)
        ground_collisions = pg.sprite.spritecollide(self.player, self.ground, False)
    
        # Checks collisions on player falling
        if self.player.velocity.y > 0:
            # Check for non-ground platform collisions first.
            if platform_collisions:
                # Check to see if the player cleared the platform
                if self.player.position.y <= (platform_collisions[0].rect.top + 15):
                    # Positions the player on the first platform they've collided with, and set them to be "grounded".
                    self.player.position.y = platform_collisions[0].rect.top
                    self.player.velocity.y = 0
                    self.player.is_airborn = False
                    self.player.is_grounded = True
                    self.player.has_doublejump = True
                    # Check if platform is moving horizontally
                    if platform_collisions[0] in self.moving_platforms_horizontal:
                        self.player.position.x += platform_collisions[0].velocity
                # Check if running left into a wall
                elif self.player.rect.left < platform_collisions[0].rect.right and self.player.rect.left > platform_collisions[0].rect.left:
                    self.player.position.x = platform_collisions[0].rect.right + 20
                    self.player.position.y -= 7
                # Check if running right into a wall
                elif self.player.rect.right > platform_collisions[0].rect.left and self.player.rect.right < platform_collisions[0].rect.right:
                    self.player.position.x = platform_collisions[0].rect.left - 20 
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
        elif self.player.velocity.y <= 0:
            if platform_collisions:
                # Check if jumping into underside of platform/object
                if self.player.rect.top <= platform_collisions[0].rect.bottom and self.player.rect.bottom > platform_collisions[0].rect.bottom:
                    self.player.position.y = platform_collisions[0].rect.bottom + PLAYER_HEIGHT
                    self.player.velocity.y = 0 
                # Check if jumping left into a wall
                elif self.player.rect.left < platform_collisions[0].rect.right and self.player.rect.left > platform_collisions[0].rect.left:
                    self.player.position.x = platform_collisions[0].rect.right + 20
                    self.player.velocity.x = 0
                    self.player.acceleration.x = 0
                # Check if jumping right into a wall
                elif self.player.rect.right > platform_collisions[0].rect.left and self.player.rect.right < platform_collisions[0].rect.right:
                    self.player.position.x = platform_collisions[0].rect.left - 20 
                    self.player.acceleration.x = 0


        ### Chrisna win-condition code
        if self.player.position.x >= 760 and self.player.position.y >= 150:
            self.WinScreen(BLUE)
            pg.display.update()
            time.sleep(2)
            self.game_end()

    def draw (self):
        # Draws all the updates
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()
        # Draws all the updates
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()
        
    def game_intro(self):
        intro = True

        while intro:
            for event in pg.event.get():
                # print(event)
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                    
            self.screen.fill(BLACK)
            largeText = pg.font.Font('freesansbold.ttf',115)
            TextSurf = largeText.render("Office Escape!", True, WHITE)
            TextRect = TextSurf.get_rect()
            TextRect.center = ((WIDTH/2),(HEIGHT/2))
            self.screen.blit(TextSurf, TextRect)

            mouse = pg.mouse.get_pos()
            click = pg.mouse.get_pressed()

            # print(mouse)

            if 150+200 > mouse[0] > 150 and 275+50 > mouse[1] > 275:
                pg.draw.rect(self.screen, BRIGHT_GREEN,(150,275,200,50))
                if click[0] == 1:
                    self.new()
                    self.run()
            else:
                pg.draw.rect(self.screen, GREEN,(150,275,200,50))


            smallText = pg.font.Font("freesansbold.ttf",30)
            TextSurf = smallText.render("START!", True, WHITE)
            TextRect = TextSurf.get_rect()
            TextRect.center = ( (150+(200/2)), (275+(50/2)) )
            self.screen.blit(TextSurf, TextRect)
            
            if 460+200 > mouse[0] > 460 and 275+50 > mouse[1] > 275:
                pg.draw.rect(self.screen, BRIGHT_RED,(460,275,200,50))
                if click[0] == 1:
                   pg.quit()              
            else:
                pg.draw.rect(self.screen, RED,(460,275,200,50))


            smallText = pg.font.Font("freesansbold.ttf",30)
            TextSurf = smallText.render("EXIT!", True, WHITE)
            TextRect = TextSurf.get_rect()
            TextRect.center = ( (460+(200/2)), (275+(50/2)) )
            self.screen.blit(TextSurf, TextRect)
            pg.display.update()
            self.clock.tick(FPS)

    def game_end(self):
        intro = True

        while intro:
            for event in pg.event.get():
                # print(event)
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                    
            self.screen.fill(WHITE)
            largeText = pg.font.Font('freesansbold.ttf',70)
            TextSurf = largeText.render("Thanks for Playing!", True, BLACK)
            TextRect = TextSurf.get_rect()
            self.deltaY -= 0.5
            TextRect.center = ((WIDTH/2),(HEIGHT/2) + self.deltaY)
            self.screen.blit(TextSurf, TextRect)


            largeText = pg.font.Font('freesansbold.ttf',50)
            TextSurf = largeText.render("Game created by:", True, BLACK)
            TextRect = TextSurf.get_rect()
            self.deltaY -= 0.5
            TextRect.center = ((WIDTH/2),((HEIGHT/2)+250) + self.deltaY)
            self.screen.blit(TextSurf, TextRect)


            largeText = pg.font.Font('freesansbold.ttf',30)
            TextSurf = largeText.render("Gary Sabo", True, BLACK)
            TextRect = TextSurf.get_rect()
            self.deltaY -= 0.5
            TextRect.center = ((WIDTH/2),((HEIGHT/2)+350) + self.deltaY)
            self.screen.blit(TextSurf, TextRect)


            largeText = pg.font.Font('freesansbold.ttf',30)
            TextSurf = largeText.render("Jimmy Pham", True, BLACK)
            TextRect = TextSurf.get_rect()
            self.deltaY -= 0.5
            TextRect.center = ((WIDTH/2),((HEIGHT/2)+450) + self.deltaY)
            self.screen.blit(TextSurf, TextRect)


            largeText = pg.font.Font('freesansbold.ttf',30)
            TextSurf = largeText.render("Randy Phan", True, BLACK)
            TextRect = TextSurf.get_rect()
            self.deltaY -= 0.5
            TextRect.center = ((WIDTH/2),((HEIGHT/2)+550) + self.deltaY)
            self.screen.blit(TextSurf, TextRect)


            largeText = pg.font.Font('freesansbold.ttf',30)
            TextSurf = largeText.render("Chrisna Ly", True, BLACK)
            TextRect = TextSurf.get_rect()
            self.deltaY -= 0.5
            TextRect.center = ((WIDTH/2),((HEIGHT/2)+650) + self.deltaY)
            self.screen.blit(TextSurf, TextRect)


            largeText = pg.font.Font('freesansbold.ttf',30)
            TextSurf = largeText.render("Daniel Lee", True, BLACK)
            TextRect = TextSurf.get_rect()
            self.deltaY -= 0.5
            TextRect.center = ((WIDTH/2),((HEIGHT/2)+750) + self.deltaY)
            self.screen.blit(TextSurf, TextRect)

            if self.deltaY < -1100:
                self.screen.fill(BLACK)

                largeText = pg.font.Font('freesansbold.ttf',115)
                TextSurf = largeText.render("Play Again?", True, WHITE)
                TextRect = TextSurf.get_rect()
                TextRect.center = ((WIDTH/2),(HEIGHT/2))
                self.screen.blit(TextSurf, TextRect)

                mouse = pg.mouse.get_pos()
                click = pg.mouse.get_pressed()

                # print(mouse)

                if 150+200 > mouse[0] > 150 and 275+50 > mouse[1] > 275:
                    pg.draw.rect(self.screen, BRIGHT_GREEN,(150,275,200,50))
                    if click[0] == 1:
                        self.new()
                        self.run()
                else:
                    pg.draw.rect(self.screen, GREEN,(150,275,200,50))


                smallText = pg.font.Font("freesansbold.ttf",30)
                TextSurf = smallText.render("START!", True, WHITE)
                TextRect = TextSurf.get_rect()
                TextRect.center = ( (150+(200/2)), (275+(50/2)) )
                self.screen.blit(TextSurf, TextRect)
                
                if 460+200 > mouse[0] > 460 and 275+50 > mouse[1] > 275:
                    pg.draw.rect(self.screen, BRIGHT_RED,(460,275,200,50))
                    if click[0] == 1:
                        pg.quit()       
                else:
                    pg.draw.rect(self.screen, RED,(460,275,200,50))


                smallText = pg.font.Font("freesansbold.ttf",30)
                TextSurf = smallText.render("EXIT!", True, WHITE)
                TextRect = TextSurf.get_rect()
                TextRect.center = ( (460+(200/2)), (275+(50/2)) )
                self.screen.blit(TextSurf, TextRect)



            pg.display.update()
            self.clock.tick(FPS)

                # Endgame screen
    def WinScreen(self, color):
        smallText = pg.font.Font("freesansbold.ttf",30)
        TextSurf = smallText.render("WINNER WINNER", True, WHITE)
        TextRect = TextSurf.get_rect()
        TextRect.center = ((WIDTH/2),(HEIGHT/2))
        self.screen.blit(TextSurf, TextRect)

        

game = Game()
game.game_intro()
while game.running:
    game.new()
    game.run()
    game.game_end()

pg.quit()