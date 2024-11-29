
import numpy as np
import gym
import time

class QLearningAgent:
    """
    A Q-learning agent for the CartPole environment.
    """

    def __init__(self, env, alpha=0.1, gamma=0.99, epsilon=1.0, num_episodes=1000,
                 num_bins=[10, 10, 10, 10], lower_bounds=[-2.4, -3.0, -0.21, -4],
                 upper_bounds=[2.4, 3.0, 0.21, 4]):
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.num_actions = env.action_space.n
        self.num_episodes = num_episodes
        self.num_bins = num_bins
        self.lower_bounds = lower_bounds
        self.upper_bounds = upper_bounds

        self.q_table = self._create_q_table()
        self.episode_rewards = []

    def _create_q_table(self):
        """Creates the Q-table with uniform random initialization."""
        return np.random.uniform(low=0, high=1, size=(self.num_bins + [self.num_actions]))

    def _discretize_state(self, state):
        """Discretizes a continuous state into a discrete index."""
        indices = []
        for i in range(len(state)):
            bins = np.linspace(
                self.lower_bounds[i], self.upper_bounds[i], self.num_bins[i])
            index = np.digitize(state[i], bins) - 1
            index = max(0, min(index, self.num_bins[i]-1))
            indices.append(index)
        return tuple(indices)

    def _choose_action(self, state, episode_index):
        """Chooses an action using epsilon-greedy strategy."""
        if episode_index < 500 or np.random.random() < self.epsilon:
            return self.env.action_space.sample()  # Explore
        else:
            state_index = self._discretize_state(state)
            return np.argmax(self.q_table[state_index])  # Exploit

    def _update_q_table(self, state, action, reward, next_state, done):
        """Updates the Q-table using the Q-learning update rule."""
        state_index = self._discretize_state(state)
        next_state_index = self._discretize_state(next_state)

        if done:
            td_target = reward
        else:
            td_target = reward + self.gamma * \
                np.max(self.q_table[next_state_index])

        self.q_table[state_index + (action,)] += self.alpha * \
            (td_target - self.q_table[state_index + (action,)])

    def train(self):
        """Trains the Q-learning agent."""
        for episode in range(self.num_episodes):
            total_reward = 0
            state, _ = self.env.reset()
            done = False

            while not done:
                action = self._choose_action(state, episode)
                next_state, reward, done, _, _ = self.env.step(action)
                self._update_q_table(state, action, reward, next_state, done)
                state = next_state
                total_reward += reward
                if episode > 7000:
                    self.epsilon = 0.999 * self.epsilon

            self.episode_rewards.append(total_reward)