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

def select_action(state, epsilon, q_table):
    """Selecciona una acción utilizando la estrategia epsilon-greedy.

    Args:
        state (list): El estado actual del entorno.
        epsilon (float): La probabilidad de exploración.
        q_table (numpy.ndarray): La tabla Q.

    Returns:
        int: El índice de la acción seleccionada.
    """
    discrete_state = discretize_state(state, n_states)
    if random.uniform(0, 1) < epsilon:
        return random.randrange(n_actions)  # Exploración
    else:
        return np.argmax(q_table[discrete_state])  # Explotación


# =============================================================================
# Hiperparámetros y Entrenamiento
# =============================================================================

# Número de episodios de entrenamiento.  Aumentar puede mejorar el aprendizaje, pero toma más tiempo.
episodes = 40000
# Factor de descuento.  Controla la importancia de las recompensas futuras (cercano a 1 valora más el futuro).
gamma = 0.99
# Probabilidad inicial de exploración (epsilon-greedy).  Empieza explorando completamente.
epsilon = 1.0
# Factor de decaimiento de epsilon.  Controla la velocidad a la que disminuye la exploración.  Cerca de 1 decae lentamente.
epsilon_decay = 0.995
# Probabilidad mínima de exploración.  Se deja algo de exploración siempre.
epsilon_min = 0.01
# Tasa de aprendizaje.  Controla la velocidad de actualización de la tabla Q.  Muy alto puede ser inestable, muy bajo lento.
learning_rate = 0.1
# Número de estados discretos por dimensión.  Afecta a la granularidad de la discretización y al tamaño de la tabla Q.
n_states = 8
# Número de acciones posibles (izquierda, quieto, derecha).
n_actions = 3

# Tabla Q: Inicializada con ceros.
q_table = np.zeros((n_states, n_states, n_states,
                   n_states, n_states, n_actions))

env = CartPoleEnv()     # Crea una instancia del entorno.
# Lista para almacenar las recompensas totales por episodio.
total_rewards = []

# =============================================================================
# Entrenamiento
# =============================================================================

episode_durations = []  # Lista para almacenar las duraciones de los episodios.

for episode in range(episodes):
    """Bucle principal de entrenamiento."""
    state = env.reset()             # Reinicia el entorno al comienzo de cada episodio.
    # Bandera que indica si el episodio ha terminado.
    done = False
    total_reward = 0               # Acumula la recompensa total del episodio.
    duration = 0  # Contador de duración del episodio

    while not done:
        """Bucle que itera hasta que el episodio termina."""
        for event in pygame.event.get():
            """Gestiona los eventos de Pygame (cierre de ventana)."""
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Selecciona una acción usando la política epsilon-greedy.
        action = select_action(state, epsilon, q_table)
        # Realiza la acción en el entorno y obtiene el nuevo estado, recompensa y bandera de fin.
        next_state, reward, done = env.step(action)
        # Renderiza el estado actual en la pantalla.
        #env.render(next_state)

        # Discretiza el estado actual.
        discrete_state = discretize_state(state, n_states)
        # Discretiza el nuevo estado.
        next_discrete_state = discretize_state(next_state, n_states)

        # Calcula el objetivo de aprendizaje temporal (TD target).
        td_target = reward + gamma * \
            np.max(q_table[next_discrete_state]) if not done else reward
        # Actualiza la tabla Q usando la regla de aprendizaje Q-learning.
        q_table[discrete_state + (action,)] += learning_rate * \
            (td_target - q_table[discrete_state + (action,)])

        state = next_state             # Actualiza el estado actual.
        total_reward += reward        # Acumula la recompensa.
        duration += 1  # Incrementa la duración del episodio.

    # Guarda la recompensa total del episodio.
    total_rewards.append(total_reward)
    episode_durations.append(duration)

    if epsilon > epsilon_min:
        # Disminuye gradualmente la probabilidad de exploración (epsilon).
        epsilon *= epsilon_decay

    # Imprime información del episodio.
    print(
        f"Episodio: {episode + 1}/{episodes}, Recompensa: {total_reward:.2f}, Duración: {duration}, Epsilon: {epsilon:.4f}")
    
# =============================================================================
# Preparación para guardar gráficos
# =============================================================================
output_folder = "graphs"
os.makedirs(output_folder, exist_ok=True)  # Crea la carpeta si no existe.

# =============================================================================
# Gráfica de Resultados
# =============================================================================

# Recompensa Total por Episodio
plt.figure(figsize=(12, 5))
plt.plot(range(episodes), total_rewards, label="Recompensa Total")
plt.xlabel("Episodio")
plt.ylabel("Recompensa")
plt.title("Recompensa Total por Episodio")
plt.legend()
plt.grid()
plt.savefig(os.path.join(output_folder, "recompensa_total.png"))
plt.show()

# Curva de Aprendizaje (Recompensa Promedio)
window_size = 50  # Tamaño de la ventana para el promedio móvil.
avg_rewards = np.convolve(total_rewards, np.ones(
    window_size) / window_size, mode="valid")

plt.figure(figsize=(12, 5))
plt.plot(range(len(avg_rewards)), avg_rewards, label="Recompensa Promedio")
plt.xlabel("Episodio")
plt.ylabel("Recompensa Promedio")
plt.title("Curva de Aprendizaje")
plt.legend()
plt.grid()
plt.savefig(os.path.join(output_folder, "curva_aprendizaje.png"))
plt.show()

# Curva de Explotación vs Exploración (Epsilon)
epsilons = [1.0 * (epsilon_decay ** i) for i in range(episodes)]
epsilons = [max(epsilon, epsilon_min) for epsilon in epsilons]

plt.figure(figsize=(12, 5))
plt.plot(range(episodes), epsilons, label="Epsilon (Exploración)")
plt.xlabel("Episodio")
plt.ylabel("Epsilon")
plt.title("Curva de Explotación vs Exploración")
plt.legend()
plt.grid()
plt.savefig(os.path.join(output_folder, "exploracion_vs_explotacion.png"))
plt.show()

# Duración de los Episodios
plt.figure(figsize=(12, 5))
plt.plot(range(episodes), episode_durations, label="Duración del Episodio")
plt.xlabel("Episodio")
plt.ylabel("Duración (pasos)")
plt.title("Duración de los Episodios")
plt.legend()
plt.grid()
plt.savefig(os.path.join(output_folder, "duracion_episodios.png"))
plt.show()

# =============================================================================
# Simulación Real
# =============================================================================

# Reiniciar el entorno para la simulación.
state = env.reset()
done = False
simulated_rewards = 0

# Inicializar lista para guardar la duración de los episodios.
episode_duration = []

# Simulación en tiempo real
while not done:
    """Simulación del péndulo controlado tras entrenamiento."""
    for event in pygame.event.get():
        """Gestionar eventos de Pygame (cierre de ventana)."""
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Selecciona la acción basándose en la tabla Q aprendida (explotación pura).
    discrete_state = discretize_state(state, n_states)
    action = np.argmax(q_table[discrete_state])

    # Avanza un paso en el entorno.
    next_state, reward, done = env.step(action)

    # Renderiza el entorno en tiempo real.
    env.render(state)

    state = next_state  # Actualiza el estado actual.
    simulated_rewards += reward  # Acumula la recompensa.

print(
    f"Recompensa total obtenida en la simulación real: {simulated_rewards:.2f}")

pygame.quit()