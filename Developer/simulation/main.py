import pygame
import numpy as np
from cart_pole import CartPoleEnv, WIDTH, HEIGHT
from train import train, q_table
from graphics import plot_results
from variables import epsilon, n_states
from functions import discretize_state

# Inicialización de Pygame: Inicializa el módulo Pygame para la visualización.
pygame.init()
# Crea la ventana de visualización con las dimensiones especificadas.
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Establece el título de la ventana.
pygame.display.set_caption("Péndulo Invertido con Q-Learning")

# Entrenamiento: Llama a la función de entrenamiento para entrenar el agente.
total_rewards, episode_durations = train(epsilon)

# Gráficas: Genera y muestra las gráficas de los resultados del entrenamiento.
plot_results(total_rewards, episode_durations, len(total_rewards))


# Simulación en tiempo real:  Simula el comportamiento del agente entrenado en el entorno.
# Reinicia el entorno para la simulación.  Es importante crear una nueva instancia para no usar la tabla q modificada durante el entrenamiento.
env = CartPoleEnv()
state = env.reset()
done = False
simulated_rewards = 0  # Acumulador de recompensas para la simulación.

# Inicializar lista para guardar la duración de los episodios de simulación
episode_duration = []

# Simulación en tiempo real: Se ejecuta un bucle hasta que el episodio termine.
while not done:
    # Gestión de eventos de Pygame (cierre de ventana): Permite cerrar la ventana de Pygame.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Selecciona la acción basándose en la tabla Q aprendida (explotación pura): Selecciona la mejor acción según la tabla Q.
    discrete_state = discretize_state(state, n_states)
    action = np.argmax(q_table[discrete_state])

    # Avanza un paso en el entorno: Realiza la acción seleccionada en el entorno.
    next_state, reward, done = env.step(action)

    # Renderiza el entorno en tiempo real: Dibuja el estado actual del entorno en la ventana de Pygame.
    env.render(screen)

    state = next_state  # Actualiza el estado actual.
    simulated_rewards += reward  # Acumula la recompensa de la simulación.


# Imprime la recompensa total obtenida durante la simulación.
print(
    f"Recompensa total obtenida en la simulación real: {simulated_rewards:.2f}")

# Cierre de Pygame: Cierra la ventana y libera los recursos de Pygame.
pygame.quit()
