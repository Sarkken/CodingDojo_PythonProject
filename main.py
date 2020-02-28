import pygame as pg
from settings import *
from sprites import *
from os import path

# Asset Folder Paths
image_folder = path.join(path.dirname(__file__), 'images')
audio_folder = path.join(path.dirname(__file__), 'sounds')


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init() # For audio
        pg.display.set_caption(TITLE)
        self.deltaY = 0
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.jump_sound = pg.mixer.Sound(path.join(audio_folder,'Jump10.wav'))
        self.hit_sound = pg.mixer.Sound(path.join(audio_folder, 'Hit.wav'))
        self.hit_sound.set_volume(100) #set volume?
        

    def new (self):
        # Starts a new game

        pg.mixer.music.load(path.join(audio_folder,"happytune.wav"))
        pg.mixer.music.play(loops=-1)

        self.all_sprites = pg.sprite.Group()
        self.out_of_bounds = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.moving_platforms_vertical = pg.sprite.Group()
        self.moving_platforms_horizontal = pg.sprite.Group()
        self.graph_platforms = pg.sprite.Group()
        self.player = Player(self)
        self.mobs = pg.sprite.Group()

        self.all_sprites.add(self.player)

        # Outer bounding to prevent player from leaving the playspace
        bound_left = Platform(-40, 0, 40, HEIGHT)
        bound_right = Platform(WIDTH, 0, 40, HEIGHT)
        bound_floor = Platform(-200, HEIGHT+20, WIDTH+400, 40)
        self.all_sprites.add(bound_left)
        self.platforms.add(bound_left)
        self.all_sprites.add(bound_right)
        self.platforms.add(bound_right)
        self.all_sprites.add(bound_floor)
        self.platforms.add(bound_floor)
        self.out_of_bounds.add(bound_floor)

        # Platforms that player can jump and run on
        p1 = Platform(0, 500, 160, 500, img="Plat1.png")
        p2_1 = Platform(160, 840, 80, 500)
        p2_2 = Platform(240, 760, 80, 500)
        p2_3 = Platform(320, 760, 80, 500)
        p2_4 = Platform(400, 760, 80, 500)
        p2_5 = Platform(480, 680, 80, 500)
        p2_1r = GraphPlatform(160, 840-80, 80, 80, "Up")
        p2_2r = GraphPlatform(240, 760-80, 80, 80, "Up")
        p2_3r = GraphPlatform(320, 760-80, 80, 80, "Down")
        p2_4r = GraphPlatform(400, 760-80, 80, 80, "Up")
        p2_5r = GraphPlatform(480, 680-80, 80, 80, "Up")
        p3 = Platform(560, 600, 320, 500, img="Plat3.png")
        p4_1 = Platform(880, 680, 80, 500)
        p4_2 = Platform(960, 760, 80, 500)
        p4_3 = Platform(1040, 760, 80, 500)
        p4_1r = GraphPlatform(880, 680-80, 80, 80, "Down")
        p4_2r = GraphPlatform(960, 760-80, 80, 80, "Down")
        p4_3r = GraphPlatform(1040, 760-80, 80, 80, "Up")
        p5 = MovingPlatformVertical(1200, 600, 80, 600)
        p6 = MovingPlatformVertical(1360, 500, 80, 600, i=-1)
        p7 = MovingPlatformVertical(1520, 400, 80, 600)
        p8 = MovingPlatformHorizontal(1200, 300, 160, 30, i=-1)
        p9 = MovingPlatformHorizontal(1520, 150, 160, 30, i=1)
        p10 = Platform(1550, 50, 50, 20, img="Plat_Victory.png")
        p11 = Platform(1108, 680, 15, 15, img="GraphArrow.png")
        self.all_sprites.add(p1)
        self.all_sprites.add(p2_1)
        self.all_sprites.add(p2_2)
        self.all_sprites.add(p2_3)
        self.all_sprites.add(p2_4)
        self.all_sprites.add(p2_5)
        self.all_sprites.add(p2_1r)
        self.all_sprites.add(p2_2r)
        self.all_sprites.add(p2_3r)
        self.all_sprites.add(p2_4r)
        self.all_sprites.add(p2_5r)
        self.all_sprites.add(p3)
        self.all_sprites.add(p4_1)
        self.all_sprites.add(p4_2)
        self.all_sprites.add(p4_3)
        self.all_sprites.add(p4_1r)
        self.all_sprites.add(p4_2r)
        self.all_sprites.add(p4_3r)
        self.all_sprites.add(p5)
        self.all_sprites.add(p6)
        self.all_sprites.add(p7)
        self.all_sprites.add(p8)
        self.all_sprites.add(p9)
        self.all_sprites.add(p10)
        self.all_sprites.add(p11)
        self.platforms.add(p1)
        self.platforms.add(p2_1)
        self.platforms.add(p2_2)
        self.platforms.add(p2_3)
        self.platforms.add(p2_4)
        self.platforms.add(p2_5)
        self.platforms.add(p3)
        self.platforms.add(p4_1)
        self.platforms.add(p4_2)
        self.platforms.add(p4_3)
        self.platforms.add(p5)
        self.platforms.add(p6)
        self.platforms.add(p7)
        self.platforms.add(p8)
        self.platforms.add(p9)
        self.platforms.add(p10)
        self.graph_platforms.add(p2_1r)
        self.graph_platforms.add(p2_2r)
        self.graph_platforms.add(p2_3r)
        self.graph_platforms.add(p2_4r)
        self.graph_platforms.add(p2_5r)
        self.graph_platforms.add(p4_1r)
        self.graph_platforms.add(p4_2r)
        self.graph_platforms.add(p4_3r)
        self.moving_platforms_vertical.add(p5)
        self.moving_platforms_vertical.add(p6)
        self.moving_platforms_vertical.add(p7)
        self.moving_platforms_horizontal.add(p8)
        self.moving_platforms_horizontal.add(p9)

        # Enemy(s) in the level
        e1 = Mob(560, 600, 320)
        self.all_sprites.add(e1)
        self.mobs.add(e1)
    

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
        

        # Gather platform and bounding collision data
        bounding_collisions = pg.sprite.spritecollide(self.player, self.out_of_bounds, False)
        platform_collisions = pg.sprite.spritecollide(self.player, self.platforms, False)
        ramp_collision = pg.sprite.spritecollide(self.player, self.graph_platforms, False, pg.sprite.collide_mask)

        # Check if player fell out of bounds
        if bounding_collisions:
            self.game_over()

        #mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            
            if self.player.health == 0:
                self.game_over()

            if hits:
                if self.player.position.x < hits[0].position.x:
                    self.player.position += vector(-MOB_KNOCKBACK, 0)
                    self.hit_sound.play()
                else:
                    self.player.position += vector(MOB_KNOCKBACK, 0)
                    self.hit_sound.play()


        # Checks collisions on player falling
        if self.player.velocity.y > 0:
            # Check to see if the player collided with a ramp
            if ramp_collision:
                self.player.velocity.y = 0
                relative_x = self.player.rect.x - ramp_collision[0].rect.x
                if ramp_collision[0].slope == "Up":
                    pos_height = relative_x  + 20 # could use self.player.rect.width # but it makes the player bounce
                if ramp_collision[0].slope == "Down":
                    pos_height = 80 - relative_x
                target_y_pos = ramp_collision[0].rect.y + 85 - pos_height
                #if self.player.rect.bottom > target_y_pos: # Also made the player bounce.
                self.player.position.y = target_y_pos

                self.player.is_airborn = False
                self.player.is_grounded = True
                self.player.has_doublejump = True
            # Check for non-ground platform collisions first.
            elif platform_collisions:
                if self.player.position.y <= (platform_collisions[0].rect.top + 20):
                    # Positions the player on the first platform they've collided with, and set them to be "grounded".
                    self.player.position.y = platform_collisions[0].rect.top
                    self.player.velocity.y = 0
                    self.player.is_airborn = False
                    self.player.is_grounded = True
                    self.player.has_doublejump = True
                    # Check if platform is moving horizontally
                    if platform_collisions[0] in self.moving_platforms_horizontal:
                        self.player.position.x += platform_collisions[0].drag
                # Check if running left into a wall
                elif self.player.rect.left < platform_collisions[0].rect.right and self.player.rect.left > platform_collisions[0].rect.left:
                    self.player.position.x = platform_collisions[0].rect.right + 20
                    self.player.position.y -= 7
                # Check if running right into a wall
                elif self.player.rect.right > platform_collisions[0].rect.left and self.player.rect.right < platform_collisions[0].rect.right:
                    self.player.position.x = platform_collisions[0].rect.left - 20 
                    self.player.position.y -= 7 
            # # Check for ground collision ater checking for platforms.
            # if ground_collisions:
            #     # Positions the player on the ground platform they've collided with, and set them to be "grounded".
            #     self.player.position.y = ground_collisions[0].rect.top
            #     self.player.velocity.y = 0
            #     self.player.is_airborn = False
            #     self.player.is_grounded = True
            #     self.player.has_doublejump = True
        # Check collisions on player running or jumping into wall
        elif self.player.velocity.y <= 0:
            if platform_collisions:
                # Can you stand on a ramp?
                if ramp_collision:
                    # self.player.position.y = ramp_collision[0].
                    self.player.velocity.y = 0
                    relative_x = self.player.rect.x - ramp_collision[0].rect.x
                    self.player.position.y = HEIGHT - relative_x
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


        if self.player.position.x >= 1550 and self.player.position.y <= 50:
            self.game_end() #or go to the next level
            



    def draw (self):
        # Draws all the updates
        self.screen.fill(WHITE)
        background = pg.image.load(path.join(image_folder, "Background_sm.gif")).convert()

        self.screen.blit(pg.transform.scale(background, (1600,900)), (0,0))
        ### Background currently causes a ton of lag, look into other methods.
        self.all_sprites.draw(self.screen)
        # for sprite in self.all_sprites:
        #     if isinstance(sprite, Player):
        #         sprite.draw_health()
        #HUD
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        pg.display.flip()
    

    def game_intro(self):
        pg.mixer.music.load(path.join(audio_folder, "happy_adveture.mp3"))
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
                pg.draw.rect(self.screen, DIM_GREEN,((WIDTH/2) - 500,575,400,100))


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
                pg.draw.rect(self.screen, DIM_RED,((WIDTH/2) + 100,575,400,100))


            smallText = pg.font.Font("freesansbold.ttf",60)
            TextSurf = smallText.render("EXIT!", True, WHITE)
            TextRect = TextSurf.get_rect()
            TextRect.center = ( ((WIDTH/2) + 100+(400/2)), (575+(100/2)) )
            self.screen.blit(TextSurf, TextRect)
            pg.display.update()
            self.clock.tick(FPS)

        pg.mixer.music.fadeout(500)

    def game_end(self):
        pg.mixer.music.load(path.join(audio_folder,"enchanted.mp3"))
        pg.mixer.music.play(loops=-1)

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
                    pg.draw.rect(self.screen, DIM_GREEN,((WIDTH/2) - 500,575,400,100))


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
                    pg.draw.rect(self.screen, DIM_RED,((WIDTH/2) + 100,575,400,100))


                smallText = pg.font.Font("freesansbold.ttf",60)
                TextSurf = smallText.render("EXIT!", True, WHITE)
                TextRect = TextSurf.get_rect()
                TextRect.center = ( ((WIDTH/2) + 100+(400/2)), (575+(100/2)) )
                self.screen.blit(TextSurf, TextRect)


            pg.display.update()
            self.clock.tick(FPS)
        pg.mixer.music.fadeout(500)

    def game_over(self):
        pg.mixer.music.load(path.join(audio_folder,"Death.mp3"))
        pg.mixer.music.play(loops=-1)
        intro = True
        while intro:
            for event in pg.event.get():
                # print(event)
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            bsod = pg.image.load(path.join(image_folder,"fake-bsod.gif")).convert()
            self.screen.blit(pg.transform.scale(bsod, (1600,900)), (0,0))
            # self.screen.fill(DEATH_RED)
            largeText = pg.font.Font('freesansbold.ttf',130)
            TextSurf = largeText.render("You Died!", True, WHITE)
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
                pg.draw.rect(self.screen, DIM_GREEN,((WIDTH/2) - 500,575,400,100))


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
                pg.draw.rect(self.screen, DIM_RED,((WIDTH/2) + 100,575,400,100))


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
    pg.draw.rect(surf, BLACK, outline_rect, 2)


game = Game()
game.game_intro()
while game.running:
    game.new()
    game.run()
    game.game_end()

pg.quit()