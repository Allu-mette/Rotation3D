import pygame
import numpy as np
import Scripts

class Simu():

    def __init__(self, width, height):

        self.running = True
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('3DRotation')
        self.clock = pygame.time.Clock()

        self.sphere = Scripts.Sphere()
        self.ground = Scripts.Ground()
        self.theta = 0
        self.rho = 0
        self.pos = [0,0,0]
        self.projBase = [[0,1,0], [0,0,1]]
        self.dir = [1,0,0]
        self.fov = np.pi/4
        pygame.mouse.set_visible(False)


    def events(self):

        for event in pygame.event.get():
                # Quit
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        keys = pygame.key.get_pressed()
        # Set the Position
        v1 = 0
        v2 = 0
        if keys[pygame.K_a]:
            self.pos[2] += .05
        elif keys[pygame.K_SPACE]:
            self.pos[2] -= .05
        elif keys[pygame.K_UP] or keys[pygame.K_z]:
            v1 += .05
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            v1 -= .05
        elif keys[pygame.K_LEFT] or keys[pygame.K_q]:
            v2 += .05
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            v2 -= .05
        self.pos[0] += np.cos(self.theta) * v1
        self.pos[1] += np.sin(self.theta) * v1
        self.pos[0] += np.cos(self.theta-np.pi/2) * v2
        self.pos[1] += np.sin(self.theta-np.pi/2) * v2

    def update(self):
        X = pygame.mouse.get_pos()
        self.theta += (X[0]-self.width/2)/300
        self.rho += (X[1]-self.height/2)/300
        self.projBase[0][0] = np.cos(self.theta+np.pi/2)
        self.projBase[0][1] = np.sin(self.theta+np.pi/2)
        self.projBase[1][0] = np.cos(self.theta)*np.cos(self.rho+np.pi/2)
        self.projBase[1][1] = np.sin(self.theta)*np.cos(self.rho+np.pi/2)
        self.projBase[1][2] = np.sin(self.rho+np.pi/2)
        self.dir = [np.cos(self.theta)*np.cos(self.rho),
                    np.sin(self.theta)*np.cos(self.rho),
                    np.sin(self.rho)]

        pygame.mouse.set_pos([self.width/2,self.height/2])
        self.sphere.update()
        
    def display(self):
        self.screen.fill('black')
        self.sphere.display(self.screen, self.pos, self.projBase, self.dir, self.fov, self.width, self.height)
        self.ground.display(self.screen, self.pos, self.projBase, self.dir, self.fov, self.width, self.height)
        pygame.display.flip()

    def run(self):
        while(self.running):
            self.events()
            self.update()
            self.display()
            self.clock.tick(60)

pygame.init()

Simu = Simu(1080, 720)
Simu.run()

pygame.quit()