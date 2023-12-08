import pygame
import sys
import random
from math import sqrt

pygame.init()

#Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PARTICLE_RADIUS = 10
NUM_PARTICLES = 50
MAX_SPEED = 2

#Colors
WHITE = (255, 255, 255)
RED = (255, 0 , 0)
BLUE = (0, 0, 255)

#Particle Class
class Particle:
    def __init__(self, x, y, is_tracer = False):
        self.x = x
        self.y = y
        self.radius
        self.color 
        self.speed 
        self.angle
        self.is_tracer
        self.path

    def move(self):
        return
    
    def check_collision(self, other_particle):
        return

    
#Create particles
particles = []

#Choose a tracer
trace_index = random.randint(0, NUM_PARTICLES - 1)

#Set up pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brownian Motion Simulation")
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #Move particle and check collision
        for particle in particles:
            particle.move()

        #Draw particles and paths
        screen.fill(WHITE)
        for particle in particles:
            pygame.draw.circle(screen, particle.color, (int(particle.x), int(particle.y)), particle.radius)

            #Draw path for the tracer
            if particle.is_tracer() and len(particle.path) >= 2:
                pygame.draw.lines(screen, particle.color, False, particle.path, 2)

        pygame.display.flip()
        clock.tick(FPS)