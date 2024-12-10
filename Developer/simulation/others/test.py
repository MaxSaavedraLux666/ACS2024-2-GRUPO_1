from Developer.simulation.others.agent import QLearningAgent
import gym


def test_agent(agent):
    test_rewards = agent.test(num_episodes=5, render=True)
    print("\nTest rewards (trained agent):", test_rewards)


if __name__ == "__main__":
    env = gym.make('CartPole-v1')
    agent = QLearningAgent(env, num_episodes=5000)  # Carga el agente entrenado
    agent.train()  # Si ya lo entrenaste previamente, esta línea no es necesaria
    test_agent(agent)