import random

import pygame

FPS = 30
DEFAULT_SPEED = 8
IN_GAME = True
RECT_SIZE = 25
CAR_W = (RECT_SIZE + 4) * 3
CAR_H = (RECT_SIZE + 4) * 4
BG = (180, 195, 180)
ORANGE = (255, 150, 100)
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
    color = {1: (0, 0, 0), 2: (155, 55, 0), 3: (10, 150, 10)}

    def __init__(self, x, y, color):
        self.color = self.color[color]
        self.move(x, y)

    def move(self, x, y):
        self.x = x
        self.y = y
        self.x1 = x
        self.x2 = x + 5
        self.y1 = y
        self.y2 = y + 5
        self.coords1 = (self.x1, self.y1, RECT_SIZE, RECT_SIZE)
        self.coords2 = (self.x2, self.y2, int(RECT_SIZE -9), int(RECT_SIZE-9))

    def draw(self):
        global sc
        pygame.draw.rect(sc, self.color,
                         self.coords1, 2)
        pygame.draw.rect(sc, self.color,
                         self.coords2)


class Car:
    def __init__(self, x, y, color):
        self.color = color
        self.move(x, y)

    def draw(self):
        self.head.draw()
        self.r_top.draw()
        self.r_bottom.draw()
        self.l_top.draw()
        self.l_bottom.draw()
        self.center.draw()

    def move(self, x, y):
        self.x = x
        self.y = y
        self.x2 = x + CAR_W
        self.y2 = y + CAR_H
        self.head = Rect(self.x + RECT_SIZE, self.y, self.color)
        self.r_top = Rect(self.x, self.y + RECT_SIZE, self.color)
        self.r_bottom = Rect(self.x, self.y + (RECT_SIZE) * 3, self.color)
        self.center = Rect(self.x + (RECT_SIZE), self.y + (RECT_SIZE) * 2, self.color)
        self.l_top = Rect(self.x + (RECT_SIZE) * 2, self.y + RECT_SIZE, self.color)
        self.l_bottom = Rect(self.x + (RECT_SIZE) * 2, self.y + (RECT_SIZE) * 3, self.color)

    def __eq__(self, other):
        global IN_GAME
        if (self.y <= other.y <= self.y2 and self.x <= other.x < self.x2) or (self.y <= other.y2 <= self.y2 and
                                                                              self.x < other.x2 <= self.x2):
            # print('.|p|c\nx|{}|{}\nx2|{}|{}\ny|{}|{}\ny2|{}|{}'.format(self.x,other.x,self.x2,other.x2,self.y,
            #                                                           other.y,self.y2,other.y2))
            IN_GAME = False


border = []
y = sc_h
while y > -sc_h / 4:
    border.append(Rect(2, y, 1))
    border.append(Rect(sc_w - 3 - RECT_SIZE, y, 1))
    y -= RECT_SIZE + 4

cars = []
# positions = [(RECT_SIZE + 4) + 2, (RECT_SIZE + 4) + 2 + ((RECT_SIZE + 4)) * 3,
#             (RECT_SIZE + 4) + 2 + #((RECT_SIZE + 4)) * 3 * 2]
road = sc_w - (RECT_SIZE + 4) * 2
free = road - (round(road / (CAR_W), 0) * (CAR_W))  # (sc_w-int(sc_w/CAR_W)*CAR_W)/2)+
print(free, road, CAR_W, round(road / (CAR_W + 4), 0))
if free<0:
    free = 0
positions = [int(abs(free) / 2) + (RECT_SIZE + 4) + 2 + CAR_W * i for i in
             range(0, int((sc_w - (RECT_SIZE + 4) * 2) / CAR_W))]

for i in range(10):
    rand = random.choice(positions)
    x = rand
    y = 0 - CAR_H
    if cars:
        rand = random.randint(1, 3)
        delta = CAR_H * rand
        y = cars[-1].y - delta
    cars.append(Car(x, y, 1))#2


def main():
    player = Car(positions[len(positions) // 2], sc_h - ((RECT_SIZE + 4) * 5), 1)  # 3
    IN_GAME = True
    SPEED = DEFAULT_SPEED
    iter = 0
    motion = 'stop'
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
                        motion = 'speed'
                elif i.type == pygame.KEYUP:
                    if i.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP]:
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
        if motion == 'left' and player.x != positions[0] and iter > FPS / SPEED / 2:
            player.move(positions[positions.index(player.x) - 1], player.y)
            iter = 0
        elif motion == 'right' and player.x != positions[-1] and iter > FPS / SPEED / 2:
            print(positions)
            player.move(positions[positions.index(player.x) + 1], player.y)
            iter = 0
        elif motion == 'speed':
            SPEED = DEFAULT_SPEED + 10
        elif motion == 'stop':
            SPEED = DEFAULT_SPEED

        if border[0].y > sc_h:
            y = border[-2].y - 4 - RECT_SIZE
            i = border.pop(0)
            i.y = y
            border.append(i)
        for i in border:
            i.move(i.x, i.y + SPEED)
            i.draw()
        if cars[0].y > sc_h:
            rand = random.randint(1, 3)
            if rand == 1:
                delta = CAR_H + RECT_SIZE + 4
            else:
                delta = CAR_H * rand
            i = cars.pop(0)
            i.y = cars[-1].y - delta
            cars.append(i)
        for i, car in enumerate(cars):
            car.move(car.x, car.y + SPEED)
            car == player
            car.draw()

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
main()
