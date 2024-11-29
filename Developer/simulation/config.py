# config.py

# Parámetros físicos
M = 1.0    # Masa del carrito (kg)
m = 0.1    # Masa del péndulo (kg)
l = 0.5    # Longitud de la varilla (m)
g = 9.8    # Gravedad (m/s^2)

# Parámetros del entorno
X_MAX = 2.4  # Rango de movimiento del carrito (m)
THETA_MAX = 0.21  # Ángulo máximo permisible (rad) ~ 12 grados
DELTA_T = 0.02  # Tiempo de actualización (s)

# Parámetros de aprendizaje
ALPHA = 0.05    # Tasa de aprendizaje
GAMMA = 0.9   # Factor de descuento
EPSILON = 1.0  # Valor inicial de epsilon (para ε-greedy)
EPSILON_DECAY = 0.99  # Decadencia de epsilon
MIN_EPSILON = 0.01  # Valor mínimo de epsilon
EPISODES = 2000  # Número de episodios de entrenamiento
