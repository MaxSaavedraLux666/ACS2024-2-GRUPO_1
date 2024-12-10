import os
import numpy as np
import matplotlib.pyplot as plt
from variables import epsilon_decay, epsilon_min


def plot_results(total_rewards, episode_durations, episodes):
    """
    Genera y guarda gráficos que muestran los resultados del entrenamiento del agente.

    Args:
        total_rewards (list): Lista de las recompensas totales obtenidas en cada episodio.
        episode_durations (list): Lista de la duración (número de pasos) de cada episodio.
        episodes (int): Número total de episodios de entrenamiento.
    """
    output_folder = "graphs"  # Directorio donde se guardarán las gráficas.
    # Crea el directorio si no existe.
    os.makedirs(output_folder, exist_ok=True)

    # Calcula los valores de epsilon a lo largo de los episodios.
    epsilons = [1.0 * (epsilon_decay ** i) for i in range(episodes)]
    # Asegura que epsilon no baje de epsilon_min
    epsilons = [max(epsilon, epsilon_min) for epsilon in epsilons]

    # Gráfica de Explotación vs Exploración
    plt.figure(figsize=(12, 5))  # Crea una figura de tamaño 12x5 pulgadas.
    # Grafica la curva de epsilon.
    plt.plot(range(episodes), epsilons, label="Epsilon (Exploración)")
    plt.xlabel("Episodio")  # Etiqueta del eje x.
    plt.ylabel("Epsilon")  # Etiqueta del eje y.
    plt.title("Curva de Explotación vs Exploración")  # Título de la gráfica.
    plt.legend()  # Muestra la leyenda.
    plt.grid()  # Agrega una cuadrícula a la gráfica.
    # Guarda la gráfica.
    plt.savefig(os.path.join(output_folder, "exploracion_vs_explotacion.png"))
    plt.show()  # Muestra la gráfica.

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

    # Curva de Aprendizaje (Recompensa Promedio usando una ventana deslizante)
    window_size = 50  # Tamaño de la ventana para calcular la media móvil.
    # Calcula la media móvil.
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

    # Gráfica de Duración de los Episodios
    plt.figure(figsize=(12, 5))
    plt.plot(range(episodes), episode_durations, label="Duración del Episodio")
    plt.xlabel("Episodio")
    plt.ylabel("Duración (pasos)")
    plt.title("Duración de los Episodios")
    plt.legend()
    plt.grid()
    plt.savefig(os.path.join(output_folder, "duracion_episodios.png"))
    plt.show()
