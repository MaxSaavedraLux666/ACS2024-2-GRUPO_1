import gym

def create_cartpole_env():
    """
    Crea y retorna el entorno CartPole.
    """
    return gym.make("CartPole-v1")
