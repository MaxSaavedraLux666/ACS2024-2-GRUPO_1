import numpy as np
import tensorflow as tf
from collections import deque
import random


class DQNAgent:
    """
    A Deep Q-Network (DQN) Agent to interact with the environment and learn optimal policies.
    """

    def __init__(self, state_size, action_size, gamma=0.99, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995, learning_rate=0.001, memory_size=2000):
        """
        Initialize the DQN agent.
        
        Args:
            state_size (int): Dimension of the state space.
            action_size (int): Dimension of the action space.
            gamma (float): Discount factor for future rewards.
            epsilon (float): Initial exploration rate.
            epsilon_min (float): Minimum exploration rate.
            epsilon_decay (float): Decay rate for epsilon.
            learning_rate (float): Learning rate for the neural network.
            memory_size (int): Size of the replay buffer.
        """
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate

        # Replay memory to store experiences
        self.memory = deque(maxlen=memory_size)

        # Neural network model for Q-value approximation
        self.model = self._build_model()

    def _build_model(self):
        """
        Build the neural network model for Q-value approximation.
        Returns:
            tf.keras.Model: Compiled model.
        """
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(
                64, input_dim=self.state_size, activation='relu'),
            tf.keras.layers.Dense(64, activation='relu'),
            # Linear output for Q-values
            tf.keras.layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate),
                      loss='mse')
        return model

    def remember(self, state, action, reward, next_state, done):
        """
        Store an experience tuple in the replay memory.
        
        Args:
            state (array): The current state.
            action (int): The action taken.
            reward (float): The reward received.
            next_state (array): The next state.
            done (bool): Whether the episode is finished.
        """
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        """
        Choose an action based on the epsilon-greedy policy.
        
        Args:
            state (array): The current state.
        Returns:
            int: Chosen action.
        """
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)  # Explore
        q_values = self.model.predict(state, verbose=0)
        return np.argmax(q_values[0])  # Exploit

    def replay(self, batch_size):
        """
        Train the network on a batch of experiences.
        
        Args:
            batch_size (int): Number of experiences to sample from memory.
        """
        if len(self.memory) < batch_size:
            return

        # Sample a random batch of experiences
        batch = random.sample(self.memory, batch_size)

        for state, action, reward, next_state, done in batch:
            # Predict the Q-value for the current state
            target = self.model.predict(state, verbose=0)

            # Update the target Q-value
            if done:
                target[0][action] = reward
            else:
                next_q_values = self.model.predict(next_state, verbose=0)
                target[0][action] = reward + \
                    self.gamma * np.amax(next_q_values[0])

            # Train the model on the updated target
            self.model.fit(state, target, epochs=1, verbose=0)

        # Decay exploration rate
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        """
        Load a saved model from a file.
        
        Args:
            name (str): Path to the saved model file.
        """
        self.model.load_weights(name)

    def save(self, name):
        """
        Save the current model to a file.
        
        Args:
            name (str): Path to save the model file.
        """
        self.model.save_weights(name)


# Example usage:
if __name__ == "__main__":
    import gym

    # Initialize environment and agent
    env = gym.make('Pendulum-v1')
    state_size = env.observation_space.shape[0]
    # Note: Pendulum has a continuous action space
    action_size = env.action_space.shape[0]
    # Discretize action space for simplicity
    agent = DQNAgent(state_size=state_size, action_size=3)
    episodes = 1000
    batch_size = 32

    for episode in range(episodes):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        total_reward = 0

        for time in range(200):
            # Render the environment
            env.render()

            # Agent chooses an action
            action = agent.act(state)

            # Execute the action in the environment
            next_state, reward, done, _ = env.step(action)
            next_state = np.reshape(next_state, [1, state_size])

            # Store the experience in memory
            agent.remember(state, action, reward, next_state, done)

            # Transition to the next state
            state = next_state
            total_reward += reward

            if done:
                print(
                    f"Episode {episode + 1}/{episodes}, Reward: {total_reward}")
                break

        # Train the agent with experiences from memory
        agent.replay(batch_size)
