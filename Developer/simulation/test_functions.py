from functions import Function


# Inicializar sistema
sistema = Function(masa_auto=10, masa_pendulo=2,
                   longitud_cuerda=1, gravedad=9.81)

# Definir condiciones iniciales
fuerza = 15
angulo = 0.1  # En radianes
velocidad_x = 2.0
velocidad_theta = 0.5

# Calcular valores
resultados = sistema.calcular_valores(
    fuerza, angulo, velocidad_x, velocidad_theta)
print(resultados)
