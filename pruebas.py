import numpy as np, pygame as py, sys
x0=3
v0=2
h=0.01
def transformacion(coord):
    coord=np.array(coord)*50
    coord[0] = 500+coord[0]
    coord[1] = 350-coord[1]
    return coord
def v(x,y):
    return np.array([x,y])

def flujo(func, r0, n, t):
    r = [np.array(r0)]
    for i in range(1, t+1):
        ri = r[i-1]
        r.append(ri + func(*ri)*n)
    return np.array(r)
def X(t,n):
    x = [x0]
    v=[v0]
    for i in range(1,t+1):
        xi = x[i-1]
        vi = v[i-1]
        v.append(vi + a(vi)*n)
        x.append(xi + vi*n)
    return np.array(x)




py.init()
screen = py.display.set_mode((1000,700))
pos = flujo(v,[0.01,0.01], 0.01, 1000).transpose()*50
pos[0] =500 + pos[0]
pos[1] = 350 - pos[1]
pos = pos.transpose()
fps = 60
clock = py.time.Clock()
p = pos[0]
t=0
while True:
    t+=1
    for event in py.event.get():
        if event.type == py.QUIT:
            sys.exit()
    screen.fill('black')
    for y in range(-10, 11):
        for x in range(-10, 11):
            inicio = transformacion((x,y))
            final = transformacion(np.array([x,y])+v(x,y)/10)
            py.draw.line(screen, 'orange', inicio, final)
    p = pos[t]
    py.draw.circle(screen, 'blue', p, 10)
    py.draw.circle(screen, 'white', p, 10,1)
    py.draw.lines(screen, 'red', False, pos)
    py.display.flip()
    clock.tick(fps)