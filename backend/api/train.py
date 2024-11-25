from simulation.q_learning import QLearning
from simulation.sarsa import SARSA

def train_model(algorithm):
    """
    Entrena el modelo usando el algoritmo especificado.
    """
    if algorithm == "q_learning":
        agent = QLearning()
        result = agent.train(episodes=1000)
    elif algorithm == "sarsa":
        agent = SARSA()
        result = agent.train(episodes=1000)
    else:
        raise ValueError("Algoritmo no soportado")
    
    return result
