from pydantic import BaseModel

class TrainRequest(BaseModel):
    algorithm: str  # Algoritmo de aprendizaje (ej. Q-Learning, DQN, etc.)
    episodes: int = 1000  # Número de episodios de entrenamiento
