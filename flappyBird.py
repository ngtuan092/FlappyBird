import pygame
from pygame.locals import *
import sys
import random
WIN_HEIGHT = 600
WIN_WIDTH = 400


# get background image
BG = pygame.image.load('img/background.png')

# get bird's image
BIRD_IMG = pygame.image.load('img/bird.png')

# get column's image
COL_IMG = pygame.image.load('img/column.png')


FPS = 60 # frame per second
fpsClock = pygame.time.Clock()

# create a surface object which we draw on window
DISPLAYSURF = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(pygame.image.load('img/flyingDuck.jpg'))
pygame.init()

class Bird:
    BIRDWIDTH = 60
    BIRDHEIGHT = 45
    G = 0.5
    SPEEDFLY = -8
    IMG = BIRD_IMG

    def __init__(self):
        self.w = Bird.BIRDWIDTH
        self.h = Bird.BIRDHEIGHT
        # initial position
        self.y = (WIN_HEIGHT - Bird.BIRDHEIGHT) / 2
        self.x = (WIN_WIDTH - Bird.BIRDWIDTH) / 2
        self.speed = 0
        self.surface = Bird.IMG

    def draw(self):
        DISPLAYSURF.blit(self.surface, (int(self.x), int(self.y)))

    def fall(self):
        self.y += self.speed + 0.5 * Bird.G
        self.speed += Bird.G

    def jump(self):
        self.speed = Bird.SPEEDFLY

class Score:
    POS_X = 50
    POS_Y = 16
    def __init__(self):
        self.val = 0
    
    def inc(self):
        self.val += 1

    def Frame(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(str(self.val),True, (0, 0, 0))
        text.get_rect().center = (Score.POS_X, Score.POS_Y)
        return text, text.get_rect()
    
def main():
    '''the game's main loop'''
    bird = Bird()
    col = Columns()
    GameOver = False
    ScoreBoard = Score()
    DISC = 0
    while True:
        Jump = False
        for event in pygame.event.get():
            # listen for even here
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == MOUSEBUTTONDOWN and GameOver is False:
                Jump = True
            if GameOver is True and event.type == MOUSEBUTTONDOWN:
                bird = Bird()
                col = Columns()
                GameOver = False
                ScoreBoard.val = 0
                DISC = 0
        
        DISPLAYSURF.blit(BG, (0, 0))
        bird.draw()
        col.draw()
        DISPLAYSURF.blit(*ScoreBoard.Frame())
        
        if not GameOver:
            
            col.move()
            
            bird.fall()
            GameOver = isGameOver(bird, col)
            
            if Jump:
                bird.jump()
            DISC += Columns.SPEED
            if DISC > Columns.DISTANCE + Columns.WIDTH:
                ScoreBoard.inc()
                DISC = 0
            
            
            
            pygame.display.update()
        fpsClock.tick(FPS)
        



class Columns:
    ''' obstacle's init and moving rule'''
    WIDTH = 60
    HEIGHT = 500
    BLANK = 200
    DISTANCE = 200
    SPEED = 2
    IMG = COL_IMG
    def __init__(self):
        self.width = Columns.WIDTH
        self.height = Columns.HEIGHT
        self.blank = Columns.BLANK # space between up and down
        self.distance = Columns.DISTANCE # between 2 columns
        self.speed = Columns.SPEED
        self.surf = Columns.IMG
        self.ls = [] # store the columns' position
        for i in range(3):
            x = (i + 2) * self.distance
            y = random.randrange(60, WIN_HEIGHT - self.blank - 60, 20)
            self.ls.append([x, y])

    def move(self):
        for i in range(3):
            self.ls[i][0] -= self.speed
        if self.ls[0][0] <= -self.width:
            self.ls.pop(0) # delete the columns which is out of window
            # create another columns and append it to self.ls
            self.ls.append([self.ls[-1][0] + self.distance, random.randrange(60, WIN_HEIGHT - self.blank - 60, 10)])


    def draw(self):
        for x, y in self.ls:
            DISPLAYSURF.blit(self.surf, (x, y - self.height))
            DISPLAYSURF.blit(self.surf, (x, y + self.blank))



def rectCollision(rect1, rect2):
    """check two rectangles if they are colliding"""
    if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
        return True
    return False

def isGameOver(bird, columns):
    """get bird and columns hit-box and return whether they collide. if collide, the game is over."""
    for i in range(3):
        rectBird = [bird.x, bird.y, bird.w, bird.h]
        rectColumn1 = [columns.ls[i][0], columns.ls[i][1] - columns.height, columns.width, columns.height]
        rectColumn2 = [columns.ls[i][0], columns.ls[i][1] + columns.blank, columns.width, columns.height]
        if rectCollision(rectBird, rectColumn1) == True or rectCollision(rectBird, rectColumn2) == True:
            return True
    if bird.y + bird.h < 0 or bird.y + bird.h > WIN_HEIGHT:
        return True
    return False


if __name__ == "__main__":
    main()