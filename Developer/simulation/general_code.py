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
