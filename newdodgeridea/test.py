import pygame as pg
import sys

pg.init()

screen = pg.display.set_mode((500, 500))
clock = pg.time.Clock()

rgb = [0, 0, 0]

test = pg.Color(0, 0, 0)

changec = pg.USEREVENT + 0
pg.time.set_timer(changec, 100)

while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if rgb != [255, 255, 255]:
            if event.type == changec:
                rgb[0] += 1
                rgb[1] += 1
                rgb[2] += 1

    screen.fill(rgb)

    pg.display.flip()
    clock.tick(60)