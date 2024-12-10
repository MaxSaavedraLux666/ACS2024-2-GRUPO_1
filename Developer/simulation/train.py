import numpy as np
import pygame
from cart_pole import CartPoleEnv
from functions import discretize_state, select_action
from variables import epsilon_min,epsilon_decay,n_actions,n_states



episodes = 100
gamma = 0.99

learning_rate = 0.1

# Tabla Q
q_table = np.zeros((n_states, n_states, n_states, n_states, n_states, n_actions))

def train(epsilon):
    env = CartPoleEnv()  # Crear una instancia del entorno  

    total_rewards = []
    episode_durations = []

    for episode in range(episodes):
        state = env.reset()
        done = False
        total_reward = 0
        duration = 0

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            action = select_action(state, epsilon, q_table)
            next_state, reward, done = env.step(action)

            discrete_state = discretize_state(state, n_states)
            next_discrete_state = discretize_state(next_state, n_states)

            td_target = reward + gamma * np.max(q_table[next_discrete_state]) if not done else reward
            q_table[discrete_state + (action,)] += learning_rate * (td_target - q_table[discrete_state + (action,)])

            state = next_state
            total_reward += reward
            duration += 1

        total_rewards.append(total_reward)
        episode_durations.append(duration)

        if epsilon > epsilon_min:
            epsilon *= epsilon_decay

        print(f"Episodio: {episode + 1}/{episodes}, Recompensa: {total_reward:.2f}, Duración: {duration}, Epsilon: {epsilon:.4f}")

    return total_rewards, episode_durations  # Devuelve los resultados