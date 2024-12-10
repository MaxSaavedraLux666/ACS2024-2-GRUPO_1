import numpy as np
import math
import random
from cart_pole import WIDTH
from variables import n_states,n_actions

def discretize_state(state, n_states):
    state_bins = [
        np.linspace(-math.pi / 2, math.pi / 2, n_states),  # theta
        np.linspace(-2, 2, n_states),  # theta_dot
        np.linspace(0, WIDTH, n_states),  # x
        np.linspace(-5, 5, n_states),  # x_dot
        np.linspace(-10, 10, n_states)  # x_ddot
    ]
    indices = [np.digitize(s, bins) - 1 for s, bins in zip(state, state_bins)]
    return tuple(indices)

def select_action(state, epsilon, q_table):
    discrete_state = discretize_state(state, n_states)
    if random.uniform(0, 1) < epsilon:
        return random.randrange(n_actions)  # Exploración
    else:
        return np.argmax(q_table[discrete_state])  # Explotación