# policies.py

import numpy as np


def epsilon_greedy(q_table, state, epsilon):
    """
    Selecciona una acción basada en la política ε-greedy.

    Args:
        q_table (numpy.ndarray): La tabla Q actual.
        state (tuple): El estado actual (discretizado).
        epsilon (float): La probabilidad de seleccionar una acción aleatoria.

    Returns:
        int: La acción seleccionada (0 o 1).
    """
    if np.random.rand() < epsilon:
        # Selección aleatoria (exploración)
        return np.random.choice(len(q_table[state]))
    else:
        # Selección basada en la tabla Q (explotación)
        return np.argmax(q_table[state])


def greedy(q_table, state):
    """
    Selecciona la mejor acción basada únicamente en la tabla Q (sin exploración).

    Args:
        q_table (numpy.ndarray): La tabla Q actual.
        state (tuple): El estado actual (discretizado).

    Returns:
        int: La acción seleccionada (0 o 1).
    """
    return np.argmax(q_table[state])


def softmax_action_selection(q_table, state, temperature=1.0):
    """
    Selecciona una acción basada en un enfoque de softmax.

    Args:
        q_table (numpy.ndarray): La tabla Q actual.
        state (tuple): El estado actual (discretizado).
        temperature (float): El parámetro de temperatura para ajustar la probabilidad.

    Returns:
        int: La acción seleccionada.
    """
    q_values = q_table[state]
    exp_values = np.exp(q_values / temperature)
    probabilities = exp_values / np.sum(exp_values)
    return np.random.choice(len(q_values), p=probabilities)
