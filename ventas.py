# Francisco Daniele
# 28/10/24
# Descripción: Esta es la interfaz de ventas, la cuál servirá para cargar las mismas utilizando los productos cargados. 
# Todas las ventas quedarán en un registro el cual podrá ser eliminado si se lo desea.

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import db  # Importamos las funciones desde db.py

# Función para validar que solo se ingresen números en el campo de "Cantidad" y "Descuento"
def validar_numeros(entrada, max_valor=100):
    if entrada.isdigit() or entrada == "":
        return True
    elif int(entrada) > max_valor:
        messagebox.showwarning("Advertencia", f"El valor no puede ser mayor que {max_valor}.")
        return False
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingrese solo números.")
        return False

# Función para actualizar el menú desplegable de productos
def actualizar_lista_productos():
    productos = db.obtener_nombres_productos()
    entry_producto['values'] = productos

# Función para agregar producto a la tabla de ventas con validación de stock
def agregar_producto(entry_producto, entry_cantidad, entry_descuento):
    producto = entry_producto.get()
    cantidad = entry_cantidad.get()
    descuento = entry_descuento.get() or "0"  # Descuento por defecto 0 si no se ingresa nada

    if producto and cantidad:
        try:
            # Obtener el precio y el stock del producto desde la base de datos
            precio_producto = db.obtener_precio_producto(producto)
            stock_disponible = db.obtener_stock_producto(producto)

            if not precio_producto:
                messagebox.showerror("Error", "Producto no encontrado.")
                return

            cantidad = int(cantidad)
            descuento = int(descuento)

            # Verificar si el producto ya está en la tabla
            for child in tree.get_children():
                item = tree.item(child)['values']
                if item[0] == producto:
                    messagebox.showwarning("Advertencia", f"El producto '{producto}' ya está en la lista de ventas.")
                    return
                    
            # Verificar si hay suficiente stock
            if cantidad > stock_disponible:
                messagebox.showwarning("Stock Insuficiente", f"Solo hay {stock_disponible} unidades disponibles de {producto}.")
                return

            # Calcular el total multiplicando el precio por la cantidad
            precio_total = precio_producto * cantidad
            if descuento > 0:
                precio_total -= (precio_total * (descuento / 100))

            # Insertar en la tabla
            tree.insert('', 'end', values=(producto, cantidad, f"{descuento}%", f"${precio_total:.2f}"))

            # Restar y actualizar el stock en la base de datos
            nuevo_stock = stock_disponible - cantidad
            db.actualizar_stock_producto(producto, nuevo_stock)
            
            # Limpiar entradas
            entry_producto.set("")
            entry_cantidad.delete(0, tk.END)
            entry_descuento.delete(0, tk.END)

            # Calcular el total de todos los productos
            calcular_total()
        except ValueError:
            messagebox.showerror("Error", "Verifique los datos ingresados.")
    else:
        messagebox.showwarning("Advertencia", "Complete todos los campos.")

# Función para calcular el total de todos los productos agregados a la tabla
def calcular_total():
    total = 0.0
    for child in tree.get_children():
        item = tree.item(child)['values']
        total += float(item[3].replace("$", ""))  # Sumar el precio total del producto
    lbl_total.config(text=f"Total: ${total:.2f}")

# Función para modificar un producto de la tabla
def modificar_producto(entry_producto, entry_cantidad, entry_descuento):
    seleccion = tree.selection()
    if seleccion:
        producto = entry_producto.get()
        cantidad = entry_cantidad.get()
        descuento = entry_descuento.get() or "0"  # Descuento por defecto 0 si no se ingresa nada

        if producto and cantidad:
            try:
                cantidad = int(cantidad)
                descuento = int(descuento)

                # Obtener precio y stock del producto
                precio_producto = db.obtener_precio_producto(producto)
                stock_disponible = db.obtener_stock_producto(producto)

                if not precio_producto:
                    messagebox.showerror("Error", "Producto no encontrado.")
                    return

                # Verificar si hay suficiente stock
                if cantidad > stock_disponible:
                    messagebox.showwarning("Stock Insuficiente", f"Solo hay {stock_disponible} unidades disponibles de {producto}.")
                    return

                # Calcular nuevo total
                precio_total = precio_producto * cantidad
                if descuento > 0:
                    precio_total -= (precio_total * (descuento / 100))

                # Actualizar en la tabla
                tree.item(seleccion, values=(producto, cantidad, f"{descuento}%", f"${precio_total:.2f}"))

                # Limpiar entradas
                entry_producto.set("")
                entry_cantidad.delete(0, tk.END)
                entry_descuento.delete(0, tk.END)

                # Recalcular el total de todos los productos
                calcular_total()
            except ValueError:
                messagebox.showerror("Error", "Verifique los datos ingresados.")
        else:
            messagebox.showwarning("Advertencia", "Complete todos los campos.")

# Función para eliminar un producto de la tabla
def eliminar_producto():
    seleccion = tree.selection()
    if seleccion:
        tree.delete(seleccion)
        # Recalcular el total de todos los productos
        calcular_total()
    else:
        messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar.")

# Función para cargar la venta en la base de datos
def cargar_venta():
    productos_venta = []
    total_venta = 0
    for item in tree.get_children():
        producto = tree.item(item)['values'][0]
        cantidad = tree.item(item)['values'][1]
        total = float(tree.item(item)['values'][3].replace("$", ""))
        productos_venta.append(f"{producto} (x{cantidad})")
        total_venta += total
    
    productos_venta_str = ", ".join(productos_venta)
    if productos_venta:
        db.registrar_venta(productos_venta_str, total_venta)
        messagebox.showinfo("Éxito", "Venta cargada exitosamente.")
        for item in tree.get_children():
            tree.delete(item)
    else:
        messagebox.showwarning("Advertencia", "No hay productos en la tabla para cargar.")

