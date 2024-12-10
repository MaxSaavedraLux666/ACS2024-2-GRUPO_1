import os
import numpy as np
import matplotlib.pyplot as plt
from variables import epsilon_decay,epsilon_min

def plot_results(total_rewards, episode_durations, episodes):
    output_folder = "graphs"
    os.makedirs(output_folder, exist_ok=True)

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

    # Gráfica de Recompensa Total por Episodio
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
    window_size = 50
    avg_rewards = np.convolve(total_rewards, np.ones(window_size) / window_size, mode="valid")

    plt.figure(figsize=(12, 5))
    plt.plot(range(len(avg_rewards)), avg_rewards, label="Recompensa Promedio")
    plt.xlabel("Episodio")
    plt.ylabel("Recompensa Promedio")
    plt.title("Curva de Aprendizaje")
    plt.legend()
    plt.grid()
    plt.savefig(os.path.join(output_folder, "curva_aprendizaje.png"))
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