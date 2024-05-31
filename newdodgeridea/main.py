import pygame as pg
import sys, random
from pygame.locals import *
from pygame.image import load
from os.path import join

pg.init()

#setup
SIZE = W, H = 800, 600
SCREEN = pg.display.set_mode(SIZE)
CLOCK = pg.time.Clock()
IMGP = "images"
ats = True

class player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        pg.mouse.set_pos((W/2, H/2))
        self.rgb = [255, 0, 0]; self.pos = 1
        self.v1 = True; self.v2 = False
        self.set_image()
        self.rect = self.image.get_rect()
        self.update()
    def update(self):
        mpos = pg.mouse.get_pos()
        self.rect.center = mpos
        pg.draw.circle(SCREEN, (0, 0, 0), mpos, 5)
        SCREEN.blit(self.image, self.rect)
        self.set_color()
    def set_color(self):
        if self.v1 and not self.rgb[self.pos] == 255:
            self.rgb[self.pos] += 1
        elif self.v2 and not self.rgb[self.pos] == 0:
            self.rgb[self.pos] -= 1
        else:
            self.set_pos()
        self.set_image()
    def set_pos(self):
        self.v1 = not self.v1
        self.v2 = not self.v2
        self.pos -= 1
        if self.pos == -1:
            self.pos = 2
    def set_image(self):
        self.image = pg.Surface((24, 24), pg.SRCALPHA)
        self.image.convert_alpha()
        pg.draw.circle(self.image, self.rgb, (12, 12), 12)
        self.mask = pg.mask.from_surface(self.image)

enemies = pg.sprite.Group() #sprite group for enemies

class enemy(pg.sprite.Sprite):
    def __init__(self, w, h):
        pg.sprite.Sprite.__init__(self, enemies)
        self.w = w
        self.h = h
        #self.image = load(join(IMGP, "circle.png")).convert_alpha()
        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA)
        self.image.convert_alpha()
        pg.draw.ellipse(self.image, (0, 0, 255), (0, 0, self.w, self.h))
        #pg.draw.rect(self.image, (0, 0, 255), pg.Rect(0, 0, self.w, self.h))
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        
        self.xr = list(range(-self.w, W + 1, 10))
        self.yr = list(range(-self.h, H + 1, 10))
        self.set_dest()
        
    def get_pos(self):
        if random.choice((1, 0)): #left or right
            x = random.choice((self.xr[0], self.xr[-1]))
            y = random.choice(self.yr)
        else: #top or bottom
            x = random.choice(self.xr)
            y = random.choice((self.yr[0], self.yr[-1]))

        return (x, y)
    
    def set_dist(self):
        self.dist = (-self.rect.x + self.dest[0], -self.rect.y + self.dest[1])
    
    def set_dest(self):
        do = 1 #plz python just implement do while loop already 😭😭
        self.dest = self.get_pos()
        while self.rect.x == self.dest[0] or self.rect.y == self.dest[1] or do:
            do = 0
            self.rect.topleft = self.get_pos()
        self.set_dist()
        #set if move forward or backward/set speed
        self.xs = int(self.dist[0]/abs(self.dist[0]))
        self.ys = int(self.dist[1]/abs(self.dist[1]))
        #prevent 0 distance
        self.measure = abs(abs(self.dist[0]) - abs(self.dist[1]))/min(abs(self.dist[0]), abs(self.dist[1]))
        #x or y movement constant
        self.constd = "x" if abs(self.dist[0]) > abs(self.dist[1]) else "y"

    def shift(self):
        self.set_dist()
        try: self.compare = abs(abs(self.dist[0]) - abs(self.dist[1]))/min(abs(self.dist[0]), abs(self.dist[1]))
        except: pass
        if self.constd == "x": #x axis movement constant
            self.rect.x += self.xs
            if self.compare <= self.measure:
                if not self.rect.y == self.dest[1]:
                    self.rect.y += self.ys
        else: #y axis movement constant
            self.rect.y += self.ys
            if self.compare <= self.measure:
                if not self.rect.x == self.dest[0]:
                    self.rect.x += self.xs

        #reset starting point and destination
        if self.rect.topleft == self.dest:
            self.set_dest()

A1 = enemy(200, 100)
A2 = enemy(100, 200)
A3 = enemy(200, 200)
A4 = enemy(200, 200)
A5 = enemy(300, 300)
A6 = enemy(50, 50)
A7 = enemy(50, 100)
A8 = enemy(100, 50)
A9 = enemy(100, 100)
A10 = enemy(100, 100)

PLAYER = player()

allow_ts = pg.USEREVENT + 0
pg.time.set_timer(allow_ts, 5000)

while 1:
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT or keys[K_ESCAPE]:
            pg.quit()
            sys.exit()
        if event.type == allow_ts:
            ats = True
        if keys[K_SPACE]:
            if ats:
                ats = False
                pg.time.delay(1000)

    SCREEN.fill((30, 30, 30))

    for e in enemies:
        #collide
        if pg.sprite.collide_mask(PLAYER, e):
            pass
            #print("a")
        #enemy movement
        e.shift()

    enemies.draw(SCREEN)
    PLAYER.update()

    pg.display.flip()
    CLOCK.tick(500)

"""
player ball is black and mouse hidden with smaller black point

za warudo timestop

special enemies ideas
king JIJIJIJA
snake gif animation
charlie woo meme
random letters that spin and appear as a group

...
"""