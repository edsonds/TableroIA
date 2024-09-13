import tkinter as tk
from PIL import Image, ImageTk


class HospitalSimulacion:
    def __init__(self, tamano, casilla):
        self.tamano = tamano
        self.casilla = casilla
        self.margen_inferior = 100  # Espacio en blanco debajo del tablero

        # Configuración de la ventana
        self.ventana = tk.Tk()
        self.ventana.title("Simulación de Hospital")

        # Crear el Canvas (ancho por alto + espacio extra en la parte inferior)
        self.canvas = tk.Canvas(self.ventana, width=tamano * casilla, height=tamano * casilla + self.margen_inferior)
        self.canvas.pack()

        # Definir las celdas inaccesibles (paredes o zonas bloqueadas)
        # Definir las celdas inaccesibles (paredes o zonas bloqueadas)+
        self.celdas_bloqueadas = [(14,5),(13,5),(11,5),(10,5)]

        # Cargar y redimensionar la imagen del robot
        self.imagen_robot = Image.open("robot.png")  # Abre la imagen
        self.imagen_robot = self.imagen_robot.resize((casilla, casilla), Image.Resampling.LANCZOS)  # Redimensiona
        self.imagen_robot_tk = ImageTk.PhotoImage(self.imagen_robot)  # Convierte a PhotoImage

        # Dibujar el hospital (cuartos)
        self.dibujar_hospital()

        # Crear el robot en la posición inicial (fila 0, columna 0)
        self.robot = self.canvas.create_image(0, 0, anchor="nw", image=self.imagen_robot_tk)
        self.pos_x = 0
        self.pos_y = 0

        # Capturar eventos de teclado para mover el robot
        self.ventana.bind("<KeyPress>", self.mover_robot)

    def dibujar_hospital(self):
        # Dibujar un hospital con cuartos como una cuadrícula
        for fila in range(self.tamano):
            for columna in range(self.tamano):
                if (fila, columna) in self.celdas_bloqueadas:
                    color = "black"  # Colores de las celdas bloqueadas
                else:
                    color = "lightgray"  # Colores de las celdas normales

                self.canvas.create_rectangle(columna * self.casilla, fila * self.casilla,
                                             (columna + 1) * self.casilla, (fila + 1) * self.casilla,
                                             fill=color)

    def mover_robot(self, event):
        # Calcular nueva posición del robot
        nueva_x, nueva_y = self.pos_x, self.pos_y
        if event.keysym == "Up" and self.pos_y > 0:
            nueva_y -= 1
        elif event.keysym == "Down" and self.pos_y < self.tamano - 1:
            nueva_y += 1
        elif event.keysym == "Left" and self.pos_x > 0:
            nueva_x -= 1
        elif event.keysym == "Right" and self.pos_x < self.tamano - 1:
            nueva_x += 1

        # Verificar si la nueva posición está en una celda bloqueada
        if (nueva_y, nueva_x) not in self.celdas_bloqueadas:
            self.pos_x, self.pos_y = nueva_x, nueva_y
            self.canvas.coords(self.robot, self.pos_x * self.casilla, self.pos_y * self.casilla)

    def iniciar(self):
        # Iniciar la ventana
        self.ventana.mainloop()


# Parámetros del hospital (10x10 cuartos, cada cuarto de 60 píxeles)
simulacion = HospitalSimulacion(15, 45)
simulacion.iniciar()
