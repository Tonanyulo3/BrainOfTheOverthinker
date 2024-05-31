class pos():
    def __init__(self, x, y):
        self.x = x
        self.y = y

a = pos(-145, 60)
b = pos(800, 410)
c = pos(-a.x+b.x, -a.y+b.y)

pepe = "x" if abs(c.y) > abs(c.x) else "y"

si = 0
no = 0

e = min(abs(c.x), abs(c.y))
diff = abs(abs(c.x) - abs(c.y))
try: si = diff/e
except: pass

while a.x != b.x or a.y != b.y:
    print(a.x, a.y)

    c.x = -a.x+b.x
    c.y = -a.y+b.y
    
    e = min(abs(c.x), abs(c.y))
    diff = abs(abs(c.x) - abs(c.y))

    try: no = diff/e
    except: pass

    if pepe == "x":
        if no <= si:
            try: a.x += int(c.x/abs(c.x))
            except: pass
        a.y += int(c.y/abs(c.y))
    elif pepe == "y":
        if no <= si:
            try: a.y += int(c.y/abs(c.y))
            except: pass
        a.x += int(c.x/abs(c.x))

print(a.x, a.y)


"""
pos(-200;0)
des(800;300)
distance(1000;300)1101110110
700/300
11010110
1010110

pos(-200;0)
des(400;500)
distance(600;500)111110
100/500
go 5 stop 1

max - min (abs)




"""
