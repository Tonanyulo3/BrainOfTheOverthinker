import pygame as pg
from pygame.image import load
from pygame.locals import K_SPACE, K_1
from os.path import join
import sys, random

def main():
    pg.init()
    pg.font.init()
    pg.mixer.init()

    #setup
    SIZE = (500, 500)
    SCREEN = pg.display.set_mode(SIZE)
    CLOCK = pg.time.Clock()

    imgp = "images"

    s1 = pg.mixer.Sound(join(imgp, "click.wav"))
    s2 = pg.mixer.Sound(join(imgp, "win.wav"))
    s1.set_volume(0.5)
    s2.set_volume(0.8)

    font1 = pg.font.Font(join(imgp, "Minecraft.ttf"), 16)
    font2 = pg.font.Font(join(imgp, "Minecraft.ttf"), 30)

    class b(pg.sprite.Sprite):
        #i cant believe this actually works
        def __init__(self):
            super().__init__()
            self.image = [pg.Surface((0, 0))]
            self.index = 0
            self.v = [False, False]
            self.open = None
        
        def rimage(self):
            return self.image[self.index]

    class game(pg.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.clicka = False; self.clicka2 = True
            self.fontcolor = [pg.Color(0, 0, 0), pg.Color(225, 225, 225)]; self.fcindex = 0
            self.ai = False
            #main table
            self.image = [load(join(imgp, "table1.png")).convert_alpha(), load(join(imgp, "table2.png")).convert_alpha()]
            self.bgcolor = [pg.Color(255, 229, 140), pg.Color(0, 0, 0)]
            self.index = 0
            self.nought = load(join(imgp, "nought.png")).convert_alpha(); self.snought = load(join(imgp, "snought.png")).convert_alpha(); self.mnought = load(join(imgp, "mininought.png")).convert_alpha(); self.nps = "0"
            self.cross = load(join(imgp, "cross.png")).convert_alpha(); self.scross = load(join(imgp, "scross.png")).convert_alpha(); self.mcross = load(join(imgp, "minicross.png")).convert_alpha(); self.cps = "0"
            self.turn = self.nought #inverted first hand
            self.nrect = [pg.Rect((50, 50), (128, 128)), pg.Rect((186, 50), (128, 128)), pg.Rect((322, 50), (128, 128)), 
                        pg.Rect((50, 186), (128, 128)), pg.Rect((186, 186), (128, 128)), pg.Rect((322, 186), (128, 128)), 
                        pg.Rect((50, 322), (128, 128)), pg.Rect((186, 322), (128, 128)), pg.Rect((322, 322), (128, 128))]
            
            #light/dark mode
            self.b1 = b()
            self.b1.image = [load(join(imgp, "sun.png")).convert_alpha(), load(join(imgp, "moon.png")).convert_alpha()]
            self.b1.rect = pg.Rect((460, 60), (30, 30))
            #easy/medium/pro mode
            self.b2 = b()
            self.b2.image = [load(join(imgp, "easy.png")).convert_alpha(), load(join(imgp, "normal.png")).convert_alpha(), load(join(imgp, "hard.png")).convert_alpha()]
            self.b2.rect = [pg.Rect((460, 120), (30, 30)), pg.Rect((460, 160), (30, 30)), pg.Rect((460, 200), (30, 30))]
            self.b2.index = 1
            self.b2.v = [[False, False], [False, False], [False, False]]
            #replacement/noreplacement mode
            self.b3 = b()
            self.b3.image = [load(join(imgp, "noreplacement.png")).convert_alpha(), load(join(imgp, "replacement1.png")).convert_alpha(), load(join(imgp, "replacement2.png")).convert_alpha()]
            self.b3.rect = pg.Rect((460, 260), (30, 30))
            #restart game button
            self.b4 = b()
            self.b4.image = [load(join(imgp, "restart1.png")).convert_alpha(), load(join(imgp, "restart2.png")).convert_alpha()]
            self.b4.rect = pg.Rect((460, 410), (30, 30))
            #reset game button
            self.b5 = b()
            self.b5.image = load(join(imgp, "reset.png")).convert_alpha()
            self.b5.rect = pg.Rect((10, 410), (30, 30))
            #menu button
            self.b6 = b()
            self.b6.image = load(join(imgp, "menu.png")).convert_alpha()
            self.b6.rect = pg.Rect((10, 60), (30, 30))
            #AI button
            self.b7 = b()
            self.b7.image = [load(join(imgp, "noreplacement.png")).convert_alpha(), load(join(imgp, "robot1.png")).convert_alpha(), load(join(imgp, "robot2.png")).convert_alpha()]
            self.b7.rect = pg.Rect((10, 120), (30, 30))

            #set table
            self.tablereset()
            self.fontset()

        def perform(self):
            #main game
            SCREEN.fill(self.bgcolor[self.index])
            SCREEN.blit(self.image[self.index], (50, 50))
            #brute force 💀 check
            self.t = 0 if (self.turn == self.cross) else 1
            self.mp = pg.mouse.get_pos()
            self.mr = pg.mouse.get_pressed()[0]
            pos = None
            if not (self.nrect[0].collidepoint(self.mp) or self.nrect[1].collidepoint(self.mp) or self.nrect[2].collidepoint(self.mp) or self.nrect[3].collidepoint(self.mp) or self.nrect[4].collidepoint(self.mp) or self.nrect[5].collidepoint(self.mp) or self.nrect[6].collidepoint(self.mp) or self.nrect[7].collidepoint(self.mp) or self.nrect[8].collidepoint(self.mp)):
                self.clicka = False
            for i in range(9):
                if self.nrect[i].collidepoint(self.mp):
                    pos = i
                    if not self.mr:
                        self.clicka = True; self.clicka2 = True
                    break
            #update table simultaneously blit symbols
            for i, n in zip(range(9), self.note):
                #button system 😩 allow click verify
                if (self.mr and self.clicka and self.clicka2) and i == pos:
                    #check if theres already a symbol/b3
                    if n == None or (self.lifespan[i] == 1 and (self.b3.index == 1 or self.b3.index == 2)):
                        self.clicka2 = False
                        self.b6.open = False #menu close
                        #symbols lifespan manage
                        self.lsminus()
                        #crucial utilization of self.turn
                        self.note[i] = self.t
                        #check for lined up symbols
                        self.pointset()
                        self.lifespan[i] = 6
                        self.turnswitch()
                        s1.play() #sound on click
                        self.ai = True #switch to ai's turn
                        break

            #buttons perform
            self.b4perform()
            self.b6perform()
            if self.b6.open:
                self.b1perform()
                self.b2perform()
                self.b3perform()
                self.b5perform()
                self.b7perform()

            #turn title blit
            wsr = self.ws[self.t].get_rect(); wsr.center = (250, 25)
            SCREEN.blit(self.ws[self.t], wsr)
            #symbol blit
            for r, n, l in zip(self.nrect, self.note, self.lifespan):
                if not n == None:
                    if (self.b2.index == 0 or self.b2.index == 1) and l == 1:
                        if n: SCREEN.blit(self.snought, r)
                        else: SCREEN.blit(self.scross, r)
                    else:
                        if n: SCREEN.blit(self.nought, r)
                        else: SCREEN.blit(self.cross, r)
                    if self.b2.index == 0:
                        self.nsr[l].center = r.center
                        SCREEN.blit(self.ns[l], self.nsr[l])
            #points perform
            SCREEN.blit(self.mcross, pg.Rect((10, 10), (0, 0)))
            SCREEN.blit(self.mnought, pg.Rect((460, 10), (0, 0)))
            SCREEN.blit(self.ps[0], pg.Rect((45, 15), (0, 0)))
            ps1r = self.ps[1].get_rect(); ps1r.topright = (455, 15)
            SCREEN.blit(self.ps[1], ps1r)

            #play of ai
            if self.ai and not self.b7.index == 0:
                self.t = 0 if (self.turn == self.cross) else 1
                self.aiplay()


        def lsminus(self):
            for l in range(9):
                if self.lifespan[l] != 0:
                    self.lifespan[l] -= 1
                    if self.lifespan[l] == 0:
                        self.note[l] = None

        def aiplay(self):
            #b3
            while 1:
                aip = random.randrange(0, 9)
                if self.lifespan[aip] == 1 and self.b3.index == 0:
                    continue
                if self.note[aip] == None or self.lifespan[aip] == 1:
                    break
            self.lsminus()
            self.note[aip] = self.t
            self.pointset()
            self.lifespan[aip] = 6
            self.turnswitch()
            self.ai = False

        def b1perform(self):
            SCREEN.blit(self.b1.rimage(), self.b1.rect)
            if self.pressed(self.b1.rect, self.b1.v):
                self.b1.index = self.plus(self.b1.index) #b1 image switch
                self.index = self.plus(self.index) #table image switch
                if self.b3.index == 1: self.b3.index = 2 #b3 image switch
                elif self.b3.index == 2: self.b3.index = 1
                if self.b7.index == 1: self.b7.index = 2 #b3 image switch
                elif self.b7.index == 2: self.b7.index = 1
                self.b4.index = self.plus(self.b4.index) #b4 image switch
                self.fontset(True) #font color switch

        def b2perform(self):
            SCREEN.blit(self.b2.image[0], self.b2.rect[0])
            SCREEN.blit(self.b2.image[1], self.b2.rect[1])
            SCREEN.blit(self.b2.image[2], self.b2.rect[2])
            if self.pressed(self.b2.rect[0], self.b2.v[0]): self.b2.index = 0
            elif self.pressed(self.b2.rect[1], self.b2.v[1]): self.b2.index = 1
            elif self.pressed(self.b2.rect[2], self.b2.v[2]): self.b2.index = 2

        def b3perform(self):
            SCREEN.blit(self.b3.rimage(), self.b3.rect)
            if self.pressed(self.b3.rect, self.b3.v):
                if self.b3.index == 0:
                    if self.index == 0: self.b3.index = 1
                    else: self.b3.index = 2
                else: self.b3.index = 0

        def b4perform(self):
            SCREEN.blit(self.b4.rimage(), self.b4.rect)
            if self.pressed(self.b4.rect, self.b4.v):
                self.tablereset()

        def b5perform(self):
            SCREEN.blit(self.b5.image, self.b5.rect)
            if self.pressed(self.b5.rect, self.b5.v):
                self.nps = "0"; self.cps = "0" #reset points
                self.tablereset() #reset table
                self.turnswitch() #start with current symbol
                self.pfset()
                self.b6.open = False #close menu
        
        def b6perform(self):
            SCREEN.blit(self.b6.image, self.b6.rect)
            if self.pressed(self.b6.rect, self.b6.v):
                self.b6.open = not self.b6.open

        def b7perform(self):
            SCREEN.blit(self.b7.rimage(), self.b7.rect)
            if self.pressed(self.b7.rect, self.b7.v):
                self.b7func(True)

        def b7func(self, b=False):
            if self.b7.index == 0:
                if self.index == 0: self.b7.index = 1
                else: self.b7.index = 2
            elif b and not self.b7.index == 0:
                self.b7.index = 0
            self.ai = True

        def turnswitch(self):
            if self.turn == self.nought:
                self.turn = self.cross
            else: self.turn = self.nought

        def tablereset(self):
            #true for nought and false for cross and none for empty space
            self.turnswitch()
            self.note = [None, None, None, None, None, None, None, None, None]
            self.lifespan = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.b6.open = False #menu close
        
        def pfset(self):
            self.ps = [font2.render(self.cps, True, self.fontcolor[self.fcindex]), font2.render(self.nps, True, self.fontcolor[self.fcindex])]

        def fontset(self, switch=False):
            if switch: self.fcindex = self.plus(self.fcindex) #b1
            #easy mode numbers
            self.ns = [None, font1.render("1", True, self.fontcolor[self.fcindex]), font1.render("2", True, self.fontcolor[self.fcindex]), font1.render("3", True, self.fontcolor[self.fcindex]), font1.render("4", True, self.fontcolor[self.fcindex]), font1.render("5", True, self.fontcolor[self.fcindex]), font1.render("6", True, self.fontcolor[self.fcindex])]
            self.nsr = [None, self.ns[1].get_rect(), self.ns[2].get_rect(), self.ns[3].get_rect(), self.ns[4].get_rect(), self.ns[5].get_rect(), self.ns[6].get_rect()]
            #turn indicator
            self.ws = [font2.render("CROSS", True, self.fontcolor[self.fcindex]), font2.render("NOUGHT", True, self.fontcolor[self.fcindex])]
            #points counter
            self.pfset()

        def pointset(self):
            #monster
            def verify(s):
                if (self.note[0] == s and self.note[1] == s and self.note[2] == s) or (self.note[3] == s and self.note[4] == s and self.note[5] == s) or (self.note[6] == s and self.note[7] == s and self.note[8] == s) or (self.note[0] == s and self.note[3] == s and self.note[6] == s) or (self.note[1] == s and self.note[4] == s and self.note[7] == s) or (self.note[2] == s and self.note[5] == s and self.note[8] == s) or (self.note[0] == s and self.note[4] == s and self.note[8] == s) or (self.note[2] == s and self.note[4] == s and self.note[6] == s):
                    try:
                        l1p = self.lifespan.index(1)
                        if not self.note[l1p] == s:
                            return True
                    except: return True
                return False

            if verify(1): self.nps = str(int(self.nps) + 1); s2.play()
            elif verify(0): self.cps = str(int(self.cps) + 1); s2.play()
            self.pfset()

        def pressed(self, rect=pg.Rect(0, 0, 0, 0), v=[]):
            if rect.collidepoint(self.mp):
                if not self.mr: v[0] = True
            else: v[0] = False; v[1] = False
            if self.mr and v[0]: v[1] = True
            if (not self.mr) and v[0] and v[1]:
                v[1] = False
                return True
            return False

        def plus(self, index=int, arraylen=2):
            index += 1
            if index == arraylen:
                index = 0
            return index

    ttt = game()

    #main
    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == K_SPACE:
                    ttt.tablereset()
                if event.key == K_1:
                    ttt.b7func()

        ttt.perform()

        pg.display.flip()
        CLOCK.tick(60)

while __name__ == "__main__":
    main()
    