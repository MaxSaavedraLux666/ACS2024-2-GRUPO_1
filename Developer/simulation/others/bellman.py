

class Bellman:
    def __init__(self, alpha, gamma):
        """
        Inicializa la clase Bellman con los parámetros necesarios.
        :param alpha: Tasa de aprendizaje (learning rate).
        :param gamma: Factor de descuento (discount factor).
        """
        self.alpha = alpha
        self.gamma = gamma

    def update_q_value(self, Q, S, A, R, Q_max, is_terminal):
        """
        Actualiza el valor de Q(S, A) según la ecuación de Bellman.
        :param Q: Diccionario o matriz con los valores de Q(s, a).
        :param S: Estado actual (s).
        :param A: Acción tomada (a).
        :param R: Recompensa recibida tras tomar la acción (r).
        :param Q_max: Máximo valor Q del próximo estado S'.
        :param is_terminal: Indica si el próximo estado S' es terminal.
        :return: El valor Q(S, A) actualizado.
        """
        if is_terminal:
            # Ecuación (2): Estado terminal
            Q[S, A] += self.alpha * (R - Q[S, A])
        else:
            # Ecuación (1): Estado no terminal
            Q[S, A] += self.alpha * (R + self.gamma * Q_max - Q[S, A])
        return Q[S, A]
