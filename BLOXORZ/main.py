import pygame as pg
import sys, os
from os.path import join
from math import floor

pg.init()

#setup
SIZE = 680, 400
TILE = 40
W, H = 17, 10
SCREEN = pg.display.set_mode(SIZE)
CLOCK = pg.time.Clock()
LVP = "data/levels"; COMP = "data/components"; IMGP = "data/images"; EXP = "data/extra" #paths
FONT = pg.font.Font(join(EXP, "Minecraft.ttf"), 30)
S1 = pg.mixer.Sound(join(EXP, "step.wav")); S2 = pg.mixer.Sound(join(EXP, "click.wav"))
S1.set_volume(0.4); S2.set_volume(0.7)
S1C = pg.mixer.Channel(0); S2C = pg.mixer.Channel(1) #sound channel

P = 2

bgimg = pg.image.load(join(IMGP, "background.png"))
pimg = pg.image.load(join(IMGP, "player.png"))
pmimg = pg.image.load(join(IMGP, "playerm.png"))
himg = pg.image.load(join(IMGP, "hole.png"))
t1img = pg.image.load(join(IMGP, "tile.png"))
t2img = pg.image.load(join(IMGP, "cwtile.png"))
b1img = pg.image.load(join(IMGP, "circle.png"))
b2img = pg.image.load(join(IMGP, "cross.png"))
b3img = pg.image.load(join(IMGP, "divide.png"))

clevel = 1 #current level
tls = len(os.listdir(LVP)) #total levels
level = []
lb = [] #backup
comp = {} #{bpos: {type: [aT], type: [aT]}}
pp = [] #player position
pb = []
pm = 2 #player main (0 and 1 separate; 2 united)

def set_font():
    global lt, ltr
    lt = FONT.render(str(clevel), True, (255, 255, 255)) #level text
    ltr = lt.get_rect()
    ltr.bottomright = SIZE

def load_level(n):
    lvl = open(join(LVP, f"lvl{n}.txt"), "r")
    l = lvl.read().split("\n")
    lvl.close()
    com = open(join(COMP, f"comp{n}.txt"), "r")
    c = com.read().split("\n"); ct = 0 #cursed technique (count)
    com.close()

    level.clear(); comp.clear(); pp.clear()
    for i in range(H):
        level.append(0) #border left
        try: a = l[i]
        except IndexError: a = ""
        for i in range(W-2):
            try: v = int(a[i]) #value
            except:
                level.append(0) #void if undefined or space
                continue
            if v == P: #register player position
                pp.append(len(level))
                level.append(1) #normal tile under player
                continue
            #register buttons
            if v == 5 or v == 6 or v == 7:
                comp[len(level)] = {}
                for i in c[ct].split("|"):
                    b = i.split("/")
                    comp[len(level)][int(b[0])] = [int(i) for i in b[1].split(" ")]
                ct += 1
            level.append(v) #default value
        level.append(0) #border right
    #save position backup
    pb[:] = pp.copy()
    lb[:] = level.copy()
    set_font()

def set_pos():
    def get_direction():
        if keys[pg.K_LEFT] or keys[pg.K_a]: return -1
        elif keys[pg.K_UP] or keys[pg.K_w]: return -W
        elif keys[pg.K_RIGHT] or keys[pg.K_d]: return 1
        elif keys[pg.K_DOWN] or keys[pg.K_s]: return W
    
    global pp, pm
    tm = [] #position to move
    d = get_direction() #direction
    c = len(pp) #old player-block position

    #setting position to move
    if pm == 2:
        for i in range(c):
            tm.append(pp[i] + d)
        if c == 1:
            tm.append(tm[0] + d)
        #delete former position
        for i in pp:
            try: tm.remove(i)
            except ValueError: pass
        pp[:] = tm.copy()
    else:
        pp[pm] += d
        #check if united
        p1 = pp[pm]; p2 = pp[get_opw()]
        if p1 == p2-1 or p1 == p2-W or p1 == p2+1 or p1 == p2+W:
            pm = 2

    #check player state (death or win)
    check_state()

