import sys, pygame
import math, random

pygame.init()

W, H = 1200, 720

#display screen
win = pygame.display.set_mode((W, H))

pygame.display.set_caption("First Game")
bg = pygame.image.load('bg.jpeg')
clock = pygame.time.Clock()


class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.Jump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpcount = 10
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

class enemy(object):
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [x, self.end]
        self.walkCount = 0
        self.vel = 4
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self,win):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0
        
        if self.vel > 0:
            # win.blit([self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        
        else: 
            # win.blit([self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        self.hitbox = (self.x + 20, self.y + 11, 30, 52)
        pygame.draw.rect(win, (250,0,0), self.hitbox, 10)
        
    
    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0

class platform(object):
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [x, self.end]
        self.walkCount = 0
        self.vel = 4

    def draw(self,win):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0
        
        if self.vel > 0:
            # win.blit([self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        
        else: 
            # win.blit([self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        
    
    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        
# x = 50
# y = 530
# width = 40
# height = 60 
# vel = 10

# Jump = False
# jumpcount = 10
# left = False
# right = False
# walkCount = 0


def redrawGameWindow():
    #character and updating the movements
    win.blit(bg, (0,0))
    pygame.draw.rect(win, (255, 0, 0), (playOne.x, playOne.y, playOne.width, playOne.height))
    pygame.draw.rect(win, (0, 0, 0), (enemyOne.x, enemyOne.y, enemyOne.width, enemyOne.height))
    pygame.draw.rect(win, (200, 100, 100), (platformOne.x, platformOne.y, platformOne.width, platformOne.height))
    pygame.draw.rect(win, (200, 100, 100), (platformTwo.x, platformTwo.y, platformTwo.width, platformTwo.height))
    pygame.display.update()

#pressing keys
playOne = player(50, 530, 40, 60)
enemyOne = enemy(300, 530, 40, 60, 700)
platformOne = platform(700, 100, 80, 20, 900)
platformTwo = platform(500, 300, 80, 20, 800)
run=True
while run:
    redrawGameWindow()
    clock.tick(27)
    
    enemyOne.draw(win)
    platformOne.draw(win)
    platformTwo.draw(win)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and playOne.x > playOne.vel:
        playOne.x-=playOne.vel
        playOne.left = True
        playOne.right = False
        
    elif keys[pygame.K_RIGHT] and playOne.x < W - playOne.width - playOne.vel:
        playOne.x+=playOne.vel
        playOne.right = True
        playOne.left = False
    else:
        playOne.right = False
        playOne.left = False
        playOne.walkCount = 0
    
    if not (playOne.Jump):
        # if keys[pygame.K_UP] and y > vel:
        #     y-=vel

        # if keys[pygame.K_DOWN] and y < 500 - height - vel:
        #     y+=vel
    
        if keys[pygame.K_SPACE]:
            playOne.Jump = True
            playOne.right = False
            playOne.left = False
            playOne.walkCount = 0
    else:
        if playOne.jumpcount >= -10:
            neg = 1
            if playOne.jumpcount < 0:
                neg = -1
            playOne.y -= (playOne.jumpcount ** 2) * 0.5 * neg
            playOne.jumpcount -= 1
        else:
            playOne.Jump = False
            playOne.jumpcount = 10


pygame.quit()