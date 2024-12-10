import unittest
import numpy as np
from ..simulation.others.cartpole_env import CustomCartPoleEnv


class TestCustomCartPoleEnv(unittest.TestCase):

    def setUp(self):
        """
        Configuración antes de cada prueba.
        """
        self.env = CustomCartPoleEnv(discrete_actions=True)

    def tearDown(self):
        """
        Limpieza después de cada prueba.
        """
        self.env.close()

    def test_environment_initialization(self):
        """
        Verifica que el entorno se inicializa correctamente.
        """
        self.assertIsNotNone(self.env)
        self.assertEqual(self.env.action_space.n, 3)

    def test_reset_environment(self):
        """
        Verifica que el entorno se reinicia correctamente.
        """
        initial_state = self.env.reset()
        self.assertEqual(len(initial_state), 4)  # CartPole tiene 4 dimensiones de estado

    def test_step_discrete_action(self):
        """
        Verifica que el entorno acepta una acción discreta y devuelve los resultados correctos.
        """
        self.env.reset()
        next_state, reward, done, _ = self.env.step(1)  # Ejecutar acción '0' (sin movimiento)
        self.assertEqual(len(next_state), 4)
        self.assertIsInstance(reward, float)
        self.assertIsInstance(done, bool)

    def test_reward_calculation(self):
        """
        Verifica que la función de recompensa devuelve valores dentro del rango esperado.
        """
        sample_state = np.array([0, 0, 0.1, 0])  # Estado ficticio
        reward = self.env._compute_reward(sample_state)
        self.assertGreaterEqual(reward, -1)
        self.assertLessEqual(reward, 1)

    def test_discrete_to_continuous_action(self):
        """
        Verifica la conversión de acciones discretas a continuas.
        """
        self.assertTrue(np.array_equal(self.env._discrete_to_continuous_action(0), np.array([-1.0])))
        self.assertTrue(np.array_equal(self.env._discrete_to_continuous_action(1), np.array([0.0])))
        self.assertTrue(np.array_equal(self.env._discrete_to_continuous_action(2), np.array([1.0])))


if __name__ == '__main__':
    unittest.main()
