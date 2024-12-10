import pygame
import numpy as np
from cart_pole import CartPoleEnv, WIDTH, HEIGHT
from train import train,q_table
from graphics import plot_results
from variables import epsilon,n_states
from functions import discretize_state

# Inicialización de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Péndulo Invertido con Q-Learning")

# Entrenamiento
total_rewards, episode_durations = train(epsilon)

# Gráficas
plot_results(total_rewards, episode_durations, len(total_rewards))


# Simulación en tiempo real
# Reiniciar el entorno para la simulación
env = CartPoleEnv()  # Asegúrate de crear una nueva instancia del entorno
state = env.reset()
done = False
simulated_rewards = 0

# Inicializar lista para guardar la duración de los episodios
episode_duration = []

# Simulación en tiempo real
while not done:
    # Gestión de eventos de Pygame (cierre de ventana)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Selecciona la acción basándose en la tabla Q aprendida (explotación pura)
    discrete_state = discretize_state(state, n_states)
    action = np.argmax(q_table[discrete_state])

    # Avanza un paso en el entorno
    next_state, reward, done = env.step(action)

    # Renderiza el entorno en tiempo real
    env.render(screen)  # Asegúrate de pasar el screen para el renderizado

    state = next_state  # Actualiza el estado actual
    simulated_rewards += reward  # Acumula la recompensa

# Imprimir la recompensa total obtenida en la simulación real
print(f"Recompensa total obtenida en la simulación real: {simulated_rewards:.2f}")

# Cierre de Pygame
pygame.quit()