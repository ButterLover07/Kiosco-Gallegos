# Francisco Daniele
# 28/10/24
# Descripción: Esta es la interfaz principal en la cuál hará de puente entre los productos, ventas empleados y alquiler

import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess

# Funciones para abrir las ventanas de los scripts
def abrir_ventas():
    subprocess.Popen(["python", "ventas.py"])

def abrir_productos():
    subprocess.Popen(["python", "productos.py"])

def abrir_empleados():
    subprocess.Popen(["python", "empleados.py"])

# Función que muestra la interfaz principal
def mostrar_interfaz_principal():
    # Crear ventana principal
    window = tk.Tk()
    window.title("Kiosco Gallegos")
    window.geometry("400x320")
    window.resizable(False, False)

    # Crear un frame para la imagen y los botones
    image_frame = tk.Frame(window)
    image_frame.pack(side=tk.TOP, padx=20, pady=(10, 5))  # Mantener el margen reducido entre imagen y botones

    button_frame = tk.Frame(window)
    button_frame.pack(side=tk.BOTTOM, padx=20, pady=(0, 5))  # Reducir el margen inferior

    # Definir colores para los botones
    color_ventas = "#FFCCCC"
    color_productos = "#CCCCFF"
    color_empleados = "#CCFFCC"

    # Cargar la imagen
    ruta_imagen = os.path.abspath("img/boceto_bd-Kiosco.png")
    imagen = tk.PhotoImage(file=ruta_imagen)
    imagen_redimensionada = imagen.subsample(4, 4)
    label_imagen = tk.Label(image_frame, image=imagen_redimensionada)
    label_imagen.pack(padx=20, pady=5, ipady=10)  # Mantener el margen reducido entre imagen y botones

    # Crear botones
    button_ventas = tk.Button(button_frame, text="Ventas", command=abrir_ventas, width=10, bg=color_ventas, font=("Arial", 12))
    button_productos = tk.Button(button_frame, text="Productos", command=abrir_productos, width=10, bg=color_productos, font=("Arial", 12))
    button_empleados = tk.Button(button_frame, text="Empleados", command=abrir_empleados, width=10, bg=color_empleados, font=("Arial", 12))

    # Posicionar los botones en una fila
    button_ventas.grid(row=0, column=0, padx=10, pady=5)
    button_productos.grid(row=0, column=1, padx=10, pady=5)
    button_empleados.grid(row=0, column=2, padx=10, pady=5)

    window.mainloop()

# Función para manejar la selección y validación del menú desplegable
def aceptar_seleccion():
    seleccion = combobox_opciones.get()
    if seleccion == "Selecciona una opción" or seleccion == "":
        # Mostrar mensaje de advertencia si no se selecciona ninguna opción
        messagebox.showerror("Error", "Debes elegir entre Kiosco, Librería o Panadería.")
    else:
        # Cerrar la ventana de selección y mostrar la interfaz principal
        ventana_seleccion.destroy()
        mostrar_interfaz_principal()

# Crear ventana de selección
ventana_seleccion = tk.Tk()
ventana_seleccion.title("Seleccionar Sección")  # Cambié el título de la ventana aquí
ventana_seleccion.geometry("300x150")
ventana_seleccion.resizable(False, False)

# Menú desplegable
opciones = ["Kiosco", "Librería", "Panadería"]
combobox_opciones = ttk.Combobox(ventana_seleccion, values=opciones, state="readonly")
combobox_opciones.set("Selecciona una opción")
combobox_opciones.pack(pady=20)

# Botón para aceptar la selección
btn_aceptar = tk.Button(ventana_seleccion, text="Aceptar", command=aceptar_seleccion)
btn_aceptar.pack()

ventana_seleccion.mainloop()
