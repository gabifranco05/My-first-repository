import random
import matplotlib.pyplot as plt

class Particle:
    def __init__(self, position : int):
        self._position = position

def random_walk(num_steps, prob_right, num_particles):

    particle_paths = []

    for particle in range(num_particles + 1):

        part = Particle(position = 0)
        particle_path = [0]

        for step in range(num_steps + 1): # Verificar para cada passo da partícula o seu movimento

            rand_prob = random.uniform(0, 1) # Número aleatório entre 0 e 1 que determina se a partícula vai para a esquerda ou direita

            if rand_prob <= prob_right:
                part._position += 1
                particle_path.append(part._position)

            else:
                part._position -= 1
                particle_path.append(part._position)

        particle_paths.append(particle_path)    

    create_plot(num_steps, particle_paths)

    return particle_paths

def create_plot(num_steps, particle_paths):

    time = [x for x in range(len(particle_paths[0]))]

    for particle_path in particle_paths:
        plt.plot(particle_path, time)

    plt.title('Random Walk - N particles')
    plt.xlabel('Position')
    plt.ylabel('Time')
    plt.show()

num_steps = 100 # Number of steps
prob_right = 0.4 # Probability of moving to the right
num_particles = 50 # Number of particles

random_walk(num_steps, prob_right, num_particles)