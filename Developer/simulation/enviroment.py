# environment.py

import numpy as np
from config import *


class CartPoleEnv:
    def __init__(self):
        self.x = 0.0          # Posición del carrito
        self.x_dot = 0.0      # Velocidad del carrito
        self.theta = 0.0      # Ángulo del péndulo
        self.theta_dot = 0.0  # Velocidad angular del péndulo
        self.done = False     # Estado terminal
        self.time = 0         # Tiempo acumulado

        # Ranges and bins for discretization
        self.x_bins = 48
        self.x_dot_bins = 21
        self.theta_bins = 48
        self.theta_dot_bins = 21

    def reset(self):
        """Restablece el entorno a un estado inicial aleatorio."""
        self.x = np.random.uniform(-0.1, 0.1)
        self.x_dot = 0.0
        self.theta = np.random.uniform(-0.05, 0.05)
        self.theta_dot = 0.0
        self.done = False
        self.time = 0
        return self.get_state()

    def discretize(self, value, bins, min_val, max_val):
        """
        Discretiza un valor continuo en índices enteros dentro del rango dado.

        Args:
            value (float): Valor continuo a discretizar.
            bins (int): Número de bins.
            min_val (float): Valor mínimo permitido.
            max_val (float): Valor máximo permitido.

        Returns:
            int: Índice entero discretizado.
        """
        # Limitar el valor al rango permitido
        value_clipped = np.clip(value, min_val, max_val)
        # Tamaño del bin
        bin_size = (max_val - min_val) / bins
        # Calcular el índice discretizado
        return int((value_clipped - min_val) // bin_size)

    def get_state(self):
        """Discretiza el espacio de observación en un estado."""
        return (
            self.discretize(self.x, self.x_bins, -X_MAX, X_MAX),
            self.discretize(self.x_dot, self.x_dot_bins, -1, 1),
            self.discretize(self.theta, self.theta_bins, -
                            THETA_MAX, THETA_MAX),
            self.discretize(self.theta_dot, self.theta_dot_bins, -1, 1)
        )

    def step(self, action):
        """Avanza un paso en el entorno basado en la acción."""
        force = 10 if action == 1 else -10

        # Ecuaciones del movimiento
        sin_theta = np.sin(self.theta)
        cos_theta = np.cos(self.theta)
        temp = (force + m * l * self.theta_dot**2 * sin_theta) / (M + m)
        theta_acc = (g * sin_theta - cos_theta * temp) / \
            (l * (4/3 - (m * cos_theta**2) / (M + m)))
        x_acc = temp - (m * l * theta_acc * cos_theta) / (M + m)

        # Actualizar el estado
        self.x += self.x_dot * DELTA_T
        self.x_dot += x_acc * DELTA_T
        self.theta += self.theta_dot * DELTA_T
        self.theta_dot += theta_acc * DELTA_T

        # Evaluar si es estado terminal
        if abs(self.x) > X_MAX or abs(self.theta) > THETA_MAX:
            self.done = True

        return self.get_state(), self.get_reward(), self.done

    def get_reward(self):
        """Calcula la recompensa."""
        if self.done:
            return -10
        # Recompensa mayor cuando el péndulo está recto
        return 1 - abs(self.theta)
