import matplotlib.pyplot as plt
import pygame
import math
import numpy as np
import random
import os


# =============================================================================
# Parámetros del Entorno
# =============================================================================

WIDTH, HEIGHT = 800, 600
FPS = 60
MASS_CART = 1.0
MASS_PENDULUM = 0.1
LENGTH = 100
GRAVITY = 9.81
TIME_STEP = 0.03
DAMPING = 0.999
PENDULUM_RADIUS = 10
CAR_WIDTH = 80
CAR_HEIGHT = 20
MAX_FORCE = 180

# Ángulo máximo para recompensa positiva (12 grados en radianes)
MAX_ANGLE_REWARD = 12 * math.pi / 180

# =============================================================================
# Inicialización de Pygame
# =============================================================================

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Péndulo Invertido con Q-Learning")
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# =============================================================================
# Clase del Entorno
# =============================================================================

class CartPoleEnv:
    def __init__(self):
        """Inicializa el entorno del péndulo invertido.

        El estado inicial se establece con el ángulo del péndulo, la velocidad angular, 
        la posición del carro, la velocidad del carro y la aceleración del carro 
        todos cerca de cero.
        """
        self.state = [0, 0, WIDTH // 2, 0,
                      0]  # [theta, theta_dot, x, x_dot, x_ddot]

    def step(self, action):
        """Avanza un paso de tiempo en la simulación.

        Args:
            action (int): La acción a realizar (0: izquierda, 1: quieto, 2: derecha).

        Returns:
            tuple: Una tupla que contiene el nuevo estado, la recompensa y un booleano 
                   que indica si el episodio ha terminado.
        """
        force = (action / (n_actions - 1)) * 2 * MAX_FORCE - MAX_FORCE
        theta, theta_dot, x, x_dot, _ = self.state
        total_mass = MASS_CART + MASS_PENDULUM

        theta_ddot = (GRAVITY * math.sin(theta) - math.cos(theta) * (force / total_mass)) / \
                     (LENGTH * (4.0 / 3.0 - MASS_PENDULUM *
                      math.cos(theta)**2 / total_mass))
        x_ddot = (force + MASS_PENDULUM * LENGTH *
                  theta_dot**2 * math.sin(theta)) / total_mass

        theta_dot += theta_ddot * TIME_STEP
        theta += theta_dot * TIME_STEP
        x_dot += x_ddot * TIME_STEP
        x += x_dot * TIME_STEP

        theta_dot *= DAMPING
        x_dot *= DAMPING
        self.state = [theta, theta_dot, x, x_dot, x_ddot]

        done = abs(theta) > math.pi / 2 or x < 0 or x > WIDTH

        angle_reward = 1.0 if abs(theta) <= MAX_ANGLE_REWARD else max(
            0, 1.0 - (abs(theta) - MAX_ANGLE_REWARD) / (math.pi / 2 - MAX_ANGLE_REWARD))
        reward = angle_reward - 0.01 * abs(x - WIDTH / 2) / WIDTH

        return self.state, reward, done

    def reset(self):
        """Reinicia el entorno a un estado aleatorio."""
        theta = random.uniform(-0.05, 0.05)
        x = WIDTH // 2 + random.uniform(-10, 10)
        self.state = [theta, 0, x, 0, 0]
        return self.state

    def render(self, state):
        """Renderiza el estado actual del entorno en la pantalla."""
        theta, _, x, _, _ = state
        screen.fill(WHITE)
        cart_x = int(x)
        pygame.draw.rect(screen, RED, [
                         cart_x - CAR_WIDTH // 2, HEIGHT - CAR_HEIGHT - 50, CAR_WIDTH, CAR_HEIGHT])
        pendulum_x = cart_x + LENGTH * math.sin(theta)
        pendulum_y = HEIGHT - 50 - LENGTH * math.cos(theta)
        pygame.draw.line(screen, BLACK, (cart_x, HEIGHT - 50),
                         (pendulum_x, pendulum_y), 2)
        pygame.draw.circle(screen, BLACK, (int(pendulum_x),
                           int(pendulum_y)), PENDULUM_RADIUS)
        pygame.display.update()
        pygame.time.delay(20)

# =============================================================================
# Funciones Auxiliares
# =============================================================================

def discretize_state(state, n_states):
    """Discretiza un estado continuo en un estado discreto.

    Divide el espacio de estados continuo en n_states intervalos para cada dimensión.

    Args:
        state (list): El estado continuo del entorno (theta, theta_dot, x, x_dot, x_ddot).
        n_states (int): El número de estados discretos por dimensión.

    Returns:
        tuple: Un índice discreto que representa el estado.
    """
    state_bins = [
        np.linspace(-math.pi / 2, math.pi / 2, n_states),  # theta
        np.linspace(-2, 2, n_states),  # theta_dot
        np.linspace(0, WIDTH, n_states),  # x
        np.linspace(-5, 5, n_states),  # x_dot
        np.linspace(-10, 10, n_states)  # x_ddot
    ]
    indices = [np.digitize(s, bins) - 1 for s, bins in zip(state, state_bins)]
    return tuple(indices)
