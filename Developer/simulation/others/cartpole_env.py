import numpy as np
import gym
from gym import spaces

class CustomCartPoleEnv(gym.Env):
    """
    Custom CartPole environment based on OpenAI Gym, with modifiable physical parameters.
    """

    def __init__(self, discrete_actions=True, length=0.5, masscart=1.0, masspole=0.1, force_mag=10.0):
        """
        Initialize the environment with custom parameters.

        Args:
            discrete_actions (bool): If True, discretizes the action space.
            length (float): Length of the pole.
            masscart (float): Mass of the cart.
            masspole (float): Mass of the pole.
            force_mag (float): Maximum force applied to the cart.
        """
        super(CustomCartPoleEnv, self).__init__()
        self.env = gym.make('CartPole-v1')

        # Modify physical parameters
        self.env.env.length = length         # Length of the pole
        self.env.env.masscart = masscart     # Mass of the cart
        self.env.env.masspole = masspole     # Mass of the pole
        self.env.env.force_mag = force_mag   # Maximum force applied to the cart

        self.state_space = self.env.observation_space
        self.action_space = spaces.Discrete(3) if discrete_actions else self.env.action_space

    def step(self, action):
        """
        Execute an action in the environment.

        Args:
            action (int): Action to take (0, 1, or 2).

        Returns:
            Tuple[np.array, float, bool, dict]: Next state, reward, done, and info.
        """
        discrete_action = int(np.clip(np.round(action), 0, 1))  # Convert discrete action to {0, 1}
        next_state, reward, terminated, truncated, info = self.env.step(discrete_action)
        done = terminated or truncated  # Combine terminated and truncated flags

        return np.array(next_state, dtype=np.float32), reward, done, info

    def reset(self):
        """
        Reset the environment and return the initial state.

        Returns:
            np.array: Initial state.
        """
        initial_state = self.env.reset()[0]
        return np.array(initial_state, dtype=np.float32)

    def render(self):
        """
        Render the environment.
        """
        return self.env.render()

    def close(self):
        """
        Close the environment.
        """
        self.env.close()

    def _discrete_to_continuous_action(self, discrete_action):
        """
        Converts a discrete action into a continuous one.

        Args:
            discrete_action (int): Discrete action.

        Returns:
            np.array: Continuous action.
        """
        if discrete_action == 0:
            return np.array([-1.0])  # Move left
        elif discrete_action == 1:
            return np.array([0.0])   # No movement
        elif discrete_action == 2:
            return np.array([1.0])   # Move right

    def _compute_reward(self, state):
        """
        Custom reward function based on the pole's angle.

        Args:
            state (np.array): Current state.

        Returns:
            float: Calculated reward.
        """
        _, _, theta, _ = state
        reward = 1.0 - (abs(theta) / 0.2)  # Penalize large deviations from vertical
        return reward


if __name__ == "__main__":
    # Create a custom environment with modified parameters
    env = CustomCartPoleEnv(
        length=1.0,       # Length of the pole
        masscart=1.5,     # Mass of the cart
        masspole=0.2,     # Mass of the pole
        force_mag=12.0    # Maximum force
    )

    # Run a sample episode
    state = env.reset()
    done = False
    total_reward = 0

    while not done:
        action = env.action_space.sample()  # Take a random action
        next_state, reward, done, _ = env.step(action)
        total_reward += reward
        env.render()

    print(f"Total Reward: {total_reward}")
    env.close()
