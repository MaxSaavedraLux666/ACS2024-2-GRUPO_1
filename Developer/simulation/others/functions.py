""" Funciones Básicas del Proyecto """

import time

class Function:
    """Clase para calcular ecuaciones del sistema de péndulo invertido."""

    def __init__(self, masa_auto, masa_pendulo, longitud_cuerda, gravedad):
        """
        Inicializa los valores predeterminados del sistema.
        
        Args:
            masa_auto (float): Masa del carro (M).
            masa_pendulo (float): Masa del péndulo (m).
            longitud_cuerda (float): Longitud de la varilla (l).
            gravedad (float): Aceleración gravitacional (g).
        """
        self.masa_auto = masa_auto
        self.masa_pendulo = masa_pendulo
        self.longitud_cuerda = longitud_cuerda
        self.gravedad = gravedad

    def calcular_aceleracion_theta(self, fuerza, angulo):
        """
        Calcula la aceleración angular del péndulo (θ̈) usando la ecuación (3).

        Args:
            fuerza (float): Fuerza aplicada al carro (u).
            angulo (float): Ángulo de inclinación del péndulo (θ).

        Returns:
            float: Aceleración angular del péndulo (θ̈).
        """
        numerador = (self.masa_auto + self.masa_pendulo) * \
            self.gravedad * angulo - fuerza  # (M + m)g(θ̈) - u
        denominador = self.longitud_cuerda * self.masa_auto # Ml
        return numerador / denominador

    def calcular_aceleracion_x(self, fuerza, angulo):
        """
        Calcula la aceleración lineal del carro (ẍ) usando la ecuación (4).

        Args:
            fuerza (float): Fuerza aplicada al carro (u).
            angulo (float): Ángulo de inclinación del péndulo (θ).

        Returns:
            float: Aceleración lineal del carro (ẍ).
        """
        numerador = fuerza - self.masa_pendulo * \
            self.gravedad * angulo  # u - mg(θ)
        denominador = self.masa_auto # M
        return numerador / denominador

    def calcular_fuerza(self, aceleracion_x, angulo):
        """
        Calcula la fuerza necesaria (u) usando la ecuación (4).

        Args:
            aceleracion_x (float): Aceleración lineal del carro (ẍ).
            angulo (float): Ángulo de inclinación del péndulo (θ).

        Returns:
            float: Fuerza aplicada al carro (u).
        """
        return self.masa_auto * aceleracion_x + self.masa_pendulo * self.gravedad * angulo

    def calcular_valores(self, fuerza, angulo, velocidad_x, velocidad_theta):
        """
        Calcula y retorna las aceleraciones lineales y angulares del sistema.

        Args:
            fuerza (float): Fuerza aplicada al carro (u).
            angulo (float): Ángulo de inclinación del péndulo (θ).
            velocidad_x (float): Velocidad lineal del carro (ẋ).
            velocidad_theta (float): Velocidad angular del péndulo (θ̇).

        Returns:
            dict: Diccionario con aceleración angular (θ̈) y lineal (ẍ).
        """
        aceleracion_theta = self.calcular_aceleracion_theta(fuerza, angulo)
        aceleracion_x = self.calcular_aceleracion_x(fuerza, angulo)

        return {
            "aceleracion_angular_theta": aceleracion_theta,
            "aceleracion_lineal_x": aceleracion_x,
            "velocidad_actual_x": velocidad_x,
            "velocidad_actual_theta": velocidad_theta,
        }

    