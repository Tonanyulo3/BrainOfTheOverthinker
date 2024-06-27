import pygame as pg
import sys
from pygame.locals import K_ESCAPE
from pygame.image import load
from os.path import join
from random import choice, choices

pg.init()

#setup
IMGP = "images"
SIZE = W, H = 800, 600
SCREEN = pg.display.set_mode(SIZE)
CLOCK = pg.time.Clock()
pg.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

BLACK = pg.Color(0, 0, 0)
WHITE = pg.Color(255, 255, 255)
man = load(join(IMGP, "manface.png")).convert_alpha()

font = pg.font.Font(join(IMGP, "Minecraft.ttf"), 50)
text1 = font.render("RIGHT CLICK TO START", True, WHITE)
text2 = font.render("LEFT CLICK TO TIMESTOP", True, WHITE)
score = 0; start = 0

se1 = pg.mixer.Sound(join(IMGP, "madeinheaven.mp3"))
se1.set_volume(0.8)
se2 = pg.mixer.Sound(join(IMGP, "zawarudo.mp3"))

enemies = pg.sprite.Group() #sprite group for enemies

def reset():
    global ats, ts, fps, gaming, bgc, bgcr, stext, srect, score
    ats = True; ts = False
    fps = 200
    gaming = False
    bgc = [0, 0, 0]; bgcr = [255, 255, 255]
    for e in enemies:
        e.die()
    pg.mouse.set_pos((W/2, H/2))
    pg.mixer.stop()
    #score text
    stext = font.render(str(score), True, WHITE)
    srect = stext.get_rect()
    srect.center = (W/2, H/2)
    #reset enemies
    if score >= 19500 or not enemies.has():
        enemies.empty()
        enemies.add(enemy(250, 250))
        enemies.add(enemy(200, 200))
        enemies.add(enemy(150, 200))
        enemies.add(enemy(200, 150))
        enemies.add(enemy(150, 150))
        enemies.add(enemy(150, 100))
        enemies.add(enemy(100, 150))
        enemies.add(enemy(100, 100))
        enemies.add(enemy(100, 50))
        enemies.add(enemy(50, 100))
        enemies.add(enemy(50, 50))
        enemies.add(enemy(50, 50))
        enemies.add(enemy(50, 50))

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
    def __init__(self, width=0, height=0):
        pg.sprite.Sprite.__init__(self, enemies)
        self.w = width
        self.h = height
        self.xr = list(range(-width-10, W + 11, 10)) #10px difference for appearance
        self.yr = list(range(-height-10, H + 11, 10))
        self.set_image()
        self.rect = self.image.get_rect()
        self.set_dest()
    def get_pos(self):
        if choice((1, 0)): #left or right
            x = choice((self.xr[0], self.xr[-1]))
            y = choice(self.yr)
        else: #top or bottom
            x = choice(self.xr)
            y = choice((self.yr[0], self.yr[-1]))
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
        self.xs = (1 if self.dist[0]>=0 else -1)
        self.ys = (1 if self.dist[1]>=0 else -1)
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
    def set_image(self):
        color = choices((WHITE, choices(([255, 255, 0], [255, 0, 255], [0, 255, 255]))[0], choices(([255, 0, 0], [0, 255, 0], [0, 0, 255]))[0]), weights=[1, 25, 40])[0]
        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA)
        self.image.convert_alpha()
        pg.draw.ellipse(self.image, color, (0, 0, self.w, self.h))
        pg.draw.ellipse(self.image, bgc, (0, 0, self.w, self.h), 2)
        if color == WHITE: #OOF
            manface = pg.transform.scale(man, (self.w, self.h))
            self.image.blit(manface, (0, 0, 0, 0))
        self.mask = pg.mask.from_surface(self.image)
    def check_dest(self):
        #reset starting point and destination
        if self.rect.topleft == self.dest:
            self.die()
    def die(self):
        self.set_dest()
        self.set_image()

P = player()

reset() #game parameters reset

allow_ts = pg.USEREVENT + 0
timestop = pg.USEREVENT + 1
change_color = pg.USEREVENT + 2
pg.time.set_timer(change_color, 235)
time_accel = pg.USEREVENT + 3

while 1:
    keys = pg.key.get_pressed()
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
        if event.type == time_accel:
            se1.play()
            fps += 30
            enemies.add(enemy(80, 80))
    
    #check mouse press (timestop)
    mp = pg.mouse.get_pressed()
    if mp[0]:
        if ats:
            pg.time.set_timer(allow_ts, 5000)
            pg.time.set_timer(timestop, 1000)
            ats = False; ts = True
            se2.play()

    SCREEN.fill(bgc)

    #text display on game pause
    if not gaming:
        #check mouse press (gamestart)
        if mp[2]:
            gaming = True
            score = 0
            start = pg.time.get_ticks()
            
            pg.time.set_timer(time_accel, 20000)
        #display hint text
        SCREEN.blit(text1, pg.Rect(90, 100, 0, 0))
        SCREEN.blit(text2, pg.Rect(80, 450, 0, 0))
        SCREEN.blit(stext, srect)
    else:
        #time score calculation
        score = pg.time.get_ticks() - start

    #display enemies
    enemies.draw(SCREEN)
    pg.draw.circle(SCREEN, bgcr, pg.mouse.get_pos(), 8)
    P.blit()

    if not ts:
        P.update()
        if gaming: #enemies don't move on timestop and game pause
            for e in enemies:
                #enemy movement
                e.shift()
                e.check_dest()
                #collide
                if pg.sprite.collide_mask(P, e):
                    gaming = False
                    reset()

                    pg.time.set_timer(time_accel, 0)

    pg.display.flip()
    CLOCK.tick(fps)