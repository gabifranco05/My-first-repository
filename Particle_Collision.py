import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def ball_collision(ball1_pos, ball2_pos, radius) -> bool: #função que verifica as condições para a colisão entre partículas
    if abs(ball1_pos - ball2_pos) < 2*radius:
        return True
    
def wall_collision(ball_pos, radius, box_size) -> bool: #função que verifica as condições para a colisão entre partícula e parede
    if ball_pos - radius < 0 or ball_pos + radius > box_size:
        return True


def simulate_collision(initial_pos1, initial_pos2, initial_velocity1, initial_velocity2, mass1, mass2, num_frames, box_size):
    ball1_x = [initial_pos1]
    ball2_x = [initial_pos2]

    ball1_velocity = initial_velocity1
    ball2_velocity = initial_velocity2

    ball1_pos = initial_pos1
    ball2_pos = initial_pos2

    radius = 0.1

    for i in range(0, num_frames):
        ball1_pos += ball1_velocity
        ball2_pos += ball2_velocity
        ball1_x.append(ball1_pos)
        ball2_x.append(ball2_pos)
        if ball_collision(ball1_pos, ball2_pos, radius):
           ball1_vel_after = ((mass1-mass2)*ball1_velocity + 2*mass2*ball2_velocity)/(mass1+mass2) # velocidade da partícula 1 após colisão
           ball2_vel_after = ((mass2-mass1)*ball2_velocity + 2*mass1*ball1_velocity)/(mass1+mass2) #     "       "     "     2  "      "
           ball1_velocity, ball2_velocity = ball1_vel_after, ball2_vel_after
        if wall_collision(ball1_pos, radius, box_size):
            ball1_velocity = - ball1_velocity
        if wall_collision(ball2_pos, radius, box_size):
            ball2_velocity = - ball2_velocity

    create_animation(ball1_x, ball2_x, box_size)
        
               
def create_animation(positions1, positions2, box_size):
    num_frames = len(positions1)

    fig, ax = plt.subplots()
    ax.set_xlim(0, box_size)
    ax.set_ylim(-0.1, 0.1)
    
    ball1, = ax.plot(positions1[0], 0, 'bo', markersize = 10)
    ball2, = ax.plot(positions2[0], 0, 'ro', markersize = 10)

    def update(frame):
        ball1.set_xdata(positions1[frame])
        ball2.set_xdata(positions2[frame])
        return ball1, ball2
    
    ani = FuncAnimation(fig, update, frames = num_frames, blit = True)
    plt.show()

    plt.close(fig)

initial_pos1 = 1
initial_pos2 = 4
initial_velocity1 = 0.2
initial_velocity2 = - 0.2
mass1 = 1.0
mass2 = 1.5
num_frames = 500
box_size = 5

simulate_collision(initial_pos1, initial_pos2, initial_velocity1, initial_velocity2, mass1, mass2, num_frames, box_size)