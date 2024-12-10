import numpy as np
import pygame
from cart_pole import CartPoleEnv
from functions import discretize_state, select_action
from variables import epsilon_min, epsilon_decay, n_actions, n_states


# Número total de episodios de entrenamiento.
episodes = 100
# Factor de descuento (gamma) para el cálculo del valor futuro de las recompensas.
gamma = 0.99
# Tasa de aprendizaje (alpha) para actualizar la tabla Q.
learning_rate = 0.1

# Tabla Q:  Matriz multidimensional que almacena los valores Q para cada estado-acción.
# Las dimensiones corresponden a la discretización de cada componente del estado (theta, theta_dot, x, x_dot, x_ddot) y la acción.
q_table = np.zeros((n_states, n_states, n_states,
                   n_states, n_states, n_actions))


def train(epsilon):
    """
    Entrena al agente usando el algoritmo Q-learning.

    Args:
        epsilon (float): Probabilidad de exploración.

    Returns:
        tuple: Una tupla conteniendo las listas de recompensas totales y duraciones de cada episodio.
    """
    env = CartPoleEnv()  # Crea una instancia del entorno de simulación.

    # Lista para almacenar las recompensas totales de cada episodio.
    total_rewards = []
    # Lista para almacenar la duración (número de pasos) de cada episodio.
    episode_durations = []

    for episode in range(episodes):  # Itera sobre cada episodio.
        state = env.reset()  # Reinicia el entorno al inicio de cada episodio.
        done = False  # Bandera para indicar si el episodio ha terminado.
        total_reward = 0  # Acumulador de la recompensa total del episodio.
        duration = 0  # Contador de pasos en el episodio.

        while not done:  # Itera hasta que el episodio termine.
            for event in pygame.event.get():  # Procesa eventos de Pygame (para cerrar la ventana si se desea)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Selecciona una acción usando una política epsilon-greedy.
            action = select_action(state, epsilon, q_table)
            # Realiza la acción y obtiene el siguiente estado, recompensa y si terminó.
            next_state, reward, done = env.step(action)

            # Discretiza el estado actual.
            discrete_state = discretize_state(state, n_states)
            # Discretiza el siguiente estado.
            next_discrete_state = discretize_state(next_state, n_states)

            # Calcula el objetivo de la actualización de la tabla Q usando el método de aprendizaje temporal por diferencias (TD).
            td_target = reward + gamma * \
                np.max(q_table[next_discrete_state]) if not done else reward
            # Actualiza el valor Q de la tabla usando el aprendizaje Q.
            q_table[discrete_state + (action,)] += learning_rate * \
                (td_target - q_table[discrete_state + (action,)])

            state = next_state  # Actualiza el estado actual.
            total_reward += reward  # Acumula la recompensa.
            duration += 1  # Incrementa la duración.

        # Almacena la recompensa total del episodio.
        total_rewards.append(total_reward)
        # Almacena la duración del episodio.
        episode_durations.append(duration)

        # Reduce epsilon gradualmente para disminuir la exploración a lo largo del entrenamiento.
        if epsilon > epsilon_min:
            epsilon *= epsilon_decay

        print(
            f"Episodio: {episode + 1}/{episodes}, Recompensa: {total_reward:.2f}, Duración: {duration}, Epsilon: {epsilon:.4f}")

    # Devuelve los resultados del entrenamiento.
    return total_rewards, episode_durations
