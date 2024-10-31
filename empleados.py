#Francisco Daniele
#28/10/24
#Descripción: Esta es la interfaz de empleados la cuál está encargada de registrar a quienes trabajan dentro del kiosco/librería/panadería

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from db import agregar_empleado, modificar_empleado, eliminar_empleado, obtener_empleados

# Función para validar la entrada del campo "Total"
def validar_total(entrada):
    if entrada.isdigit() or entrada == "":
        return True
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingrese solo números aquí.")
        return False

# Función para validar la entrada del campo "Precio"
def validar_precio(entrada):
    if entrada.replace(".", "", 1).isdigit() or entrada == "":
        return True
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingrese un número válido para el precio.")
        return False

# Función para cargar los empleados en la tabla al abrir la ventana
def cargar_empleados():
    for empleado in obtener_empleados():
        tree.insert('', 'end', values=(empleado[1], empleado[2], empleado[3], empleado[0]))

# Definir las funciones para manejar los eventos de los botones
def agregar_empleado_gui(entry_nombre, entry_apellido, entry_email):
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    email = entry_email.get()
    if nombre and apellido and email:
        nuevo_id = agregar_empleado(nombre, apellido, email)
        if nuevo_id is not None:
            tree.insert('', 'end', values=(nombre, apellido, email, nuevo_id))
            entry_nombre.delete(0, tk.END)
            entry_apellido.delete(0, tk.END)
            entry_email.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "No se pudo agregar el empleado a la base de datos.")
    else:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

def modificar_empleado_gui(entry_nombre, entry_apellido, entry_email):
    seleccion = tree.selection()
    if seleccion:
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        email = entry_email.get()
        empleado_id = tree.item(seleccion, 'values')[3]  # Obtener el ID del empleado
        if nombre and apellido and email:
            modificar_empleado(empleado_id, nombre, apellido, email)
            tree.item(seleccion, values=(nombre, apellido, email, empleado_id))
            entry_nombre.delete(0, tk.END)
            entry_apellido.delete(0, tk.END)
            entry_email.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

def eliminar_empleado_gui():
    seleccion = tree.selection()
    if seleccion:
        empleado_id = tree.item(seleccion, 'values')[3]  # Obtener el ID del empleado
        eliminar_empleado(empleado_id)
        tree.delete(seleccion)

def mostrar_info(event):
    item = tree.selection()[0]
    valores = tree.item(item, 'values')
    info_texto.config(state=tk.NORMAL)  # Habilitar la edición temporalmente
    info_texto.delete('1.0', tk.END)
    info_texto.insert(tk.END, f"Nombre: {valores[0]}\nApellido: {valores[1]}\nE-mail: {valores[2]}\nID: {valores[3]}")
    info_texto.config(state=tk.DISABLED)  # Deshabilitar la edición después de mostrar la información

# Verificar si este archivo se está ejecutando como un script independiente
if __name__ == "__main__":
    # Crear una nueva ventana solo si se ejecuta como un script independiente
    ventana_productos = tk.Tk()

    # Configurar la ventana
    ventana_productos.title("Empleados")
    ventana_productos.geometry("850x650")  # Aumentado el tamaño de la ventana en 100 píxeles de ancho y alto
    ventana_productos.resizable(False, False)  # Hacer que la ventana no sea redimensionable

    # Crear una grilla para mostrar los datos
    tree = ttk.Treeview(ventana_productos, columns=('Nombre', 'Apellido', 'E-mail', 'ID'), show='headings')
    tree.heading('Nombre', text='Nombre')
    tree.heading('Apellido', text='Apellido')
    tree.heading('E-mail', text='E-mail')
    tree.heading('ID', text='ID')
    tree.pack(pady=10)

    # Cargar los empleados existentes en la tabla
    cargar_empleados()

    # Crear etiquetas y campos de entrada para los datos
    tk.Label(ventana_productos, text="Nombre:").pack()
    entry_nombre = tk.Entry(ventana_productos)
    entry_nombre.pack()

    tk.Label(ventana_productos, text="Apellido:").pack()
    entry_apellido = tk.Entry(ventana_productos)
    entry_apellido.pack()

    tk.Label(ventana_productos, text="E-mail:").pack()
    entry_email = tk.Entry(ventana_productos)
    entry_email.pack()

    # Obtener el ancho máximo de los botones
    max_button_width = max(len("Agregar Empleado"), len("Modificar Empleado"), len("Eliminar Empleado"))

    # Botones para agregar, modificar y eliminar empleados
    btn_agregar = tk.Button(ventana_productos, text="Agregar Empleado", command=lambda: agregar_empleado_gui(entry_nombre, entry_apellido, entry_email), width=max_button_width)
    btn_agregar.pack(pady=5)

    btn_modificar = tk.Button(ventana_productos, text="Modificar Empleado", command=lambda: modificar_empleado_gui(entry_nombre, entry_apellido, entry_email), width=max_button_width)
    btn_modificar.pack(pady=5)

    btn_eliminar = tk.Button(ventana_productos, text="Eliminar Empleado", command=eliminar_empleado_gui, width=max_button_width)
    btn_eliminar.pack(pady=5)

    # Configurar evento de doble clic para mostrar información
    tree.bind("<Double-1>", mostrar_info)

    # Cuadro de texto para mostrar la información detallada
    info_texto = tk.Text(ventana_productos, height=5, width=40)
    info_texto.pack(pady=10)
    info_texto.config(state=tk.DISABLED)  # Establecer como solo lectura

    # Ejecutar el bucle de eventos de la ventana
    ventana_productos.mainloop()