def cargar_venta():
    productos = []
    total_venta = 0.0
    for child in tree.get_children():
        item = tree.item(child)['values']
        productos.append(f"{item[0]} x{item[1]} (Descuento: {item[2]})")
        total_venta += float(item[3].replace("$", ""))

    if productos:
        db.registrar_venta(", ".join(productos), total_venta)
        messagebox.showinfo("Éxito", "Venta cargada exitosamente.")
        tree.delete(*tree.get_children())  # Limpiar tabla
        calcular_total()  # Resetear el total
    else:
        messagebox.showwarning("Advertencia", "No hay productos para registrar.")

# Función para mostrar el registro de ventas
def mostrar_registro_ventas():
    ventas = db.obtener_registro_ventas()
    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registro de Ventas")
    ventana_registro.geometry("500x400")
    
    texto_registro = tk.Text(ventana_registro, state=tk.NORMAL)
    texto_registro.pack(padx=10, pady=10)

    for venta in ventas:
        texto_registro.insert(tk.END, f"Venta ID: {venta[0]}\nProductos: {venta[1]}\nTotal: ${venta[2]:.2f}\n\n")
    
    texto_registro.config(state=tk.DISABLED)

    # Crear un Treeview para mostrar las ventas
    tree_registro = ttk.Treeview(ventana_registro, columns=("Venta ID", "Producto", "Cantidad", "Total"), show="headings")
    tree_registro.heading("Venta ID", text="Venta ID")
    tree_registro.heading("Producto", text="Producto")
    tree_registro.heading("Cantidad", text="Cantidad")
    tree_registro.heading("Total", text="Total")
    tree_registro.pack(fill=tk.BOTH, expand=True)

    # Insertar ventas en el Treeview
    for venta in ventas:
        tree_registro.insert("", "end", values=venta)

# Función para borrar todas las ventas en la tabla de ventas
def borrar_registro():
    if messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas borrar todos los registros de ventas?"):
        # Eliminar todas las ventas de la base de datos
        db.borrar_todas_las_ventas()  # Asumiendo que esta función existe en db.py
        # Limpiar el Treeview
        for item in tree.get_children():
            tree.delete(item)
        messagebox.showinfo("Registro Borrado", "Todos los registros de ventas han sido borrados.")

# Crear la ventana
if __name__ == "__main__":
    ventana_ventas = tk.Tk()
    ventana_ventas.title("Ventas")
    ventana_ventas.geometry("850x630")

    # Crear tabla
    tree = ttk.Treeview(ventana_ventas, columns=("Producto", "Cantidad", "Descuento", "Total"), show="headings")
    tree.heading("Producto", text="Producto")
    tree.heading("Cantidad", text="Cantidad")
    tree.heading("Descuento", text="Descuento")
    tree.heading("Total", text="Total")
    tree.pack(pady=10)

    # Crear etiquetas y campos de entrada
    tk.Label(ventana_ventas, text="Producto:").pack()
    entry_producto = ttk.Combobox(ventana_ventas, state="readonly")
    entry_producto.pack()
    actualizar_lista_productos()  # Llenar el menú desplegable con productos de la base de datos

    tk.Label(ventana_ventas, text="Cantidad:").pack()
    entry_cantidad = tk.Entry(ventana_ventas, validate="key", validatecommand=(ventana_ventas.register(lambda entrada: validar_numeros(entrada)), "%P"))
    entry_cantidad.pack()

    tk.Label(ventana_ventas, text="Descuento:").pack()
    entry_descuento = tk.Entry(ventana_ventas, validate="key", validatecommand=(ventana_ventas.register(lambda entrada: validar_numeros(entrada, 100)), "%P"))
    entry_descuento.pack()

    # Botones
    max_button_width = max(len("Agregar Producto"), len("Modificar Producto"), len("Eliminar Producto"))

    btn_agregar = tk.Button(ventana_ventas, text="Agregar Producto", command=lambda: agregar_producto(entry_producto, entry_cantidad, entry_descuento), width=max_button_width)
    btn_agregar.pack(pady=5)

    btn_modificar = tk.Button(ventana_ventas, text="Modificar Producto", command=lambda: modificar_producto(entry_producto, entry_cantidad, entry_descuento), width=max_button_width)
    btn_modificar.pack(pady=5)

    btn_eliminar = tk.Button(ventana_ventas, text="Eliminar Producto", command=eliminar_producto, width=max_button_width)
    btn_eliminar.pack(pady=5)

    # Frame para los botones de registro y borrado, en la parte inferior
    frame_botones_inferior = tk.Frame(ventana_ventas)
    frame_botones_inferior.pack(pady=10)
    btn_cargar_venta = tk.Button(ventana_ventas, text="Cargar Venta", command=cargar_venta)
    btn_cargar_venta.pack(pady=5)
    # Botón para ver el registro de ventas
    btn_registro_ventas = tk.Button(frame_botones_inferior, text="Registro de Ventas", command=mostrar_registro_ventas)
    btn_registro_ventas.grid(row=0, column=0, padx=10)

    # Botón para borrar el registro de ventas
    btn_borrar_registro = tk.Button(frame_botones_inferior, text="Borrar Registro", command=borrar_registro)
    btn_borrar_registro.grid(row=0, column=1, padx=10)

    # Etiqueta de total
    lbl_total = tk.Label(ventana_ventas, text="Total: $0.00", font=("Helvetica", 16))
    lbl_total.pack(pady=10)

    ventana_ventas.mainloop()
