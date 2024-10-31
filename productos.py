#Francisco Daniele
#28/10/24
#Descripción: Esta es la interfaz de productos en las que se podrán cargar, modificar y eliminar los productos 
#para luego ser utilizados en el registro de ventas


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import db  # Importamos las funciones desde db.py


# Función para validar la entrada del campo "Stock"
def validar_stock(entrada):
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

# Función para agregar el producto a la base de datos y a la tabla
def agregar_producto(entry_nombre, entry_stock, entry_precio):
    nombre = entry_nombre.get()
    stock = entry_stock.get()
    precio = entry_precio.get()

    # Asegurarse de que el precio tenga el símbolo "$" al principio
    if precio and not precio.startswith("$"):
        precio = "$" + precio

    if nombre and stock and precio:
        stock = int(stock)
        precio = float(precio.replace("$", ""))
        
        # Agregar producto a la base de datos
        producto_id = db.agregar_producto(nombre, stock, precio)
        
        if producto_id:
            tree.insert('', 'end', values=(producto_id, nombre, stock, f"${precio:.2f}"))
            entry_nombre.delete(0, tk.END)
            entry_stock.delete(0, tk.END)
            entry_precio.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "No se pudo agregar el producto a la base de datos.")
    else:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

# Función para manejar el evento de presionar la tecla "Enter"
def agregar_con_enter(event, entry_nombre, entry_stock, entry_precio):
    agregar_producto(entry_nombre, entry_stock, entry_precio)

# Función para modificar el producto en la base de datos y en la tabla
def modificar_producto(entry_nombre, entry_stock, entry_precio):
    seleccion = tree.selection()
    if seleccion:
        nombre = entry_nombre.get()
        stock = entry_stock.get()
        precio = entry_precio.get()

        # Asegurarse de que el precio tenga el símbolo "$" al principio
        if precio and not precio.startswith("$"):
            precio = "$" + precio

        if nombre and stock and precio:
            stock = int(stock)
            precio = float(precio.replace("$", ""))
            
            # Obtener el ID del producto seleccionado
            item = tree.item(seleccion)
            producto_id = item['values'][0]

            # Modificar producto en la base de datos
            if db.modificar_producto(producto_id, nombre, stock, precio):
                tree.item(seleccion, values=(producto_id, nombre, stock, f"${precio:.2f}"))
                entry_nombre.delete(0, tk.END)
                entry_stock.delete(0, tk.END)
                entry_precio.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "No se pudo modificar el producto en la base de datos.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

# Función para eliminar el producto de la base de datos y de la tabla
def eliminar_producto():
    seleccion = tree.selection()
    if seleccion:
        item = tree.item(seleccion)
        producto_id = item['values'][0]

        # Eliminar producto de la base de datos
        if db.eliminar_producto(producto_id):
            tree.delete(seleccion)
        else:
            messagebox.showerror("Error", "No se pudo eliminar el producto de la base de datos.")

# Función para mostrar la información del producto seleccionado
def mostrar_info(event):
    item = tree.selection()[0]
    valores = tree.item(item, 'values')
    info_texto.config(state=tk.NORMAL)
    info_texto.delete('1.0', tk.END)
    info_texto.insert(tk.END, f"Nombre: {valores[1]}\nStock: {valores[2]}\nPrecio: {valores[3]}")
    info_texto.config(state=tk.DISABLED)

# Cargar productos desde la base de datos al iniciar la aplicación
def cargar_productos():
    productos = db.obtener_productos()
    for producto in productos:
        tree.insert('', 'end', values=(producto[0], producto[1], producto[2], f"${producto[3]:.2f}"))

# Verificar si este archivo se está ejecutando como un script independiente
if __name__ == "__main__":

    # Crear una nueva ventana
    ventana_productos = tk.Tk()

    # Configurar la ventana
    ventana_productos.title("Productos")
    ventana_productos.geometry("650x550")

    # Crear una grilla para mostrar los datos (ahora incluye una columna para el ID, oculta)
    tree = ttk.Treeview(ventana_productos, columns=('ID', 'Nombre', 'Stock', 'Precio'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Nombre', text='Nombre')
    tree.heading('Stock', text='Stock')
    tree.heading('Precio', text='Precio')

    tree.column('ID', width=0, stretch=tk.NO)  # Ocultar la columna de ID

    tree.pack(pady=10)

    # Crear etiquetas y campos de entrada para los datos
    tk.Label(ventana_productos, text="Nombre:").pack()
    entry_nombre = tk.Entry(ventana_productos)
    entry_nombre.pack()

    tk.Label(ventana_productos, text="Stock:").pack()
    entry_stock = tk.Entry(ventana_productos)
    entry_stock.pack()

    tk.Label(ventana_productos, text="Precio:").pack()
    entry_precio = tk.Entry(ventana_productos)
    entry_precio.pack()

    # Configurar validación de entrada para el campo "Stock"
    validar_stock_cmd = ventana_productos.register(validar_stock)
    entry_stock.config(validate="key", validatecommand=(validar_stock_cmd, "%P"))

    # Configurar validación de entrada para el campo "Precio"
    validar_precio_cmd = ventana_productos.register(validar_precio)
    entry_precio.config(validate="key", validatecommand=(validar_precio_cmd, "%P"))

    # Vincular la tecla "Enter" al evento de agregar producto
    entry_nombre.bind("<Return>", lambda event: agregar_con_enter(event, entry_nombre, entry_stock, entry_precio))
    entry_stock.bind("<Return>", lambda event: agregar_con_enter(event, entry_nombre, entry_stock, entry_precio))
    entry_precio.bind("<Return>", lambda event: agregar_con_enter(event, entry_nombre, entry_stock, entry_precio))

    # Botones para agregar, modificar y eliminar productos
    max_button_width = max(len("Agregar Producto"), len("Modificar Producto"), len("Eliminar Producto"))

    btn_agregar = tk.Button(ventana_productos, text="Agregar Producto", command=lambda: agregar_producto(entry_nombre, entry_stock, entry_precio), width=max_button_width)
    btn_agregar.pack(pady=5)

    btn_modificar = tk.Button(ventana_productos, text="Modificar Producto", command=lambda: modificar_producto(entry_nombre, entry_stock, entry_precio), width=max_button_width)
    btn_modificar.pack(pady=5)

    btn_eliminar = tk.Button(ventana_productos, text="Eliminar Producto", command=eliminar_producto, width=max_button_width)
    btn_eliminar.pack(pady=5)

    # Configurar evento de doble clic para mostrar información
    tree.bind("<Double-1>", mostrar_info)

    # Cuadro de texto para mostrar la información detallada
    info_texto = tk.Text(ventana_productos, height=5, width=40)
    info_texto.pack(pady=10)
    info_texto.config(state=tk.DISABLED)

    # Cargar productos al iniciar
    cargar_productos()

    # Ejecutar el bucle de eventos de la ventana
    ventana_productos.mainloop()
