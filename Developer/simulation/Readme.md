# Simulación de Péndulo Invertido con Q-Learning

## Table of Contents
- [English Version](#english-version)
- [Versión en Español](#versión-en-español)

---
<a name="english-version"></a>
## English Version
This repository contains a simulation of an inverted pendulum using the Q-learning reinforcement learning algorithm. The simulation is done with Pygame for graphical visualization.

## Requirements

* Python 3.x
* Librerías: `numpy`, `pygame`, `matplotlib`
  ```bash
  pip install numpy pygame matplotlib
  ```

## Execution

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MaxSaavedraLux666/ACS2024-2-GRUPO_1.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd Intelligent-Control-of-the-Inverted-Pendulum\Developer\simulation
   ```
3. **Run the main script:**
   ```bash
   python main.py 
   ```

This will run the agent training and then display a real-time simulation of the agent trying to maintain the pendulum balance. Graphs will be generated in the `graphs` folder showing the learning curve, episode lengths, and epsilon evolution (exploration/exploitation).

## Parameters

You can modify training and simulation parameters in the following files:

* **`variables.py`:** This file contains the most important parameters that control the behavior of the Q-learning algorithm:

* `n_actions`: Number of possible actions for the agent (usually 3).
* `epsilon_decay`: Epsilon decay factor (controls the rate of exploration decay). Values ​​closer to 1 indicate slower decay.
* `epsilon_min`: Minimum epsilon value (ensures minimal exploration even at the end of training).
* `n_states`: Number of discretized states per dimension of the state space. Increasing this value increases accuracy but also training time.
* `epsilon`: Initial epsilon value (exploration probability at the start of training, usually 1.0).
* Other parameters related to the pendulum physics (mass, length, gravity, etc) are found in `cart_pole.py`.
* **`train.py`:** This file contains training parameters:

* `episodes`: Total number of training episodes.
* `gamma`: Discount factor for the future value of rewards.
* `learning_rate`: Learning rate for updating the Q table.

By changing these parameters, you can experiment with different configurations and observe their impact on the agent's performance. Remember that increasing `n_states` significantly can greatly increase training time.

## Project Structure

* `main.py`: Main script to run the simulation.
* `cart_pole.py`: Class that defines the inverted pendulum environment.
* `train.py`: Functions to train the agent with Q-learning.
* `functions.py`: Auxiliary functions (state discretization, action selection).
* `graphics.py`: Functions to generate and save the graphs.
* `variables.py`: File with the global variables of the project.
* `graphs/`: Folder where the generated graphs are saved.

## Considerations

* Discretizing the state space can impact performance. Experimenting with different values ​​of `n_states` may be necessary.
* Training can take a considerable amount of time, especially with a large number of states.

This project provides a solid foundation for understanding and experimenting with reinforcement learning on a classic problem like the inverted pendulum. Have fun experimenting!


<a name="versión-en-español"></a>
## Versión en Español
Este repositorio contiene una simulación de un péndulo invertido utilizando el algoritmo de aprendizaje por refuerzo Q-learning.  La simulación se realiza con Pygame para la visualización gráfica.

## Requisitos

* Python 3.x
* Librerías: `numpy`, `pygame`, `matplotlib`
  ```bash
  pip install numpy pygame matplotlib
  ```

## Ejecución

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/MaxSaavedraLux666/ACS2024-2-GRUPO_1.git
   ```
2. **Navega al directorio del proyecto:**
   ```bash
   cd Intelligent-Control-of-the-Inverted-Pendulum\Developer\simulation
   ```
3. **Ejecuta el script principal:**
   ```bash
   python main.py 
   ```

Esto ejecutará el entrenamiento del agente y luego mostrará una simulación en tiempo real del agente intentando mantener el equilibrio del péndulo.  Se generarán gráficas en la carpeta `graphs` mostrando la curva de aprendizaje, la duración de los episodios y la evolución de epsilon (exploración/explotación).

## Parámetros

Puedes modificar los parámetros del entrenamiento y la simulación en los siguientes archivos:

* **`variables.py`:** Este archivo contiene los parámetros más importantes que controlan el comportamiento del algoritmo Q-learning:

  * `n_actions`: Número de acciones posibles para el agente (generalmente 3).
  * `epsilon_decay`: Factor de decaimiento de epsilon (controla la tasa de disminución de la exploración).  Valores más cercanos a 1 indican una disminución más lenta.
  * `epsilon_min`: Valor mínimo de epsilon (asegura una exploración mínima incluso al final del entrenamiento).
  * `n_states`: Número de estados discretizados por dimensión del espacio de estados. Aumentar este valor aumenta la precisión pero también el tiempo de entrenamiento.
  * `epsilon`: Valor inicial de epsilon (probabilidad de exploración al inicio del entrenamiento, generalmente 1.0).
  * Otros parámetros relacionados con la física del péndulo (masa, longitud, gravedad, etc) se encuentran en `cart_pole.py`.
* **`train.py`:**  Este archivo contiene parámetros del entrenamiento:

  * `episodes`: Número total de episodios de entrenamiento.
  * `gamma`: Factor de descuento para el valor futuro de las recompensas.
  * `learning_rate`: Tasa de aprendizaje para actualizar la tabla Q.

Al modificar estos parámetros, puedes experimentar con diferentes configuraciones y observar su impacto en el rendimiento del agente.  Recuerda que aumentar `n_states` significativamente puede aumentar considerablemente el tiempo de entrenamiento.

## Estructura del Proyecto

* `main.py`: Script principal para ejecutar la simulación.
* `cart_pole.py`: Clase que define el entorno del péndulo invertido.
* `train.py`: Funciones para entrenar el agente con Q-learning.
* `functions.py`: Funciones auxiliares (discretización del estado, selección de acciones).
* `graphics.py`: Funciones para generar y guardar las gráficas.
* `variables.py`: Archivo con las variables globales del proyecto.
* `graphs/`: Carpeta donde se guardan las gráficas generadas.

## Consideraciones

* La discretización del espacio de estados puede afectar el rendimiento. Experimentar con diferentes valores de `n_states` puede ser necesario.
* El entrenamiento puede tardar un tiempo considerable, especialmente con un gran número de estados.

Este proyecto proporciona una base sólida para entender y experimentar con el aprendizaje por refuerzo en un problema clásico como el péndulo invertido. ¡Diviértete experimentando!
