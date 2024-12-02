import numpy as np

class Qlearning():
    """Clase para el algoritmo Q-learning."""
    
    def __init__(self, alpha=0.1, gamma=0.99, epsilon=2.0):
        """Valores predeterminados."""
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.tabla_valor = None
        self.tabla_indice = None
        self.intervalo_posicion_carro = None
        self.intervalo_velocidad_carro = None
        self.intervalo_angulo_pendulo = None
        self.intervalo_velocidad_angulo_pendulo = None
        self.cantidad_estados = None

    def definir_discretizacion(self, intervalo_posicion_carro=10, intervalo_velocidad_carro=5, intervalo_angulo_pendulo=8, intervalo_velocidad_angulo_pendulo=5):
        """Define los valores de discretización para calcular el tamaño de la tabla de estados."""
        self.intervalo_posicion_carro = intervalo_posicion_carro
        self.intervalo_velocidad_carro = intervalo_velocidad_carro
        self.intervalo_angulo_pendulo = intervalo_angulo_pendulo
        self.intervalo_velocidad_angulo_pendulo = intervalo_velocidad_angulo_pendulo
        self.cantidad_estados = (self.intervalo_posicion_carro *
                                 self.intervalo_velocidad_carro *
                                 self.intervalo_angulo_pendulo *
                                 self.intervalo_velocidad_angulo_pendulo)
        return self.cantidad_estados

    def crear_tabla_valores(self):
        """Crea la tabla de valores Q para el aprendizaje."""
        # Número de filas = cantidad de estados; Número de columnas = cantidad de acciones (2 acciones: izquierda y derecha)
        self.tabla_valor = np.zeros((self.cantidad_estados, 2))
        return self.tabla_valor

    def crear_tabla_indice_estados(self):
        """Crea la tabla para los índices de los estados discretizados."""
        self.tabla_indice = []
        for x in range(self.intervalo_posicion_carro):
            for dx in range(self.intervalo_velocidad_carro):
                for theta in range(self.intervalo_angulo_pendulo):
                    for dtheta in range(self.intervalo_velocidad_angulo_pendulo):
                        self.tabla_indice.append((x, dx, theta, dtheta))
        return self.tabla_indice

    def discretizar_estado_v0(self, posicion, velocidad, angulo, velocidad_angular):
        """Discretiza un estado continuo al índice correspondiente en la tabla."""
        x_bin = min(int(posicion * self.intervalo_posicion_carro),
                    self.intervalo_posicion_carro - 1)
        dx_bin = min(int(velocidad * self.intervalo_velocidad_carro),
                     self.intervalo_velocidad_carro - 1)
        theta_bin = min(int(angulo * self.intervalo_angulo_pendulo),
                        self.intervalo_angulo_pendulo - 1)
        dtheta_bin = min(int(velocidad_angular * self.intervalo_velocidad_angulo_pendulo),
                         self.intervalo_velocidad_angulo_pendulo - 1)
        return self.tabla_indice.index((x_bin, dx_bin, theta_bin, dtheta_bin))

    def discretizar_estado(self, x, dx, theta, dtheta):
        """Discretiza el estado continuo y encuentra su índice en la tabla."""
        # Convertir las variables continuas en índices discretos
        x_bin = max(0, min(self.intervalo_posicion_carro - 1,
                    int((x + 2.4) / (4.8 / self.intervalo_posicion_carro))))
        dx_bin = max(0, min(self.intervalo_velocidad_carro - 1,
                            int((dx + 1.0) / (2.0 / self.intervalo_velocidad_carro))))
        theta_bin = max(0, min(self.intervalo_angulo_pendulo - 1,
                        int((theta + 12.0) / (24.0 / self.intervalo_angulo_pendulo))))
        dtheta_bin = max(0, min(self.intervalo_velocidad_angulo_pendulo - 1,
                                int((dtheta + 2.0) / (4.0 / self.intervalo_velocidad_angulo_pendulo))))

        print(f'Antes : {x}')
        print(f'Después : {x_bin}')

        # Buscar en la tabla de índices
        try:
            return self.tabla_indice.index((x_bin, dx_bin, theta_bin, dtheta_bin))
        except ValueError:
            raise ValueError(
                f"El estado discretizado ({x_bin}, {dx_bin}, {theta_bin}, {dtheta_bin}) no está en la tabla de índices.")

    def bellman_valor_accion(self, valor_estado, recompensa, valor_estado_maximo, estado_terminal=False):
        """Calcula el valor de la acción mediante la ecuación de Bellman."""
        if estado_terminal:
            valor = valor_estado + self.alpha * (recompensa - valor_estado)
        else:
            valor = valor_estado + self.alpha * \
                (recompensa + self.gamma * valor_estado_maximo - valor_estado)
        return valor

    def actualizar_valor_tabla(self, estado, accion, recompensa, siguiente_estado, estado_terminal=False):
        """Actualiza la tabla Q basada en la ecuación de Bellman."""
        indice_estado = self.discretizar_estado(*estado)
        indice_siguiente = self.discretizar_estado(*siguiente_estado)
        valor_actual = self.tabla_valor[indice_estado, accion]
        valor_max_siguiente = np.max(self.tabla_valor[indice_siguiente])
        self.tabla_valor[indice_estado, accion] = self.bellman_valor_accion(
            valor_actual, recompensa, valor_max_siguiente, estado_terminal)
        print(
            f"Estado: {indice_estado}, Acción: {accion}, Nuevo Valor: {self.tabla_valor[indice_estado, accion]}")

    def entrenar_algoritmo(self, cantidad_pasos, posicion_inicial, velocidad_inicial, angulo_inicial, velocidad_angular_inicial):
        """Desarrolla el entrenamiento del algoritmo Q-learning."""
        estado_actual = (posicion_inicial, velocidad_inicial,
                         angulo_inicial, velocidad_angular_inicial)
        self.crear_tabla_valores()
        self.crear_tabla_indice_estados()

        for paso in range(cantidad_pasos):
            # Elegir acción basada en epsilon-greedy
            p = np.random.rand()
            indice_estado = self.discretizar_estado(*estado_actual)
            if p > self.epsilon:
                accion = np.argmax(self.tabla_valor[indice_estado])
            else:
                accion = np.random.choice([0, 1])

            # Simular la acción para obtener el nuevo estado y recompensa
            nueva_posicion = np.clip(
                estado_actual[0] + np.random.uniform(-0.1, 0.1), -2.4, 2.4)
            nueva_velocidad = np.clip(
                estado_actual[1] + np.random.uniform(-0.05, 0.05), -1, 1)
            nuevo_angulo = np.clip(
                estado_actual[2] + np.random.uniform(-0.2, 0.2), -0.2, 0.2)
            nueva_velocidad_angular = np.clip(
                estado_actual[3] + np.random.uniform(-0.1, 0.1), -1, 1)
            siguiente_estado = (nueva_posicion, nueva_velocidad,
                                nuevo_angulo, nueva_velocidad_angular)

            recompensa = 1 if abs(nuevo_angulo) < 0.2 and abs(
                nueva_posicion) < 2.4 else -1
            estado_terminal = recompensa == -1

            # Actualizar tabla
            self.actualizar_valor_tabla(
                estado_actual, accion, recompensa, siguiente_estado, estado_terminal)

            # Si es un estado terminal, reiniciar el estado actual
            estado_actual = siguiente_estado if not estado_terminal else (
                posicion_inicial, velocidad_inicial, angulo_inicial, velocidad_angular_inicial)

        return self.tabla_valor