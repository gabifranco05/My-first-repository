import pygame
import sys
import random
from math import atan2, cos, sin, pi, sqrt

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
        self.radius = PARTICLE_RADIUS
        self.color = RED
        self.speed = random.uniform(0, MAX_SPEED)
        self.angle = random.uniform(0, 2*pi)
        self.is_tracer = is_tracer
        self.path = []

    def move(self):
        if self.check_wall_collision():
            self.angle = pi - self.angle
            if self.x >= WIDTH/2: 
                self.x = WIDTH - self.radius
            else:
                self.x = self.radius                     

        if self.check_floor_roof_collision():
            self.angle = - self.angle
            if self.y >= HEIGHT/2:
                self.y = HEIGHT - self.radius
            else:
                self.y = self.radius

        for other_particle in particles:
            if self.check_collision(other_particle):
                self.speed, other_particle.speed = other_particle.speed, self.speed
                self.angle, other_particle.angle = other_particle.angle, self.angle
                self.x += self.speed*cos(self.angle)
                self.y += self.speed*sin(self.angle)

        self.x += self.speed*cos(self.angle)
        self.y += self.speed*sin(self.angle)
        self.path.append((self.x, self.y))

    def check_collision(self, other_particle):  ### Verifica se duas partículas colidem
        if sqrt((self.y - other_particle.y)**2 + (self.x - other_particle.x)**2) <= 2*PARTICLE_RADIUS:
            return True
        else:
            return False
        
    def check_wall_collision(self):  ### Verifica se a partícula colide com as paredes
        if (self.x + self.radius) >= WIDTH or (self.x - self.radius) <= 0:
            return True
        else:
            return False 
        
    def check_floor_roof_collision(self):  ### Verifica se a partícula colide com o chão ou o teto
        if (self.y + self.radius) >= HEIGHT or (self.y - self.radius) <= 0:
            return True
        else:
            return False    

#Create particles
particles = [Particle(x = random.uniform(0, WIDTH), y = random.uniform(0, HEIGHT), is_tracer = False) for i in range(NUM_PARTICLES)]

#Choose a tracer
trace_index = random.randint(0, NUM_PARTICLES - 1)
particles[trace_index].color = BLUE
particles[trace_index].is_tracer = True

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
            if particle.is_tracer and len(particle.path) >= 2:
                pygame.draw.lines(screen, particle.color, False, particle.path, 2)

        pygame.display.flip()
        clock.tick(FPS)