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

