import numpy as np
import gym
from gym import spaces


class CustomCartPoleEnv(gym.Env):
    """
    Custom CartPole environment based on OpenAI Gym.
    """

    def __init__(self, discrete_actions=True):
        """
        Initializing the environment.

        Args:
            discrete_actions (bool): If True, discretizes the action space.
        """
        super(CustomCartPoleEnv, self).__init__()
        self.env = gym.make('CartPole-v1')
        self.state_space = self.env.observation_space
        self.action_space = self.env.action_space

        # If specified, discretizes the action space into {-1, 0, 1}
        if discrete_actions:
            self.action_space = spaces.Discrete(3)

    def step(self, action):
        """
        Executes an action in the environment and returns the new observation, the reward, and whether the episode has ended.
        """
        discrete_action = int(np.round(action))  # Convert continuous action to discrete (0 or 1)
        discrete_action = np.clip(discrete_action, 0, 1)

        # The step function now returns 5 values: observation, reward, terminated, truncated, info
        next_state, reward, terminated, truncated, info = self.env.step(discrete_action)

        # Join terminated and truncated to define whether the episode has ended
        done = terminated or truncated

        return np.array(next_state, dtype=np.float32), reward, done, info



    def reset(self):
        """
        Resets the environment and returns to the initial state.
        """
        initial_state = self.env.reset()[0]  # Resets the environment and returns to the initial state
        return np.array(initial_state, dtype=np.float32)  # Make sure to return the state as a 4-dimensional array


    def render(self, mode='human'):
        """
        Render the environment.

        Args:
            mode (str): Rendering mode.
        """
        return self.env.render(mode=mode)

    def close(self):
        """
        Close the environment.
        """
        self.env.close()

    def _discrete_to_continuous_action(self, discrete_action):
        """
        Converts a discrete action into a continuous one.

        Args:
            discrete_action (int): Discreet action.

        Returns:
            np.array: Continuous action.
        """
        if discrete_action == 0:
            return np.array([-1.0])  # Negative action
        elif discrete_action == 1:
            return np.array([0.0])   # No action
        elif discrete_action == 2:
            return np.array([1.0])   # Positive action

    def _compute_reward(self, state):
        """
        Calculates custom reward based on pole angle.

        Args:
            state (np.array): Current status.

        Returns:
            float: Calculated reward.
        """
        x, x_dot, theta, theta_dot = state
        reward = 1.0 - (abs(theta) / 0.2)  # Penalizes large angles
        return reward
