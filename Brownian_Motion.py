import pygame
import sys
import random
from math import sqrt, pi, sin, cos, atan, atan2

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

def elastic_collision(v1i, v2i, theta1, theta2):
    # Calculate relative velocity components
    v_rel_x = v1i * cos(theta1) - v2i * cos(theta2)
    v_rel_y = v1i * sin(theta1) - v2i * sin(theta2)

    # Calculate final velocities after collision
    v1f = v2i + 2 * (v_rel_x * cos(theta2) + v_rel_y * sin(theta2))
    v2f = v1i + 2 * (v_rel_x * cos(theta1) + v_rel_y * sin(theta1))

    # Calculate final angles after collision
    phi1 = atan2(v1f * sin(theta1) + v2f * sin(theta2), v1f * cos(theta1) + v2f * cos(theta2))
    phi2 = atan2(v1f * sin(theta1) + v2f * sin(theta2), v1f * cos(theta1) + v2f * cos(theta2))

    return v1f, v2f, phi1, phi2

#Particle Class
class Particle:
    def __init__(self, x, y, is_tracer = False):
        self.x = x
        self.y = y
        self.radius = PARTICLE_RADIUS
        
        self.color = RED
        self.speed = random.uniform(0, MAX_SPEED)
        self.angle = random.uniform(-2*pi, 2*pi)
        self.is_tracer = is_tracer
        self.path = []

    def move(self):
        return

    
    def check_collision(self, other_particle):
        if sqrt((self.y - other_particle.y)**2 + (self.x - other_particle.x)**2) <= 2*PARTICLE_RADIUS:
            return True
        else:
            return False
        
    def check_wall_collision(self):
        if (self.x + self.radius) >= WIDTH or (self.x - self.radius) <= 0:
            return True
        else:
            return False 
        
    def check_floor_roof_collision(self):
        if (self.y + self.radius) >= HEIGHT or (self.y - self.radius) <= 0:
            return True
        else:
            return False 
        

    
#Create particles
particles = [Particle(x = random.uniform(0 ,800), y = random.uniform(0, 600), is_tracer = False) for i in range(NUM_PARTICLES)]

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