import gym
from agent import QLearningAgent


def train_agent():
    env = gym.make('CartPole-v1')
    agent = QLearningAgent(env, num_episodes=5000)
    agent.train()
    return agent


if __name__ == "__main__":
    trained_agent = train_agent()
    print("Training complete.")
