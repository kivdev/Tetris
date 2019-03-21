import random

import pygame

FPS = 30
DEFAULT_SPEED = 4
IN_GAME = True
RECT_SIZE = 25
CAR_W = (RECT_SIZE + 4) * 3
CAR_H = (RECT_SIZE + 4) * 4
BG = (180, 195, 180)
ORANGE = (255, 150, 100)
W = 4 + (RECT_SIZE + 4) * 11
block = None
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
        self.move(x, y)

    def move(self, x, y):
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


blocks = []

k = 0
class Block:
    # 0: куб, 1:т, 2:г, 3:левая z, 4:правая z, 5:прямая, 6:обратная г
    def __init__(self, x, y):
        self.block_type = random.randint(0, 6)
        self.rotate = 0
        self.move(x, y)

    def draw(self):
        for i in self.__dict__.values():
            if isinstance(i, Rect):
                i.draw()

    def move(self, x, y):
        self.x = x
        self.y = y
        if self.block_type == 0:
            self.x2 = x + (RECT_SIZE) * 2
            self.y2 = y + (RECT_SIZE) * 2
            self.w = self.x2 - self.x
            self.h = self.y2 - self.y
            self._lt = Rect(x, y)
            self._rt = Rect(x + RECT_SIZE, y)
            self._lb = Rect(x, y + RECT_SIZE)
            self._rb = Rect(x + RECT_SIZE, y + RECT_SIZE)
        elif self.block_type == 1:
            self.x2 = x + (RECT_SIZE) * 3
            self.y2 = y + (RECT_SIZE) * 2
            self.w = self.x2 - self.x
            self.h = self.y2 - self.y
            self._t = Rect(x + RECT_SIZE, y)
            self._lb = Rect(x, y+ RECT_SIZE)
            self._mb = Rect(x + RECT_SIZE, y + RECT_SIZE)
            self._rb = Rect(x + RECT_SIZE * 2, y + RECT_SIZE)
        elif self.block_type == 2:
            self.x2 = x + (RECT_SIZE) * 3
            self.y2 = y + (RECT_SIZE) * 2
            self.w = self.x2 - self.x
            self.h = self.y2 - self.y
            self._t = Rect(x + RECT_SIZE * 2, y)
            self._lb = Rect(x, y+ RECT_SIZE)
            self._mb = Rect(x + RECT_SIZE, y + RECT_SIZE)
            self._rb = Rect(x + RECT_SIZE * 2, y + RECT_SIZE)
        elif self.block_type == 6:
            self.x2 = x + (RECT_SIZE) * 3
            self.y2 = y + (RECT_SIZE) * 2
            self.w = self.x2 - self.x
            self.h = self.y2 - self.y
            self._t = Rect(x, y)
            self._lb = Rect(x , y+ RECT_SIZE)
            self._mb = Rect(x + RECT_SIZE, y + RECT_SIZE)
            self._rb = Rect(x + RECT_SIZE * 2, y + RECT_SIZE)
        elif self.block_type == 3:
            self.x2 = x + (RECT_SIZE) * 3
            self.y2 = y + (RECT_SIZE) * 2
            self.w = self.x2 - self.x
            self.h = self.y2 - self.y
            self._lt = Rect(x, y)
            self._mt = Rect(x + RECT_SIZE, y)
            self._mb = Rect(x + RECT_SIZE, y + RECT_SIZE)
            self._rb = Rect(x + RECT_SIZE * 2, y + RECT_SIZE)
        elif self.block_type == 4:
            self.x2 = x + (RECT_SIZE) * 3
            self.y2 = y + (RECT_SIZE) * 2
            self.w = self.x2 - self.x
            self.h = self.y2 - self.y
            self._mt = Rect(x + RECT_SIZE, y)
            self._rt = Rect(x + RECT_SIZE * 2, y)
            self._lb = Rect(x, y + RECT_SIZE)
            self._mb = Rect(x + RECT_SIZE, y + RECT_SIZE)
        elif self.block_type == 5:
            self.x2 = x + (RECT_SIZE) * 4
            self.y2 = y + (RECT_SIZE) * 1
            self.w = self.x2 - self.x
            self.h = self.y2 - self.y
            self._lt = Rect(x, y)
            self._lmt = Rect(x + RECT_SIZE, y)
            self._rmt = Rect(x + RECT_SIZE * 2, y)
            self._rt = Rect(x + RECT_SIZE * 3, y)
        self.draw()

    def __eq__(self, other):
        global block
        if (self.y <= other.y <= self.y2 and self.x <= other.x < self.x2) or (self.y <= other.y2 <= self.y2 and
                                                                              self.x < other.x2 <= self.x2):
            # Более сложная логика размещения
            y = other.y-1
            block.move(block.x,y-block.h)
            block = None
            blocks.append(self)


start_pos = sc_w / 2 - RECT_SIZE * 2

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
                elif i.key == pygame.K_DOWN:
                    motion = 'speed'
            elif i.type == pygame.KEYUP:
                if i.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN]:
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
    if block:
        if motion == 'left' and block.x-RECT_SIZE>=0:
            block.move(block.x-RECT_SIZE,block.y)
        elif motion == 'right' and block.x2+RECT_SIZE<=sc_w:
            block.move(block.x+RECT_SIZE,block.y)
        elif motion == 'speed':
            SPEED = DEFAULT_SPEED + 10
        elif motion == 'stop':
            SPEED = DEFAULT_SPEED
    if block is None:
        block = Block(start_pos, -RECT_SIZE * 2)
    elif block.y2 < sc_h:
        block.move(block.x, block.y + SPEED)
    if block.y2 > sc_h:
        block.move(block.x, sc_h-block.h)
        blocks.append(block)
        block = None
    for i in blocks:
        if block:
            block == i
        i.draw()
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
