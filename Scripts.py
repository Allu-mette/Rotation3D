import numpy as np
import pygame

class Sphere:
    def __init__(self):
        self.pos = []
        self.center = [0, 0, 0]
        for z in np.linspace(-1, 1, 20):
            for i in range(40):
                x = np.sqrt(1-z*z)*np.cos(i*2*np.pi/40)
                y = np.sqrt(1-z*z)*np.sin(i*2*np.pi/40)

                self.pos.append([x, y, z])
        
        self.xTheta = np.pi/300
        self.yTheta = np.pi/300
        self.zTheta = np.pi/600

    def update(self):

        self.pos = Rx(self.xTheta, self.pos)
        self.pos = Ry(self.yTheta, self.pos)
        self.pos = Rz(self.zTheta, self.pos)

    def display(self, screen, ref, base, dir, fov, width, height):
        display(self.pos, screen, ref, base, dir, fov, width, height)

class Ground:

    def __init__(self):
        self.pos = []
        self.N = 20
        for i in range(self.N):
            for j in range(self.N):
                self.pos.append([i-10, j-10, 0])

    def display(self, screen, ref, base, dir, fov, width, height):
        display(self.pos, screen, ref, base, dir, fov, width, height)


def display(pos, screen, ref, base, dir, fov, width, height):

    for p in pos:
        v = []
        v.append(p[0]-ref[0])
        v.append(p[1]-ref[1])
        v.append(p[2]-ref[2])
        xx = dotProduct(v, base[0])
        yy = dotProduct(v, base[1])
        zz = dotProduct(v, dir)
        d = 1/(np.tan(fov/2))
        rat = width/height

        xp = d*xx/zz
        yp = d*yy/zz
        xp /= rat

        xp = (xp+1)*width/2
        yp = (yp+1)*height/2
        if dotProduct(v, dir) > 0:
            pygame.draw.circle(screen, (255, 255, 255), [xp, yp], 2)


def Rx(theta, pos):
    R = []
    R.append([1, 0, 0])
    R.append([0, np.cos(theta), np.sin(theta)])
    R.append([0, -np.sin(theta), np.cos(theta)])

    P = []
    for p in pos:
        P.append(MatriceCal(R, p))

    return P

def Ry(theta, pos):
    R = []
    R.append([np.cos(theta), 0, np.sin(theta)])
    R.append([0, 1, 0])
    R.append([-np.sin(theta), 0, np.cos(theta)])

    P = []
    for p in pos:
        P.append(MatriceCal(R, p))

    return P

def Rz(theta, pos):
    R = []
    R.append([np.cos(theta), np.sin(theta), 0])
    R.append([-np.sin(theta), np.cos(theta), 0])
    R.append([0, 0, 1])

    P = []
    for p in pos:
        P.append(MatriceCal(R, p))

    return P

def MatriceCal(M, pos):
    P = []
    for m in M:
        s = 0
        for i in range(len(m)):
            s += pos[i]*m[i]
        P.append(s)

    return P

def dotProduct(v1, v2):
    d = 0
    for i in range(len(v1)):
        d += v1[i] * v2[i]
    return d