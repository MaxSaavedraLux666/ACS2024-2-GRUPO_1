import numpy as np
import tensorflow as tf
from cartpole_env import CustomCartPoleEnv


class PolicyGradient:
    def __init__(self, state_size, action_size, learning_rate=0.01, gamma=0.99):
        """
        Initialize the Policy Gradient agent.
        
        Args:
            state_size (int): Dimensions of the state space.
            action_size (int): Dimensions of the action space.
            learning_rate (float): Learning rate for the neural network.
            gamma (float): Discount factor for future rewards.
        """
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.env = CustomCartPoleEnv()

        # Model for policy prediction
        self.model = self._build_model()

        # Memory for storing transitions
        self.states = []
        self.actions = []
        self.rewards = []

    def _build_model(self):
        """
        Build the neural network model for the policy.
        
        Returns:
            tf.keras.Model: Compiled model.
        """
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(24, activation='relu', input_shape=(self.state_size,)),
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(self.action_size, activation='softmax')  # Action probabilities
        ])
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate),
                      loss='categorical_crossentropy')
        return model

    def choose_action(self, state):
        """
        Select an action based on the current policy.
        
        Args:
            state (array): Current state.
        Returns:
            int: Selected action.
        """
        state = state.reshape([1, self.state_size])
        action_probs = self.model.predict(state, verbose=0)
        action = np.random.choice(self.action_size, p=action_probs[0])
        return action

    def store_transition(self, state, action, reward):
        """
        Store a transition in memory.
        
        Args:
            state (array): Current state.
            action (int): Action taken.
            reward (float): Reward received.
        """
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)

    def learn(self):
        """
        Train the policy using Policy Gradient.
        """
        # Compute discounted rewards
        discounted_rewards = self._discount_rewards()
        discounted_rewards -= np.mean(discounted_rewards)  # Normalize
        discounted_rewards /= np.std(discounted_rewards)

        # Prepare training data
        states = np.vstack(self.states)
        actions = np.array(self.actions)
        rewards = discounted_rewards

        # One-hot encode actions
        actions_onehot = np.zeros((len(actions), self.action_size))
        actions_onehot[np.arange(len(actions)), actions] = 1

        # Train the model
        self.model.train_on_batch(states, actions_onehot, sample_weight=rewards)

        # Clear memory
        self.states, self.actions, self.rewards = [], [], []

    def _discount_rewards(self):
        """
        Compute discounted rewards.
        
        Returns:
            np.array: Discounted rewards.
        """
        discounted_rewards = np.zeros_like(self.rewards, dtype=np.float32)
        cumulative = 0
        for t in reversed(range(len(self.rewards))):
            cumulative = cumulative * self.gamma + self.rewards[t]
            discounted_rewards[t] = cumulative
        return discounted_rewards

    def train(self, episodes=1000, max_steps=500):
        """
        Train the agent using Policy Gradient.
        
        Args:
            episodes (int): Number of training episodes.
            max_steps (int): Maximum steps per episode.
        """
        for episode in range(episodes):
            state = self.env.reset()
            state = np.reshape(state, [1, self.state_size])
            total_reward = 0
            done = False

            for step in range(max_steps):
                action = self.choose_action(state)
                next_state, reward, done, _ = self.env.step(action)
                next_state = np.reshape(next_state, [1, self.state_size])

                # Store the transition
                self.store_transition(state, action, reward)

                state = next_state
                total_reward += reward

                if done:
                    break

            # Update the policy after each episode
            self.learn()
            print(f"Episode {episode + 1}/{episodes}, Total Reward: {total_reward}")

        self.env.close()


# Example usage
if __name__ == "__main__":
    env = CustomCartPoleEnv()
    state_size = env.state_space.shape[0]
    action_size = env.action_space.n

    agent = PolicyGradient(state_size, action_size)
    agent.train(episodes=1000)
