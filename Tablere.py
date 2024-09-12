import tkinter as tk
from PIL import Image, ImageTk


class HospitalSimulacion:
    def __init__(self, tamano, casilla):
        self.tamano = tamano
        self.casilla = casilla

        # Configuración de la ventana
        self.ventana = tk.Tk()
        self.ventana.title("Simulación de Hospital")

        # Crear el Canvas
        self.canvas = tk.Canvas(self.ventana, width=tamano * casilla, height=tamano * casilla)
        self.canvas.pack()

        # Cargar y redimensionar la imagen del robot
        self.imagen_robot = Image.open("D:\Tec\ia\\robot.png")  # Abre la imagen
        self.imagen_robot = self.imagen_robot.resize((casilla, casilla), Image.Resampling.LANCZOS)  # Redimensiona
        self.imagen_robot_tk = ImageTk.PhotoImage(self.imagen_robot)  # Convierte a PhotoImage

        # Dibujar el hospital (cuartos)
        self.dibujar_hospital()

        # Crear el robot en la posición inicial (fila 0, columna 0)
        self.robot = self.canvas.create_image(tamano/2, tamano/2, anchor="nw", image=self.imagen_robot_tk)
        self.pos_x = 0
        self.pos_y = 0

        # Capturar eventos de teclado para mover el robot
        self.ventana.bind("<KeyPress>", self.mover_robot)

    def dibujar_hospital(self):
        # Dibujar un hospital con cuartos como una cuadrícula
        for fila in range(self.tamano):
            for columna in range(self.tamano):
                self.canvas.create_rectangle(columna * self.casilla, fila * self.casilla,
                                             (columna + 1) * self.casilla, (fila + 1) * self.casilla,
                                             fill="lightgray")

    def mover_robot(self, event):
        # Mover el robot basado en las teclas de flecha
        if event.keysym == "Up" and self.pos_y > 0:
            self.pos_y -= 1
        elif event.keysym == "Down" and self.pos_y < self.tamano - 1:
            self.pos_y += 1
        elif event.keysym == "Left" and self.pos_x > 0:
            self.pos_x -= 1
        elif event.keysym == "Right" and self.pos_x < self.tamano - 1:
            self.pos_x += 1

        # Actualizar la posición del robot en el canvas
        self.canvas.coords(self.robot, self.pos_x * self.casilla, self.pos_y * self.casilla)

    def iniciar(self):
        # Iniciar la ventana
        self.ventana.mainloop()


# Parámetros del hospital (10x10 cuartos, cada cuarto de 60 píxeles)
simulacion = HospitalSimulacion(12, 60)
simulacion.iniciar()
