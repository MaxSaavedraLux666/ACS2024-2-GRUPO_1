# Simulación de Péndulo Invertido con Q-Learning

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
   git clone <url_del_repositorio>
   ```
2. **Navega al directorio del proyecto:**
   ```bash
   cd <nombre_del_repositorio>
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
