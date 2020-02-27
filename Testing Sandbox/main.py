import pygame as pg
from settings import *
from sprites import *



class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init() # For audio
        pg.display.set_caption(TITLE)
        self.deltaY = 0
        self.true_scroll = [0,0]
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.jump_sound = pg.mixer.Sound('test1\Jump10.wav')

    def new (self):
        # Starts a new game
        bg = pg.image.load("test1\sheet1.png").convert()
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.moving_platforms_vertical = pg.sprite.Group()
        self.moving_platforms_horizontal = pg.sprite.Group()
        self.ground = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        for plat in VERTICAL_FLATFORM_LIST:
            p = MovingPlatformVertical(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
            self.moving_platforms_vertical.add(p)

        for plat in HORIZONTAL_FLATFORM_LIST:
            p = MovingPlatformHorizontal(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
            self.moving_platforms_horizontal.add(p)

        
        pg.mixer.music.load("test1\happytune.wav")
        self.run()

    def run (self):
        # Runs the game
        pg.mixer.music.play(loops=-1)

        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

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

    def draw (self):
        # Draws all the updates
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def game_intro(self):
        pg.mixer.music.load("test1\happy_adveture.mp3")
        pg.mixer.music.play(loops=-1)

        intro = True

        while intro:
            for event in pg.event.get():
                # print(event)
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                    
            self.screen.fill(BLACK)
            largeText = pg.font.Font('freesansbold.ttf',130)
            TextSurf = largeText.render("Office Escape!", True, WHITE)
            TextRect = TextSurf.get_rect()
            TextRect.center = ((WIDTH/2),(HEIGHT/2))
            self.screen.blit(TextSurf, TextRect)

            mouse = pg.mouse.get_pos()
            click = pg.mouse.get_pressed()

            # print(mouse)

            if (WIDTH/2) - 500+400 > mouse[0] > (WIDTH/2) - 500 and 575+100 > mouse[1] > 575:
                pg.draw.rect(self.screen, GREEN,((WIDTH/2) - 500,575,400,100))
                if click[0] == 1:
                    self.new()
                    self.run()
            else:
                pg.draw.rect(self.screen, LIGHT_GREEN,((WIDTH/2) - 500,575,400,100))


            smallText = pg.font.Font("freesansbold.ttf",60)
            TextSurf = smallText.render("START!", True, WHITE)
            TextRect = TextSurf.get_rect()
            TextRect.center = ( ((WIDTH/2) - 500+(400/2)), (575+(100/2)) )
            self.screen.blit(TextSurf, TextRect)
            
            if (WIDTH/2) + 100+400 > mouse[0] > (WIDTH/2) + 100 and 575+100 > mouse[1] > 575:
                pg.draw.rect(self.screen, RED,((WIDTH/2) + 100,575,400,100))
                if click[0] == 1:
                   pg.quit()              
            else:
                pg.draw.rect(self.screen, LIGHT_RED,((WIDTH/2) + 100,575,400,100))


            smallText = pg.font.Font("freesansbold.ttf",60)
            TextSurf = smallText.render("EXIT!", True, WHITE)
            TextRect = TextSurf.get_rect()
            TextRect.center = ( ((WIDTH/2) + 100+(400/2)), (575+(100/2)) )
            self.screen.blit(TextSurf, TextRect)
            pg.display.update()
            self.clock.tick(FPS)

        pg.mixer.music.fadeout(500)

    def game_end(self):


        intro = True

        while intro:
            for event in pg.event.get():
                # print(event)
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                    
            self.screen.fill(WHITE)
            largeText = pg.font.Font('freesansbold.ttf',100)
            TextSurf = largeText.render("Thanks for Playing!", True, BLACK)
            TextRect = TextSurf.get_rect()
            self.deltaY -= 0.5
            TextRect.center = ((WIDTH/2),(HEIGHT/2) + self.deltaY)
            self.screen.blit(TextSurf, TextRect)


            largeText = pg.font.Font('freesansbold.ttf',80)
            TextSurf = largeText.render("Game created by:", True, BLACK)
            TextRect = TextSurf.get_rect()
            self.deltaY -= 0.5
            TextRect.center = ((WIDTH/2),((HEIGHT/2)+250) + self.deltaY)
            self.screen.blit(TextSurf, TextRect)


            largeText = pg.font.Font('freesansbold.ttf',50)
            TextSurf = largeText.render("Gary Sabo", True, BLACK)
            TextRect = TextSurf.get_rect()
            self.deltaY -= 0.5
            TextRect.center = ((WIDTH/2),((HEIGHT/2)+350) + self.deltaY)
            self.screen.blit(TextSurf, TextRect)


            largeText = pg.font.Font('freesansbold.ttf',50)
            TextSurf = largeText.render("Jimmy Pham", True, BLACK)
            TextRect = TextSurf.get_rect()
            self.deltaY -= 0.5
            TextRect.center = ((WIDTH/2),((HEIGHT/2)+450) + self.deltaY)
            self.screen.blit(TextSurf, TextRect)


            largeText = pg.font.Font('freesansbold.ttf',50)
            TextSurf = largeText.render("Randy Phan", True, BLACK)
            TextRect = TextSurf.get_rect()
            self.deltaY -= 0.5
            TextRect.center = ((WIDTH/2),((HEIGHT/2)+550) + self.deltaY)
            self.screen.blit(TextSurf, TextRect)


            largeText = pg.font.Font('freesansbold.ttf',50)
            TextSurf = largeText.render("Chrisna Ly", True, BLACK)
            TextRect = TextSurf.get_rect()
            self.deltaY -= 0.5
            TextRect.center = ((WIDTH/2),((HEIGHT/2)+650) + self.deltaY)
            self.screen.blit(TextSurf, TextRect)


            largeText = pg.font.Font('freesansbold.ttf',50)
            TextSurf = largeText.render("Daniel Lee", True, BLACK)
            TextRect = TextSurf.get_rect()
            self.deltaY -= 0.5
            TextRect.center = ((WIDTH/2),((HEIGHT/2)+750) + self.deltaY)
            self.screen.blit(TextSurf, TextRect)

            if self.deltaY < -1300:
                self.screen.fill(BLACK)

                largeText = pg.font.Font('freesansbold.ttf',115)
                TextSurf = largeText.render("Play Again?", True, WHITE)
                TextRect = TextSurf.get_rect()
                TextRect.center = ((WIDTH/2),(HEIGHT/2))
                self.screen.blit(TextSurf, TextRect)

                mouse = pg.mouse.get_pos()
                click = pg.mouse.get_pressed()

                if (WIDTH/2) - 500+400 > mouse[0] > (WIDTH/2) - 500 and 575+100 > mouse[1] > 575:
                    pg.draw.rect(self.screen, GREEN,((WIDTH/2) - 500,575,400,100))
                    if click[0] == 1:
                        self.new()
                        self.run()
                else:
                    pg.draw.rect(self.screen, LIGHT_GREEN,((WIDTH/2) - 500,575,400,100))


                smallText = pg.font.Font("freesansbold.ttf",60)
                TextSurf = smallText.render("START!", True, WHITE)
                TextRect = TextSurf.get_rect()
                TextRect.center = ( ((WIDTH/2) - 500+(400/2)), (575+(100/2)) )
                self.screen.blit(TextSurf, TextRect)
                
                if (WIDTH/2) + 100+400 > mouse[0] > (WIDTH/2) + 100 and 575+100 > mouse[1] > 575:
                    pg.draw.rect(self.screen, RED,((WIDTH/2) + 100,575,400,100))
                    if click[0] == 1:
                        pg.quit()              
                else:
                    pg.draw.rect(self.screen, LIGHT_RED,((WIDTH/2) + 100,575,400,100))


                smallText = pg.font.Font("freesansbold.ttf",60)
                TextSurf = smallText.render("EXIT!", True, WHITE)
                TextRect = TextSurf.get_rect()
                TextRect.center = ( ((WIDTH/2) + 100+(400/2)), (575+(100/2)) )
                self.screen.blit(TextSurf, TextRect)


            pg.display.update()
            self.clock.tick(FPS)

    def game_over(self):
        pg.mixer.music.load("test1\Death.mp3")
        pg.mixer.music.play(loops=-1)
        intro = True
        while intro:
            for event in pg.event.get():
                # print(event)
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                    
            self.screen.fill(DEATH_RED)
            largeText = pg.font.Font('freesansbold.ttf',130)
            TextSurf = largeText.render("You Died!", True, BLACK)
            TextRect = TextSurf.get_rect()
            TextRect.center = ((WIDTH/2),(HEIGHT/2)- 200)
            self.screen.blit(TextSurf, TextRect)

            largeText = pg.font.Font('freesansbold.ttf',130)
            TextSurf = largeText.render("Try Again?", True, WHITE)
            TextRect = TextSurf.get_rect()
            TextRect.center = ((WIDTH/2),(HEIGHT/2))
            self.screen.blit(TextSurf, TextRect)

            mouse = pg.mouse.get_pos()
            click = pg.mouse.get_pressed()

            # print(mouse)

            if (WIDTH/2) - 500+400 > mouse[0] > (WIDTH/2) - 500 and 575+100 > mouse[1] > 575:
                pg.draw.rect(self.screen, GREEN,((WIDTH/2) - 500,575,400,100))
                if click[0] == 1:
                    self.new()
                    self.run()
            else:
                pg.draw.rect(self.screen, LIGHT_GREEN,((WIDTH/2) - 500,575,400,100))


            smallText = pg.font.Font("freesansbold.ttf",60)
            TextSurf = smallText.render("YES", True, WHITE)
            TextRect = TextSurf.get_rect()
            TextRect.center = ( ((WIDTH/2) - 500+(400/2)), (575+(100/2)) )
            self.screen.blit(TextSurf, TextRect)
            
            if (WIDTH/2) + 100+400 > mouse[0] > (WIDTH/2) + 100 and 575+100 > mouse[1] > 575:
                pg.draw.rect(self.screen, RED,((WIDTH/2) + 100,575,400,100))
                if click[0] == 1:
                    pg.quit()              
            else:
                pg.draw.rect(self.screen, LIGHT_RED,((WIDTH/2) + 100,575,400,100))


            smallText = pg.font.Font("freesansbold.ttf",60)
            TextSurf = smallText.render("NO", True, WHITE)
            TextRect = TextSurf.get_rect()
            TextRect.center = ( ((WIDTH/2) + 100+(400/2)), (575+(100/2)) )
            self.screen.blit(TextSurf, TextRect)
            pg.display.update()
            self.clock.tick(FPS)

        pg.mixer.music.fadeout(500)


game = Game()
# game.game_intro()
while game.running:
    game.new()
    # game.game_end()
    # game.game_over()

pg.quit()