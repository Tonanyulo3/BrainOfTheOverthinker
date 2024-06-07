import pygame as pg
import sys, random, time
from pygame.locals import *
from pygame.image import load
from os.path import join

pg.init()

#setup
SIZE = W, H = 800, 600
SCREEN = pg.display.set_mode(SIZE)
CLOCK = pg.time.Clock()
IMGP = "images"
pg.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

BLACK = pg.Color(0, 0, 0)
WHITE = pg.Color(255, 255, 255)
man = load(join(IMGP, "manface.png")).convert_alpha()

font = pg.font.Font(join(IMGP, "Minecraft.ttf"), 50)
text1 = font.render("RIGHT CLICK TO START", True, WHITE)
text2 = font.render("LEFT CLICK TO TIMESTOP", True, WHITE)
score = 0; start = 0

enemies = pg.sprite.Group() #sprite group for enemies

def reset():
    global ats, ts, fps, gaming, bgc, bgcr, stext, srect, score
    ats = True; ts = False
    fps = 250
    gaming = False
    bgc = [0, 0, 0]; bgcr = [255, 255, 255]
    for i in enemies:
        i.set_dest()
    pg.mouse.set_pos((W/2, H/2))
    #score text
    stext = font.render(str(score), True, WHITE)
    srect = stext.get_rect()
    srect.center = (W/2, H/2)

def bgcolor():
    if not bgc == [255, 255, 255]:
        bgc[0] += 1; bgc[1] += 1; bgc[2] += 1
        bgcr[0] -= 1; bgcr[1] -= 1; bgcr[2] -= 1

class player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.rgb = [255, 0, 0]; self.pos = 1
        self.v1 = True; self.v2 = False
        self.set_image()
        self.rect = self.image.get_rect()
        self.update()
    def update(self):
        mpos = pg.mouse.get_pos()
        self.rect.center = mpos
        self.blit()
    def blit(self):
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

class enemy(pg.sprite.Sprite):
    def __init__(self, width, height):
        pg.sprite.Sprite.__init__(self, enemies)
        self.w = width
        self.h = height
        self.set_image()
        self.rect = self.image.get_rect()
        
        self.xr = list(range(-self.w-10, W + 11, 10)) #10px difference for appearance
        self.yr = list(range(-self.h-10, H + 11, 10))
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
    def set_image(self):
        color = random.choices((WHITE, random.choices(([255, 255, 0], [255, 0, 255], [0, 255, 255]))[0], random.choices(([255, 0, 0], [0, 255, 0], [0, 0, 255]))[0]), weights=[1, 25, 40])[0]
        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA)
        self.image.convert_alpha()
        pg.draw.ellipse(self.image, color, (0, 0, self.w, self.h))
        pg.draw.ellipse(self.image, bgc, (0, 0, self.w, self.h), 2)
        if color == WHITE: #OOF
            manface = pg.transform.scale(man, (self.w, self.h))
            self.image.blit(manface, (0, 0, 0, 0))
        self.mask = pg.mask.from_surface(self.image)
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
            self.set_image()

reset() #game parameters reset

enemies.add(enemy(350, 350))
enemies.add(enemy(250, 250))
enemies.add(enemy(200, 200))
enemies.add(enemy(150, 200))
enemies.add(enemy(200, 150))
enemies.add(enemy(150, 150))
enemies.add(enemy(125, 125))
enemies.add(enemy(150, 100))
enemies.add(enemy(100, 150))
enemies.add(enemy(100, 100))
enemies.add(enemy(100, 50))
enemies.add(enemy(50, 100))
enemies.add(enemy(50, 50))
enemies.add(enemy(50, 50))
enemies.add(enemy(50, 50))

P = player()

allow_ts = pg.USEREVENT + 0
timestop = pg.USEREVENT + 1
change_color = pg.USEREVENT + 2
pg.time.set_timer(change_color, 235)

while 1:
    keys = pg.key.get_pressed()
    mp = pg.mouse.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT or keys[K_ESCAPE]:
            pg.quit()
            sys.exit()
        if event.type == change_color:
            if gaming:
                bgcolor()
        if event.type == allow_ts:
            ats = True
        if event.type == timestop:
            ts = False
        if mp[0]:
            if ats:
                pg.time.set_timer(allow_ts, 5000)
                pg.time.set_timer(timestop, 1000)
                ats = False; ts = True
        if mp[2]:
            gaming = True
            score = 0
            start = pg.time.get_ticks()

    SCREEN.fill(bgc)

    #text display on game pause
    if not gaming:
        SCREEN.blit(text1, pg.Rect(90, 100, 0, 0))
        SCREEN.blit(text2, pg.Rect(80, 450, 0, 0))
        SCREEN.blit(stext, srect)
    else:
        #time score calculation
        score = pg.time.get_ticks() - start

    if not ts:
        P.update()
        if gaming: #enemies don't move on timestop and game pause
            for e in enemies:
                #enemy movement
                e.shift()
                #collide
                if pg.sprite.collide_mask(P, e):
                    gaming = False
                    reset()

    enemies.draw(SCREEN)
    pg.draw.circle(SCREEN, bgcr, pg.mouse.get_pos(), 8)
    P.blit()

    pg.display.flip()
    CLOCK.tick(fps)

"""
player ball is black and mouse hidden with smaller black point

za warudo timestop

special enemies ideas
king JIJIJIJA
snake gif animation
charlie woo meme
random letters that spin and appear as a group
MADE IN HEAVEN
LOL logo
POOP
...
"""