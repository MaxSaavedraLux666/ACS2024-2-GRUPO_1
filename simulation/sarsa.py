class SARSA:
    def __init__(self):
        self.env = create_cartpole_env()

    def train(self, episodes=1000):
        """
        Entrena al agente usando SARSA.
        """
        for episode in range(episodes):
            state = self.env.reset()
            action = self.env.action_space.sample()
            done = False
            while not done:
                next_state, reward, done, _ = self.env.step(action)
                next_action = self.env.action_space.sample()
                # Actualizar valores SARSA
                # ...
        return {"success": True}
