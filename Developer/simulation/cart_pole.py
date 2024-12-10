import pygame
import math
import random
from variables import n_actions

# =============================================================================
# Parámetros del Entorno: Definición de constantes que configuran el entorno de simulación.
# =============================================================================

WIDTH, HEIGHT = 800, 600  # Dimensiones de la ventana de visualización (ancho, alto) en píxeles.
FPS = 60  # Número de fotogramas por segundo para la simulación.
MASS_CART = 1.0  # Masa del carro en kg.
MASS_PENDULUM = 0.1  # Masa del péndulo en kg.
LENGTH = 100  # Longitud del péndulo en píxeles.
GRAVITY = 9.81  # Aceleración debida a la gravedad en m/s².
TIME_STEP = 0.03  # Paso de tiempo de la simulación en segundos.
DAMPING = 0.999  # Factor de amortiguamiento para la velocidad del carro y el péndulo.
PENDULUM_RADIUS = 10  # Radio del círculo que representa el péndulo en píxeles.
CAR_WIDTH = 80  # Ancho del rectángulo que representa el carro en píxeles.
CAR_HEIGHT = 20  # Alto del rectángulo que representa el carro en píxeles.
MAX_FORCE = 180  # Fuerza máxima que se puede aplicar al carro.

# Ángulo máximo para recompensa positiva (12 grados en radianes):  Umbral para considerar el ángulo como "estable" y otorgar recompensa máxima.
MAX_ANGLE_REWARD = 12 * math.pi / 180

# =============================================================================
# Clase del Entorno: Define la dinámica del entorno de simulación del péndulo invertido.
# =============================================================================

class CartPoleEnv:
    def __init__(self):
        # Inicializa el estado del sistema.  El estado incluye: ángulo, velocidad angular, posición x, velocidad x, aceleración x.
        self.state = [0, 0, WIDTH // 2, 0, 0]  # [theta, theta_dot, x, x_dot, x_ddot]

    def step(self, action):
        # Aplica una fuerza al carro según la acción elegida por el agente.
        force = (action / (n_actions - 1)) * 2 * MAX_FORCE - MAX_FORCE # Mapea la acción discreta a una fuerza continua.
        theta, theta_dot, x, x_dot, _ = self.state # Desempaqueta el estado actual.
        total_mass = MASS_CART + MASS_PENDULUM # Masa total del sistema.

        # Calcula la aceleración angular y lineal usando las ecuaciones de movimiento del péndulo invertido.
        theta_ddot = (GRAVITY * math.sin(theta) - math.cos(theta) * (force / total_mass)) / \
                     (LENGTH * (4.0 / 3.0 - MASS_PENDULUM * math.cos(theta)**2 / total_mass))
        x_ddot = (force + MASS_PENDULUM * LENGTH * theta_dot**2 * math.sin(theta)) / total_mass

        # Actualiza el estado del sistema usando el método de Euler.
        theta_dot += theta_ddot * TIME_STEP
        theta += theta_dot * TIME_STEP
        x_dot += x_ddot * TIME_STEP
        x += x_dot * TIME_STEP

        # Aplica amortiguamiento a las velocidades.
        theta_dot *= DAMPING
        x_dot *= DAMPING
        self.state = [theta, theta_dot, x, x_dot, x_ddot] # Actualiza el estado del sistema.

        # Determina si el episodio ha terminado (el péndulo cae o el carro sale de los límites).
        done = abs(theta) > math.pi / 2 or x < 0 or x > WIDTH

        # Calcula la recompensa basándose en el ángulo del péndulo y la posición del carro.
        angle_reward = 1.0 if abs(theta) <= MAX_ANGLE_REWARD else max(
            0, 1.0 - (abs(theta) - MAX_ANGLE_REWARD) / (math.pi / 2 - MAX_ANGLE_REWARD))
        reward = angle_reward - 0.01 * abs(x - WIDTH / 2) / WIDTH # Recompensa basada en ángulo y posición del carro.

        return self.state, reward, done # Devuelve el nuevo estado, la recompensa y si el episodio ha terminado.

    def reset(self):
        # Reinicia el entorno a un estado aleatorio.
        theta = random.uniform(-0.05, 0.05) # Ángulo inicial aleatorio cercano a la vertical.
        x = WIDTH // 2 + random.uniform(-10, 10) # Posición inicial aleatoria cercana al centro.
        self.state = [theta, 0, x, 0, 0] # Reinicia el estado del sistema.
        return self.state

    def render(self, screen):
        # Dibuja el entorno en la pantalla usando Pygame.
        screen.fill((255, 255, 255)) # Llena la pantalla con blanco.
        theta, _, x, _, _ = self.state # Desempaqueta el estado actual.
        cart_x = int(x) # Convierte la posición x a un entero para Pygame.
        pygame.draw.rect(screen, (255, 0, 0), [cart_x - CAR_WIDTH // 2, HEIGHT - CAR_HEIGHT - 50, CAR_WIDTH, CAR_HEIGHT]) # Dibuja el carro.
        pendulum_x = cart_x + LENGTH * math.sin(theta) # Calcula la posición x del péndulo.
        pendulum_y = HEIGHT - 50 - LENGTH * math.cos(theta) # Calcula la posición y del péndulo.
        pygame.draw.line(screen, (0, 0, 0), (cart_x, HEIGHT - 50), (pendulum_x, pendulum_y), 2) # Dibuja el péndulo.
        pygame.draw.circle(screen, (0, 0, 0), (int(pendulum_x), int(pendulum_y)), PENDULUM_RADIUS) # Dibuja el círculo en el extremo del péndulo.
        pygame.display.update() # Actualiza la pantalla.
        pygame.time.delay(20) # Introduce un pequeño retraso.