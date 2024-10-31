#Francisco Daniele
#28/10/24
#Descripción: Este archivo de código maneja la creación de tablas y la interacción entre la base de datos y la interfaz


import sqlite3
# Crear o conectar la base de datos
conn = sqlite3.connect('kiosco.db')
cursor = conn.cursor()

def obtener_nombres_productos():
    conexion = sqlite3.connect("kiosco.db")
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT nombre FROM productos")
        productos = [fila[0] for fila in cursor.fetchall()]
    except sqlite3.Error as e:
        print("Error al obtener los nombres de productos:", e)
        productos = []
    finally:
        conexion.close()
    return productos

# Conectar a la base de datos
def conectar():
    return sqlite3.connect('kiosco.db')

# Función para actualizar el stock de un producto después de una venta
def actualizar_stock_producto(nombre_producto, cantidad_vendida):
    conn = conectar()
    cursor = conn.cursor()
    # Obtener el stock actual
    cursor.execute("SELECT stock FROM productos WHERE nombre = ?", (nombre_producto,))
    resultado = cursor.fetchone()
    if resultado:
        stock_actual = resultado[0]
        nuevo_stock = stock_actual - cantidad_vendida
        if nuevo_stock < 0:
            nuevo_stock = 0  # Evitar stock negativo
        cursor.execute("UPDATE productos SET stock = ? WHERE nombre = ?", (nuevo_stock, nombre_producto))
        conn.commit()
    conn.close()

# Funciones para manejar ventas en la base de datos
def agregar_venta(producto_id, cantidad, descuento, total):
    try:
        cursor.execute('INSERT INTO ventas (producto_id, cantidad, descuento, total) VALUES (?, ?, ?, ?)', (producto_id, cantidad, descuento, total))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print("Error al agregar venta:", e)
        return None

# Función para obtener el stock de un producto por su nombre
def obtener_stock_producto(nombre_producto):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT stock FROM productos WHERE nombre = ?", (nombre_producto,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

# Función para obtener el registro de todas las ventas
def obtener_registro_ventas():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM ventas')
    ventas = cursor.fetchall()
    conexion.close()
    
    return ventas  # Retorna una lista con todas las ventas registradas

# Función para crear la tabla de productos (si aún no existe)
def crear_tabla_productos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

# Función para crear la tabla de ventas (si aún no existe)
def crear_tabla_ventas():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            productos TEXT NOT NULL,
            total REAL NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

# Función para crear la tabla de empleados (si aún no existe)
def crear_tabla_empleados():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

# Función para obtener el precio de un producto
def obtener_precio_producto(nombre_producto):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('SELECT precio FROM productos WHERE nombre = ?', (nombre_producto,))
    resultado = cursor.fetchone()
    conexion.close()
    
    if resultado:
        return resultado[0]  # Retorna el precio del producto
    else:
        return None  # Si no se encuentra el producto

# Función para registrar una venta en la tabla de ventas
def registrar_venta(productos, total):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('INSERT INTO ventas (productos, total) VALUES (?, ?)', (productos, total))
    conexion.commit()
    conexion.close()

# Función para obtener el registro de todas las ventas
def obtener_registro_ventas():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM ventas')
    ventas = cursor.fetchall()
    conexion.close()
    
    return ventas  # Retorna una lista con todas las ventas registradas

# Función para obtener todos los productos (necesaria para productos.py)
def obtener_productos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('SELECT id, nombre, stock, precio FROM productos')  # El orden debe ser ID, Nombre, Stock, Precio
    productos = cursor.fetchall()
    conexion.close()
    
    return productos  # Retorna una lista con todos los productos registrados

# Función para agregar un producto
def agregar_producto(nombre, stock, precio):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)', (nombre, precio, stock))
    conexion.commit()
    producto_id = cursor.lastrowid  # Obtener el ID del último producto insertado
    conexion.close()
    return producto_id

# Función para modificar un producto
def modificar_producto(id_producto, nuevo_nombre, nuevo_precio, nuevo_stock):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        UPDATE productos 
        SET nombre = ?, precio = ?, stock = ? 
        WHERE id = ?
    ''', (nuevo_nombre, nuevo_precio, nuevo_stock, id_producto))
    conexion.commit()
    exito = cursor.rowcount > 0  # Verificar si se modificó alguna fila
    conexion.close()
    return exito

# Función para eliminar un producto
def eliminar_producto(id_producto):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM productos WHERE id = ?', (id_producto,))
    conexion.commit()
    exito = cursor.rowcount > 0  # Verificar si se eliminó alguna fila
    conexion.close()
    return exito

# Función para borrar todas las ventas (utilizada en ventas.py)
def borrar_todas_las_ventas():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM ventas')
    conexion.commit()
    conexion.close()

# Función para agregar un empleado
def agregar_empleado(nombre, apellido, email):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('INSERT INTO empleados (nombre, apellido, email) VALUES (?, ?, ?)', (nombre, apellido, email))
    conexion.commit()
    empleado_id = cursor.lastrowid  # Obtener el ID del último empleado insertado
    conexion.close()
    return empleado_id

# Función para modificar un empleado
def modificar_empleado(id_empleado, nuevo_nombre, nuevo_apellido, nuevo_email):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        UPDATE empleados
        SET nombre = ?, apellido = ?, email = ?
        WHERE id = ?
    ''', (nuevo_nombre, nuevo_apellido, nuevo_email, id_empleado))
    conexion.commit()
    exito = cursor.rowcount > 0  # Verificar si se modificó alguna fila
    conexion.close()
    return exito

# Función para eliminar un empleado
def eliminar_empleado(id_empleado):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM empleados WHERE id = ?', (id_empleado,))
    conexion.commit()
    exito = cursor.rowcount > 0  # Verificar si se eliminó alguna fila
    conexion.close()
    return exito

# Función para obtener todos los empleados
def obtener_empleados():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('SELECT id, nombre, apellido, email FROM empleados')
    empleados = cursor.fetchall()
    conexion.close()
    
    return empleados  # Retorna una lista con todos los empleados registrados

# Llamada para crear las tablas si no existen
crear_tabla_productos()
crear_tabla_ventas()
crear_tabla_empleados()
