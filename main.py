import pygame as pg
from settings import *
from sprites import *
from os import path

# Asset Folder Paths
image_folder = path.join(path.dirname(__file__), 'images')



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
        self.mobs = pg.sprite.Group()
        self.moving_platforms_vertical = pg.sprite.Group()
        self.moving_platforms_horizontal = pg.sprite.Group()
        self.graph_platforms = pg.sprite.Group()
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
        plat1 = Platform(int(WIDTH*.3), HEIGHT-60, 80, 20)
        self.all_sprites.add(plat1)
        self.platforms.add(plat1)
        plat2 = MovingPlatformVertical(int(WIDTH*.6), HEIGHT-120, 80, 20)
        self.all_sprites.add(plat2)
        self.platforms.add(plat2)
        self.moving_platforms_vertical.add(plat2)
        plat3 = MovingPlatformHorizontal(int(WIDTH*.85), HEIGHT-120, 80, 20)
        self.all_sprites.add(plat3)
        self.platforms.add(plat3)
        self.moving_platforms_horizontal.add(plat3)
        graph_plat = GraphPlatform(100, HEIGHT-150, 150, 150)
        self.all_sprites.add(graph_plat)
        # self.platforms.add(graph_plat)
        self.graph_platforms.add(graph_plat)
        mob1 = Mob(int(WIDTH*.4), HEIGHT-60, 80, 20, 600)
        self.all_sprites.add(mob1)
        self.mobs.add(mob1)
      

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
        

        # Gather platform and ground collision data
        platform_collisions = pg.sprite.spritecollide(self.player, self.platforms, False)
        ground_collisions = pg.sprite.spritecollide(self.player, self.ground, False)
        ramp_collision = pg.sprite.spritecollide(self.player, self.graph_platforms, False, pg.sprite.collide_mask)


        #mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            
            if self.player.health == 0:
                self.player = False

            if hits:
                self.player.position += vector(MOB_KNOCKBACK, 0)

        # Checks collisions on player falling
        if self.player.velocity.y > 0:
            # Check to see if the player collided with a ramp
            if ramp_collision:
                self.player.velocity.y = 0
                relative_x = self.player.rect.x - ramp_collision[0].rect.x
                self.player.position.y = HEIGHT - (relative_x + 15)
                self.player.is_airborn = False
                self.player.is_grounded = True
                self.player.has_doublejump = True
            # Check for non-ground platform collisions first.
            elif platform_collisions:
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
        elif self.player.velocity.y <= 0:
            if platform_collisions:
                # Can you stand on a ramp?
                if ramp_collision:
                    # self.player.position.y = ramp_collision[0].
                    self.player.velocity.y = 0
                    relative_x = self.player.rect.x - ramp_collision[0].rect.x
                    self.player.position.y = HEIGHT - (relative_x + 15)
                    self.player.is_airborn = False
                    self.player.is_grounded = True
                    self.player.has_doublejump = True
                # Check if jumping into underside of platform/object
                elif self.player.rect.top <= platform_collisions[0].rect.bottom and self.player.rect.bottom > platform_collisions[0].rect.bottom:
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
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # for sprite in self.all_sprites:
        #     if isinstance(sprite, Player):
        #         sprite.draw_health()
        #HUD
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        pg.display.flip()
    

    def game_intro(self):
        pg.mixer.music.load("sounds\happy_adveture.mp3")
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

def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > .6:
        col= GREEN
    elif pct > .3:
        col= YELLOW
    else:
        col= RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


game = Game()
game.game_intro()
while game.running:
    game.new()
    game.run()
    game.game_end()

pg.quit()