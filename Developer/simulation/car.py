import tkinter as tk
import math


class CarSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Carrito con Péndulo")
        # Aumentar la altura para incluir el péndulo
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # Crear el lienzo donde se dibujará el carrito y el péndulo
        self.canvas = tk.Canvas(root, width=600, height=300, bg="white")
        self.canvas.pack()

        # Dibujar la línea horizontal
        self.canvas.create_line(50, 150, 550, 150, width=3, fill="black")

        # Crear el carrito (un rectángulo con ruedas)
        self.car_body = self.canvas.create_rectangle(
            50, 130, 110, 150, fill="blue", outline="black")
        self.wheel1 = self.canvas.create_oval(55, 150, 65, 160, fill="black")
        self.wheel2 = self.canvas.create_oval(95, 150, 105, 160, fill="black")

        # Crear el péndulo (línea y bola)
        self.pendulum_length = 100  # Longitud del péndulo
        # Ángulo inicial del péndulo (45 grados)
        self.pendulum_angle = math.pi / 4
        self.pendulum_angular_velocity = 0  # Velocidad angular inicial
        self.pendulum_angular_acceleration = 0  # Aceleración angular inicial

        # Coordenadas iniciales del péndulo
        self.car_x = 50  # Posición inicial del carro
        self.direction = "right"  # Dirección inicial del movimiento
        self.pivot_x = self.car_x + 30  # Punto de sujeción del péndulo
        self.pivot_y = 130  # Altura del punto de sujeción

        # Calcular la posición de la bola del péndulo
        self.ball_x = self.pivot_x + self.pendulum_length * \
            math.sin(self.pendulum_angle)
        self.ball_y = self.pivot_y + self.pendulum_length * \
            math.cos(self.pendulum_angle)

        # Dibujar el péndulo
        self.pendulum_line = self.canvas.create_line(
            self.pivot_x, self.pivot_y, self.ball_x, self.ball_y, width=2, fill="black")
        self.pendulum_ball = self.canvas.create_oval(
            self.ball_x - 10, self.ball_y - 10, self.ball_x + 10, self.ball_y + 10, fill="red")

        # Crear un frame para los botones
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.X, pady=10)

        # Botones para el control del carrito
        self.start_button = tk.Button(
            self.button_frame, text="Iniciar", command=self.start_moving)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(
            self.button_frame, text="Detener", command=self.stop_moving)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.move_left_button = tk.Button(
            self.button_frame, text="Mover Izquierda", command=self.move_left)
        self.move_left_button.pack(side=tk.LEFT, padx=5)

        self.move_right_button = tk.Button(
            self.button_frame, text="Mover Derecha", command=self.move_right)
        self.move_right_button.pack(side=tk.LEFT, padx=5)

        # Variable para controlar el movimiento
        self.is_moving = False

    def start_moving(self):
        self.is_moving = True
        self.move_car()

    def stop_moving(self):
        self.is_moving = False

    def move_car(self):
        if self.is_moving:
            if self.car_x >= 500:  # Límite derecho
                self.direction = "left"
            elif self.car_x <= 50:  # Límite izquierdo
                self.direction = "right"

            # Actualizar posición del carro
            self.car_x += 5 if self.direction == "right" else -5

            # Mover el carrito
            self.canvas.move(
                self.car_body, 5 if self.direction == "right" else -5, 0)
            self.canvas.move(
                self.wheel1, 5 if self.direction == "right" else -5, 0)
            self.canvas.move(
                self.wheel2, 5 if self.direction == "right" else -5, 0)

            # Mover el péndulo
            self.update_pendulum()

            # Llamar nuevamente a la función después de un breve intervalo
            self.root.after(50, self.move_car)

    def update_pendulum(self):
        """Actualizar la posición del péndulo."""
        self.pivot_x = self.car_x + 30  # El péndulo se mueve con el carro

        # Simulación simple del movimiento del péndulo
        gravity = 0.01  # Aceleración de gravedad simulada
        self.pendulum_angular_acceleration = - \
            gravity * math.sin(self.pendulum_angle)
        self.pendulum_angular_velocity += self.pendulum_angular_acceleration
        self.pendulum_angle += self.pendulum_angular_velocity

        # Calcular la nueva posición de la bola
        self.ball_x = self.pivot_x + self.pendulum_length * \
            math.sin(self.pendulum_angle)
        self.ball_y = self.pivot_y + self.pendulum_length * \
            math.cos(self.pendulum_angle)

        # Actualizar las coordenadas del péndulo en el lienzo
        self.canvas.coords(self.pendulum_line, self.pivot_x,
                           self.pivot_y, self.ball_x, self.ball_y)
        self.canvas.coords(self.pendulum_ball, self.ball_x - 10,
                           self.ball_y - 10, self.ball_x + 10, self.ball_y + 10)

    def move_left(self):
        """Mover el carrito manualmente hacia la izquierda."""
        if self.car_x > 50:  # Verificar que no pase el límite izquierdo
            self.car_x -= 5
            self.canvas.move(self.car_body, -5, 0)
            self.canvas.move(self.wheel1, -5, 0)
            self.canvas.move(self.wheel2, -5, 0)
            self.update_pendulum()

    def move_right(self):
        """Mover el carrito manualmente hacia la derecha."""
        if self.car_x < 500:  # Verificar que no pase el límite derecho
            self.car_x += 5
            self.canvas.move(self.car_body, 5, 0)
            self.canvas.move(self.wheel1, 5, 0)
            self.canvas.move(self.wheel2, 5, 0)
            self.update_pendulum()


# Crear la ventana principal
root = tk.Tk()
simulator = CarSimulator(root)
root.mainloop()
