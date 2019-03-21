import random

import pygame

FPS = 30
DEFAULT_SPEED = 8
IN_GAME = True
RECT_SIZE = 25
TANK_W = (RECT_SIZE + 4) * 3
TANK_H = (RECT_SIZE + 4) * 3
BG = (180, 195, 180)
W = 4 + (RECT_SIZE + 4) * 11

pygame.init()

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

clock = pygame.time.Clock()

sc = pygame.display.set_mode((W, 0))

sc_w, sc_h = sc.get_rect()[2:4]
if sc_h / 2 > W:
    sc = pygame.display.set_mode((W, W * 2))
    sc_w, sc_h = sc.get_rect()[2:4]


class Rect:
    global sc
    color = (0, 0, 0)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x1 = x
        self.x2 = x + 5
        self.y1 = y
        self.y2 = y + 5
        self.coords1 = (self.x1, self.y1, RECT_SIZE, RECT_SIZE)
        self.coords2 = (self.x2, self.y2, int(RECT_SIZE - 9), int(RECT_SIZE - 9))


    def draw(self):
        global sc
        pygame.draw.rect(sc, self.color,
                         self.coords1, 2)
        pygame.draw.rect(sc, self.color,
                         self.coords2)


class Tank:
    color = (0, 0, 0)
    def __init__(self, x, y, player = None):
        self.player = None
        if self.player:
            r = 'forward'
        self.move(x, y, r)

    def draw(self):
        for i in self.__dict__.values():
            if isinstance(i, Rect):
                i.draw()

    def move(self, x, y,r=None):
        if r == 'forward':
            self.x = x
            self.y = y
            self.x2 = x + TANK_W
            self.y2 = y + TANK_H
            self.head = Rect(x+RECT_SIZE,y)
            self.l_top = Rect(x,y+RECT_SIZE)
            self.m_top = Rect(x+RECT_SIZE,y+RECT_SIZE)
            self.r_top = Rect(x+RECT_SIZE*2,y+RECT_SIZE)
            self.l_bottom = Rect(x,y+RECT_SIZE*2)
            if self.player:
                self.m_bottom = Rect(x+RECT_SIZE,y+RECT_SIZE*2)
            self.r_bottom = Rect(x+RECT_SIZE*2,y+RECT_SIZE*2)
        if r == 'left':
            self.x = x
            self.y = y
            self.x2 = x + TANK_W
            self.y2 = y + TANK_H
            self.head = Rect(x, y + RECT_SIZE)
            self.l_top = Rect(x + RECT_SIZE, y + RECT_SIZE*3)
            self.m_top = Rect(x + RECT_SIZE, y + RECT_SIZE*2)
            self.r_top = Rect(x + RECT_SIZE, y + RECT_SIZE)
            self.l_bottom = Rect(x + RECT_SIZE * 2, y + RECT_SIZE * 3)
            if self.player:
                self.m_bottom = Rect(x + RECT_SIZE * 2, y + RECT_SIZE * 2)
            self.r_bottom = Rect(x + RECT_SIZE * 2, y + RECT_SIZE)
        if r == 'right':
            self.x = x
            self.y = y
            self.x2 = x + TANK_W
            self.y2 = y + TANK_H
            self.head = Rect(x + RECT_SIZE, y)
            self.l_top = Rect(x, y + RECT_SIZE)
            self.m_top = Rect(x + RECT_SIZE, y + RECT_SIZE)
            self.r_top = Rect(x + RECT_SIZE * 2, y + RECT_SIZE)
            self.l_bottom = Rect(x, y + RECT_SIZE * 2)
            if self.player:
                self.m_bottom = Rect(x + RECT_SIZE, y + RECT_SIZE * 2)
            self.r_bottom = Rect(x + RECT_SIZE * 2, y + RECT_SIZE * 2)
        if r == 'back':
            self.x = x
            self.y = y
            self.x2 = x + TANK_W
            self.y2 = y + TANK_H
            self.head = Rect(x + RECT_SIZE, y)
            self.l_top = Rect(x, y + RECT_SIZE)
            self.m_top = Rect(x + RECT_SIZE, y + RECT_SIZE)
            self.r_top = Rect(x + RECT_SIZE * 2, y + RECT_SIZE)
            self.l_bottom = Rect(x, y + RECT_SIZE * 2)
            if self.player:
                self.m_bottom = Rect(x + RECT_SIZE, y + RECT_SIZE * 2)
            self.r_bottom = Rect(x + RECT_SIZE * 2, y + RECT_SIZE * 2)

        self.draw()

    def __eq__(self, other):
        pass
        #global IN_GAME
        #if (self.y <= other.y <= self.y2 and self.x <= other.x < self.x2) or (self.y <= other.y2 <= self.y2 and
        #                                                                      self.x < other.x2 <= self.x2):
        #    # print('.|p|c\nx|{}|{}\nx2|{}|{}\ny|{}|{}\ny2|{}|{}'.format(self.x,other.x,self.x2,other.x2,self.y,
        #    #                                                           other.y,self.y2,other.y2))
        #    IN_GAME = False



player = Tank(sc_w/2-TANK_W/2, sc_h - ((RECT_SIZE + 4) * 5), 1)
iter = 0
motion = 'stop'
IN_GAME = True
SPEED = DEFAULT_SPEED
while IN_GAME:
    iter += 1
    if iter > 800:
        iter = 0
    sc.fill(BG)
    for i in pygame.event.get():
        try:
            if i.type == pygame.QUIT:
                exit()
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_LEFT:
                    motion = 'left'
                elif i.key == pygame.K_RIGHT:
                    motion = 'right'
                elif i.key == pygame.K_UP:
                    motion = 'forward'
                elif i.key == pygame.K_DOWN:
                    motion = 'back'
            elif i.type == pygame.KEYUP:
                if i.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    motion = 'stop'
            elif i.type == pygame.FINGERDOWN:
                if i.x < 0.5:
                    print(i.x)
                    motion = 'left'
                else:
                    motion = 'right'
            elif i.type == pygame.FINGERUP:
                motion = 'stop'
        except AttributeError:
            pass
    if motion == 'left':
        player.move(player.x-SPEED,player.y,'left')
    elif motion == 'right':
        player.move(player.x+SPEED,player.y,'left')
    if motion == 'forward':
        player.move(player.x,player.y-SPEED,'top')
    elif motion == 'back':
        player.move(player.x,player.y+SPEED,'down')

    elif motion == 'stop':
        SPEED = DEFAULT_SPEED

    player.draw()
    pygame.display.update()
    if pygame.get_error():
        pass
        # print(pygame.get_error())
    clock.tick(FPS)
textsurface = myfont.render('Game Over', False, (255, 0, 0))
sc.blit(textsurface, (sc_w / 4, sc_h / 2))
pygame.display.update()
while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
