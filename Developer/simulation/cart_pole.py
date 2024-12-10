import pygame
import math
import random
from variables import n_actions
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
# Clase del Entorno
# =============================================================================

class CartPoleEnv:
    def __init__(self):
        self.state = [0, 0, WIDTH // 2, 0, 0]  # [theta, theta_dot, x, x_dot, x_ddot]

    def step(self, action):
        force = (action / (n_actions - 1)) * 2 * MAX_FORCE - MAX_FORCE
        theta, theta_dot, x, x_dot, _ = self.state
        total_mass = MASS_CART + MASS_PENDULUM

        theta_ddot = (GRAVITY * math.sin(theta) - math.cos(theta) * (force / total_mass)) / \
                     (LENGTH * (4.0 / 3.0 - MASS_PENDULUM * math.cos(theta)**2 / total_mass))
        x_ddot = (force + MASS_PENDULUM * LENGTH * theta_dot**2 * math.sin(theta)) / total_mass

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
        theta = random.uniform(-0.05, 0.05)
        x = WIDTH // 2 + random.uniform(-10, 10)
        self.state = [theta, 0, x, 0, 0]
        return self.state

    def render(self, screen):
        screen.fill((255, 255, 255))
        theta, _, x, _, _ = self.state
        cart_x = int(x)
        pygame.draw.rect(screen, (255, 0, 0), [cart_x - CAR_WIDTH // 2, HEIGHT - CAR_HEIGHT - 50, CAR_WIDTH, CAR_HEIGHT])
        pendulum_x = cart_x + LENGTH * math.sin(theta)
        pendulum_y = HEIGHT - 50 - LENGTH * math.cos(theta)
        pygame.draw.line(screen, (0, 0, 0), (cart_x, HEIGHT - 50), (pendulum_x, pendulum_y), 2)
        pygame.draw.circle(screen, (0, 0, 0), (int(pendulum_x), int(pendulum_y)), PENDULUM_RADIUS)
        pygame.display.update()
        pygame.time.delay(20)