def activate_comp():
    def act(t): #button type (0, 1, 2)
        S2C.play(S2)
        for i in atiles:
            if t == 0:
                if level[i] == 1: level[i] = 0
                elif level[i] == 0: level[i] = 1
            elif t == 1: level[i] = 1
            elif t == 2: level[i] = 0

    global pm
    for i in pp:
        if i in comp: #player touching component
            c = comp[i]
            for btype, atiles in c.items():
                if level[i] == 5: #circle button
                    act(btype)
                if len(pp) == 1:
                    if level[i] == 6: #cross button
                        act(btype)
                    elif level[i] == 7: #division button
                        pm = btype
                        pp[:] = atiles #joy division!!??
                        S2C.play(S2)
        elif level[i] == 4: #crosswise-only tile
            if len(pp) == 1:
                reset_level()
                break

def reset_level():
    global pm
    pp[:] = pb.copy()
    level[:] = lb.copy()
    pm = 2

def check_state():
    global clevel
    #out of bounds
    for i in pp:
        if i > 169 or i < 0: #limit
            reset_level()
        elif level[i] == 0: #void
            reset_level()
    #hole in one
    if len(pp) == 1 and level[pp[0]] == 3:
        clevel += 1
        load_level(clevel)

def get_opw(): #opposite player main
    if pm == 0: opm = 1
    elif pm == 1: opm = 0
    return opm

delay = pg.USEREVENT + 0
allow_move = True

#user input level
print(f"Available levels: (1-33) (34-{tls-1})")
print("There's no level 0 don't event try it")

try:
    ulevel = int(input("Enter level: ")) #user level
    if ulevel in range(tls):
        clevel = ulevel
except: pass

load_level(clevel)

#main
while 1:
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if not pm == 2:
                    pm = get_opw()
        if event.type == delay:
            allow_move = True

    if keys[pg.K_LEFT] or keys[pg.K_UP] or keys[pg.K_RIGHT] or keys[pg.K_DOWN] or \
       keys[pg.K_a] or keys[pg.K_w] or keys[pg.K_d] or keys[pg.K_s]:
        if allow_move:
            S1C.play(S1)
            set_pos()
            activate_comp()
            allow_move = False
            pg.time.set_timer(delay, 150)

    SCREEN.blit(bgimg, pg.Rect(0, 0, 0, 0))

    #display components
    for i in range(H):
        for j in range(W):
            tile = level[(W * i) + j]
            if tile == 0: #empty void
                continue
            if tile == 1: #normal tile ⬜
                SCREEN.blit(t1img, pg.Rect(TILE*j, TILE*i, 0, 0))
            elif tile == 3: #exit hole 🔳
                SCREEN.blit(himg, pg.Rect(TILE*j, TILE*i, 0, 0))
            elif tile == 4: #crosswise-only tile 🟧
                SCREEN.blit(t2img, pg.Rect(TILE*j, TILE*i, 0, 0))
            elif tile == 5: #all-sides button (circle) ⭕
                SCREEN.blit(b1img, pg.Rect(TILE*j, TILE*i, 0, 0))
            elif tile == 6: #endwise-only button (cross) ❌
                SCREEN.blit(b2img, pg.Rect(TILE*j, TILE*i, 0, 0))
            elif tile == 7: #self division button (()) (endwise-only) 💢
                SCREEN.blit(b3img, pg.Rect(TILE*j, TILE*i, 0, 0))
            elif tile == 2: #player 🟫
                pass

    #display player
    if pm == 2:
        for i in pp:
            SCREEN.blit(pimg, pg.Rect(TILE*(i%W), TILE*floor(i/W), TILE, TILE))
    else:
        SCREEN.blit(pmimg, pg.Rect(TILE*(pp[pm]%W), TILE*floor(pp[pm]/W), TILE, TILE))
        SCREEN.blit(pimg, pg.Rect(TILE*(pp[get_opw()]%W), TILE*floor(pp[get_opw()]/W), TILE, TILE))

    SCREEN.blit(lt, ltr)

    pg.display.flip()
    CLOCK.tick(60)