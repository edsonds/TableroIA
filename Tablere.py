import tkinter as tk
from PIL import Image, ImageTk
import random


class HospitalSimulacion:
    def __init__(self, tamano, casilla, num_bloqueadas, num_pilas, num_charcos, num_jeringas):
        self.tamano = tamano
        self.casilla = casilla
        self.margen_inferior = 100  # Espacio en blanco debajo del tablero

        # Configuración de la ventana
        self.ventana = tk.Tk()
        self.ventana.title("Simulación de Hospital")

        # Crear el Canvas (ancho por alto + espacio extra en la parte inferior)
        self.canvas = tk.Canvas(self.ventana, width=tamano * casilla, height=tamano * casilla + self.margen_inferior)
        self.canvas.pack()

        # Inicializar contadores
        self.pasos = 0
        self.energia = 100

        # Etiquetas para mostrar energía y pasos
        self.label_pasos = tk.Label(self.ventana, text=f"Pasos: {self.pasos}")
        self.label_pasos.pack()
        self.label_energia = tk.Label(self.ventana, text=f"Energía: {self.energia}")
        self.label_energia.pack()

        # Generar celdas bloqueadas aleatoriamente
        self.celdas_bloqueadas = self.generar_bloqueadas(num_bloqueadas)

        # Generar pilas aleatoriamente
        self.pilas = self.generar_pilas(num_pilas)

        # Generar charcos aleatoriamente
        self.charcos = self.generar_charcos(num_charcos)

        # Generar jeringas aleatoriamente
        self.jeringas = self.generar_jeringas(num_jeringas)

        # Cargar y redimensionar las imágenes de la silla, la mesa, la pila, el charco y la jeringa
        self.imagen_silla = self.convertir_transparente("Resources/Silla.png")
        self.imagen_mesa = self.convertir_transparente("Resources/mesa.png")
        self.imagen_pila = self.convertir_transparente("Resources/pila.png")
        self.imagen_charco = self.convertir_transparente("Resources/charco.png")  # Imagen del charco
        self.imagen_jeringa = self.convertir_transparente("Resources/jeringa.png")  # Imagen de la jeringa

        # Cargar y redimensionar la imagen del robot
        self.imagen_robot = self.convertir_transparente("Resources/robot.png")

        # Dibujar el hospital (cuartos), las pilas, los charcos y las jeringas
        self.dibujar_hospital()
        self.dibujar_pilas()
        self.dibujar_charcos()
        self.dibujar_jeringas()

        # Crear el robot en la posición inicial (fila 0, columna 0)
        self.robot = self.canvas.create_image(0, 0, anchor="nw", image=self.imagen_robot)
        self.pos_x = 0
        self.pos_y = 0

        # Capturar eventos de teclado para mover el robot
        self.ventana.bind("<KeyPress>", self.mover_robot)

    def convertir_transparente(self, ruta_imagen):
        """Convierte el fondo blanco de una imagen PNG a transparente"""
        imagen = Image.open(ruta_imagen).convert("RGBA")
        # Obtener los datos de la imagen (lista de pixeles)
        datos = imagen.getdata()

        # Crear una nueva lista para almacenar los datos modificados
        nuevos_datos = []
        for item in datos:
            # Cambiar el color blanco (255, 255, 255) a transparencia (0 en el canal alfa)
            if item[:3] == (255, 255, 255):
                nuevos_datos.append((255, 255, 255, 0))
            else:
                nuevos_datos.append(item)

        # Actualizar la imagen con los nuevos datos
        imagen.putdata(nuevos_datos)

        # Redimensionar la imagen
        imagen = imagen.resize((self.casilla, self.casilla), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(imagen)

    def generar_bloqueadas(self, num_bloqueadas):
        # Generar todas las posiciones posibles en la cuadrícula
        todas_posiciones = [(fila, columna) for fila in range(self.tamano) for columna in range(self.tamano)]
        # Excluir la posición inicial (0, 0) para que no esté bloqueada
        todas_posiciones.remove((0, 0))
        # Seleccionar un número de celdas bloqueadas aleatorias
        bloqueadas = random.sample(todas_posiciones, num_bloqueadas)
        # Para cada celda bloqueada, asignar aleatoriamente "silla" o "mesa"
        return [(fila, columna, random.choice(["silla", "mesa"])) for fila, columna in bloqueadas]

    def generar_pilas(self, num_pilas):
        # Generar todas las posiciones posibles en la cuadrícula excluyendo celdas bloqueadas y (0, 0)
        todas_posiciones = [(fila, columna) for fila in range(self.tamano) for columna in range(self.tamano)]
        todas_posiciones = [pos for pos in todas_posiciones if pos != (0, 0) and pos not in [(b[0], b[1]) for b in self.celdas_bloqueadas]]
        # Seleccionar un número de celdas para colocar pilas
        pilas = random.sample(todas_posiciones, num_pilas)
        return pilas

    def generar_charcos(self, num_charcos):
        # Generar todas las posiciones posibles en la cuadrícula excluyendo celdas bloqueadas, pilas y (0, 0)
        todas_posiciones = [(fila, columna) for fila in range(self.tamano) for columna in range(self.tamano)]
        todas_posiciones = [pos for pos in todas_posiciones if pos != (0, 0) and pos not in [(b[0], b[1]) for b in self.celdas_bloqueadas] and pos not in self.pilas]
        # Seleccionar un número de celdas para colocar charcos
        charcos = random.sample(todas_posiciones, num_charcos)
        return charcos

    def generar_jeringas(self, num_jeringas):
        # Generar todas las posiciones posibles en la cuadrícula excluyendo celdas bloqueadas, pilas, charcos y (0, 0)
        todas_posiciones = [(fila, columna) for fila in range(self.tamano) for columna in range(self.tamano)]
        todas_posiciones = [pos for pos in todas_posiciones if pos != (0, 0) and pos not in [(b[0], b[1]) for b in self.celdas_bloqueadas] and pos not in self.pilas and pos not in self.charcos]
        # Seleccionar un número de celdas para colocar jeringas
        jeringas = random.sample(todas_posiciones, num_jeringas)
        return jeringas

    def dibujar_hospital(self):
        # Dibujar un hospital con cuartos como una cuadrícula
        for fila in range(self.tamano):
            for columna in range(self.tamano):
                # Verificar si la celda está bloqueada y qué tipo de objeto tiene (silla o mesa)
                bloqueada = next((item for item in self.celdas_bloqueadas if item[0] == fila and item[1] == columna),
                                 None)

                if bloqueada:
                    # Si es una silla, colocar la imagen de la silla, si es una mesa, colocar la imagen de la mesa
                    if bloqueada[2] == "silla":
                        self.canvas.create_image(columna * self.casilla, fila * self.casilla, anchor="nw",
                                                 image=self.imagen_silla)
                    elif bloqueada[2] == "mesa":
                        self.canvas.create_image(columna * self.casilla, fila * self.casilla, anchor="nw",
                                                 image=self.imagen_mesa)
                else:
                    # Dibujar las celdas normales
                    self.canvas.create_rectangle(columna * self.casilla, fila * self.casilla,
                                                 (columna + 1) * self.casilla, (fila + 1) * self.casilla,
                                                 fill="lightgray")

    def dibujar_pilas(self):
        # Dibujar las pilas en el canvas
        self.pila_ids = []
        for fila, columna in self.pilas:
            pila_id = self.canvas.create_image(columna * self.casilla, fila * self.casilla, anchor="nw",
                                               image=self.imagen_pila)
            self.pila_ids.append(pila_id)

    def dibujar_charcos(self):
        # Dibujar los charcos en el canvas
        self.charco_ids = []
        for fila, columna in self.charcos:
            charco_id = self.canvas.create_image(columna * self.casilla, fila * self.casilla, anchor="nw",
                                                 image=self.imagen_charco)
            self.charco_ids.append(charco_id)

    def dibujar_jeringas(self):
        # Dibujar las jeringas en el canvas
        self.jeringa_ids = []
        for fila, columna in self.jeringas:
            jeringa_id = self.canvas.create_image(columna * self.casilla, fila * self.casilla, anchor="nw",
                                                  image=self.imagen_jeringa)
            self.jeringa_ids.append(jeringa_id)

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
        if (nueva_y, nueva_x) not in [(b[0], b[1]) for b in self.celdas_bloqueadas]:
            # Actualizar la posición del robot
            self.pos_x, self.pos_y = nueva_x, nueva_y
            self.canvas.coords(self.robot, self.pos_x * self.casilla, self.pos_y * self.casilla)

            # Actualizar el contador de pasos y energía
            self.pasos += 1
            self.energia = max(0, self.energia - 5)  # No permitir que la energía sea menor que 0

            # Verificar si el robot está sobre una pila
            if (self.pos_y, self.pos_x) in self.pilas:
                self.energia = min(100, self.energia + 20)  # No permitir que la energía supere 100
                self.pilas.remove((self.pos_y, self.pos_x))  # Eliminar la pila del mapa

                # Eliminar la pila del canvas
                self.eliminar_pila(self.pos_y, self.pos_x)

            # Verificar si el robot está sobre un charco
            if (self.pos_y, self.pos_x) in self.charcos:
                self.energia = max(0, self.energia - 20)  # Restar 20 de energía por tocar un charco

            # Verificar si el robot está sobre una jeringa
            if (self.pos_y, self.pos_x) in self.jeringas:
                self.energia = min(100, self.energia + 10)  # Sumar 10 de energía por recoger una jeringa
                self.jeringas.remove((self.pos_y, self.pos_x))  # Eliminar la jeringa del mapa

                # Eliminar la jeringa del canvas
                self.eliminar_jeringa(self.pos_y, self.pos_x)

            # Actualizar los labels de pasos y energía
            self.label_pasos.config(text=f"Pasos: {self.pasos}")
            self.label_energia.config(text=f"Energía: {self.energia}")

    def eliminar_pila(self, fila, columna):
        """Elimina la imagen de la pila en la celda especificada"""
        for pila_id in self.pila_ids:
            coords = self.canvas.coords(pila_id)
            if (coords[0] // self.casilla, coords[1] // self.casilla) == (columna, fila):
                self.canvas.delete(pila_id)
                self.pila_ids.remove(pila_id)
                break

    def eliminar_jeringa(self, fila, columna):
        """Elimina la imagen de la jeringa en la celda especificada"""
        for jeringa_id in self.jeringa_ids:
            coords = self.canvas.coords(jeringa_id)
            if (coords[0] // self.casilla, coords[1] // self.casilla) == (columna, fila):
                self.canvas.delete(jeringa_id)
                self.jeringa_ids.remove(jeringa_id)
                break

    def iniciar(self):
        # Iniciar la ventana
        self.ventana.mainloop()


# Parámetros del hospital (10x10 cuartos, cada cuarto de 60 píxeles, 5 pilas, 5 charcos y 5 jeringas)
simulacion = HospitalSimulacion(10, 60, num_bloqueadas=20, num_pilas=5, num_charcos=5, num_jeringas=1)
simulacion.iniciar()
