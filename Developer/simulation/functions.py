import numpy as np
import math
import random
from cart_pole import WIDTH
from variables import n_states, n_actions


def discretize_state(state, n_states):
    """
    Discretiza un estado continuo en un estado discreto.

    Args:
        state (list): El estado continuo del entorno (theta, theta_dot, x, x_dot, x_ddot).
        n_states (int): El número de estados discretos por dimensión.

    Returns:
        tuple: El estado discreto como una tupla de índices.
    """
    # Define los límites de los bins para cada componente del estado.
    state_bins = [
        np.linspace(-math.pi / 2, math.pi / 2, n_states),  # theta (ángulo)
        np.linspace(-2, 2, n_states),  # theta_dot (velocidad angular)
        np.linspace(0, WIDTH, n_states),  # x (posición del carro)
        np.linspace(-5, 5, n_states),  # x_dot (velocidad del carro)
        np.linspace(-10, 10, n_states)  # x_ddot (aceleración del carro)
    ]
    # Determina el índice del bin al que pertenece cada componente del estado.
    indices = [np.digitize(s, bins) - 1 for s, bins in zip(state, state_bins)]
    # Devuelve el estado discreto como una tupla.  Se resta 1 para que los índices comiencen en 0.
    return tuple(indices)


def select_action(state, epsilon, q_table):
    """
    Selecciona una acción usando una política epsilon-greedy.

    Args:
        state (list): El estado del entorno.
        epsilon (float): La probabilidad de exploración.
        q_table (numpy.ndarray): La tabla Q.

    Returns:
        int: El índice de la acción seleccionada.
    """
    discrete_state = discretize_state(state, n_states)  # Discretiza el estado.
    # Se genera un número aleatorio para decidir entre exploración y explotación.
    if random.uniform(0, 1) < epsilon:
        # Selecciona una acción aleatoria (exploración).
        return random.randrange(n_actions)
    else:
        # Selecciona la acción con el valor Q máximo (explotación).
        return np.argmax(q_table[discrete_state])
