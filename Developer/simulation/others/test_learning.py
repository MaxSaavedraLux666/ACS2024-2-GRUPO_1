from Developer.simulation.others.q_learning import Qlearning

qlearn = Qlearning(alpha=0.1, gamma=0.95, epsilon=0.2)
qlearn.definir_discretizacion(10, 5, 8, 5)
tabla_final = qlearn.entrenar_algoritmo(1000, 0, 0, 0.1, 0.0)
