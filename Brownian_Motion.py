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

def elastic_collision(v1i, v2i, theta1, theta2): ### Devolve as velocidades e ângulos finais numa colisão de partículas
    # Calculate relative velocity components
    v_rel_x = v1i * cos(theta1) - v2i * cos(theta2)
    v_rel_y = v1i * sin(theta1) - v2i * sin(theta2)

    # Calculate final velocities after collision
    v1f_rel_x = (v1i - v2i) * cos(theta1 - theta2)
    v1f_rel_y = (v1i - v2i) * sin(theta1 - theta2)

    v2f_rel_x = (v2i - v1i) * cos(theta2 - theta1)
    v2f_rel_y = (v2i - v1i) * sin(theta2 - theta1)

    # Calculate final velocities in the absolute frame
    v1f_x = v_rel_x + v1f_rel_x
    v1f_y = v_rel_y + v1f_rel_y

    v2f_x = v_rel_x + v2f_rel_x
    v2f_y = v_rel_y + v2f_rel_y

    # Calculate final angles after collision
    phi1 = atan2(v1f_y, v1f_x)
    phi2 = atan2(v2f_y, v2f_x)

    # Calculate final speeds
    v1f = sqrt(v1f_x**2 + v1f_y**2)
    v2f = sqrt(v2f_x**2 + v2f_y**2)

    return [v1f, v2f, phi1, phi2]

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
            self.x += self.speed*cos(self.angle)
            self.y += self.speed*sin(self.angle)
            self.path.append((self.x, self.y))
                                

        if self.check_floor_roof_collision():
            self.angle = - self.angle
            if self.y >= HEIGHT/2:
                self.y = HEIGHT - self.radius
            else:
                self.y = self.radius
            self.x += self.speed*cos(self.angle)
            self.y += self.speed*sin(self.angle)
            self.path.append((self.x, self.y))

        for other_particle_index in self.square_tribution.values():
            if other_particle_index is not None:
                other_particle = particles[other_particle_index]
                if self.check_collision(other_particle):
                    # Perform elastic collision
                    self.speed, other_particle.speed = other_particle.speed, self.speed
                    self.angle, other_particle.angle = other_particle.angle, self.angle
                    self.x += self.speed*cos(self.angle)
                    self.y += self.speed*sin(self.angle)
                    self.path.append((self.x, self.y))
                    break



        

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

    def attribute_square(self):
        self.square_tribution = {}
        for i in (self.y - self.radius, self.y + self.radius):
            for j in (self.x - self.radius, self.x + self.radius):
                square = (i // 40, j // 40)
                if self.square_tribution.get(square) is None:
                    self.square_tribution[square] = particles.index(self)


    def check_square(self, square_map):
        for square, particle_index in self.square_tribution.items():
            if particle_index is not None and square in square_map:
                particle1 = particles[particle_index]
                for other_particle_index in square_map[square]:
                    if particle_index != other_particle_index:
                        particle2 = particles[other_particle_index]
                        particle1.check_collision(particle2)   

#Create particles
particles = [Particle(x = random.uniform(0, WIDTH), y = random.uniform(0, HEIGHT), is_tracer = False) for i in range(NUM_PARTICLES)]

square_map = {}
for p in particles:
    for i in (p.y - p.radius, p.y + p.radius):
        for j in (p.x - p.radius, p.x + p.radius):
            square = (i // 40, j // 40)
            if square not in square_map:
                square_map[square] = []
            square_map[square].append(particles.index(p))

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