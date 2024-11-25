import torch
import torch.nn as nn

class DQN:
    def __init__(self):
        self.model = nn.Sequential(
            nn.Linear(4, 128),  # 4 entradas: estado
            nn.ReLU(),
            nn.Linear(128, 2)  # 2 salidas: acciones
        )

    def train(self, episodes=1000):
        """
        Entrena al agente usando DQN.
        """
        # Implementación del bucle de entrenamiento DQN
        pass
