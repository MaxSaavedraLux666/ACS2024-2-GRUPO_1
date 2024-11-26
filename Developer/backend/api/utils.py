def log_training(algorithm, result):
    """
    Log de los resultados del entrenamiento.
    """
    with open("training_logs.txt", "a") as file:
        file.write(f"Algorithm: {algorithm}, Result: {result}\n")
