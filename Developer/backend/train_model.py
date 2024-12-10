import matplotlib.pyplot as plt
import numpy as np
import random
import os
from models.cartpole import CartPoleEnv, discretize_state, select_action

# Hiperparámetros (ajustar según sea necesario)
episodes = 5000
gamma = 0.99
epsilon = 1.0
epsilon_decay = 0.995
epsilon_min = 0.01
learning_rate = 0.1
n_states = 8
n_actions = 3

q_table = np.zeros((n_states, n_states, n_states,
                   n_states, n_states, n_actions))
env = CartPoleEnv()
total_rewards = []

for episode in range(episodes):
    state = env.reset()
    done = False
    total_reward = 0
    while not done:
        action = select_action(state, epsilon, q_table)
        next_state, reward, done = env.step(action)
        discrete_state = discretize_state(state, n_states)
        next_discrete_state = discretize_state(next_state, n_states)
        td_target = reward + gamma * \
            np.max(q_table[next_discrete_state]) if not done else reward
        q_table[discrete_state + (action,)] += learning_rate * \
            (td_target - q_table[discrete_state + (action,)])
        state = next_state
        total_reward += reward
    total_rewards.append(total_reward)
    if epsilon > epsilon_min:
        epsilon *= epsilon_decay
    print(
        f"Episodio: {episode + 1}/{episodes}, Recompensa: {total_reward:.2f}, Epsilon: {epsilon:.4f}")

# Guardar la tabla Q entrenada
model_path = "q_table_trained.npy"
np.save(model_path, q_table)
print(f"Tabla Q guardada en {model_path}")

# Código opcional para graficar la curva de aprendizaje
plt.figure(figsize=(10, 6))
plt.plot(total_rewards)
plt.xlabel("Episodio")
plt.ylabel("Recompensa")
plt.title("Curva de Aprendizaje")
plt.grid(True)
plt.savefig("curva_aprendizaje.png")
plt.show()
