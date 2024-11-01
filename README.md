﻿# Kiosco-BD

Este proyecto es una aplicación de gestión para un kiosco que permite administrar productos, ventas, empleados y alquileres. La aplicación está desarrollada en Python utilizando la biblioteca `tkinter` para la interfaz gráfica y `sqlite3` para la base de datos.

## Tabla de contenidos

- [Instalación](#instalación)
- [Ejecución de la Aplicación](#ejecución-de-la-aplicación)
- [Funcionalidades](#funcionalidades)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Conexión a la Base de Datos](#conexión-a-la-base-de-datos)
- [Pruebas de Funcionalidades CRUD](#pruebas-de-funcionalidades-crud)
- [Funcionalidades Extra](#funcionalidades-extra)

---

## Instalación

1. Clona este repositorio en tu máquina local:
   ```bash
   git clone https://github.com/ButterLover07/Kiosco-Gallegos.git
   ```
2. Accede al directorio del proyecto:
   ```bash
   cd kiosco-bd
   ```
3. Asegúrate de tener Python instalado (versión 3.6 o superior) junto con las bibliotecas necesarias.

## Ejecución de la Aplicación

Para ejecutar la aplicación principal, abre una terminal en el directorio del proyecto y ejecuta:

```bash
python main.py
```

Se abrirá una ventana con un menú desplegable donde podrás seleccionar entre "Kiosco", "Librería" o "Panadería". Una vez seleccionada la opción, se mostrará la interfaz de gestión correspondiente.

## Funcionalidades

### 1. **Gestión de Productos (`productos.py`)**

   - Agregar, modificar y eliminar productos de la base de datos.
   - Visualizar productos en una tabla con los campos: nombre, stock y precio.
   - Validación en los campos:
     - `Stock`: Solo permite números enteros.
     - `Precio`: Permite números decimales.
   - Verificación de stock antes de cada venta.

## Estructura
```bash
kiosco-bd
│
├── img                   
│   └── boceto_bd-Kiosco.png              
│
├── scripts               
│   └── crear_base_datos_kiosco.mwb
│   └── crear_base_datos_kiosco.mwb.bak
│   └── crear_tabla_productos.sql          
│
├── .gitignore              
├── README.md                
│
├── db.py                     
├── empleados.py              
├── kiosco.db                 
├── main.py                   
├── productos.py              
└── ventas.py                 
```

### 2. **Gestión de Ventas (`ventas.py`)**

   - Barra de búsqueda para seleccionar productos desde la base de datos.
   - Campos de `Cantidad` y `Descuento` validados:
     - `Cantidad`: Solo permite números.
     - `Descuento`: Solo números y no mayor a 100.
   - El precio total se calcula automáticamente, aplicando el descuento.
   - Opciones para:
     - Registrar ventas en la base de datos.
     - Cargar ventas con todos los productos en una tabla de ventas.
     - Ver el registro de ventas en una ventana separada.
   - Evita cargar el mismo producto dos veces en una venta.

### 3. **Gestión de Empleados (`empleados.py`)**

   - Permite agregar, modificar y eliminar empleados.
   - Cada empleado tiene un ID autogenerado en la base de datos, además de los campos de nombre, apellido y correo electrónico.
   - Tabla de visualización de empleados, mostrando todos los campos.

## Tecnologías Utilizadas

- **Python**: Lenguaje principal del proyecto.
- **tkinter**: Biblioteca para la interfaz gráfica de usuario.
- **SQLite**: Base de datos local para almacenar productos, ventas y empleados.

## Conexión a la Base de Datos

La base de datos `kiosco.db` se encuentra en el archivo `db.py`. Para realizar la conexión:

1. Verifica que el archivo `kiosco.db` esté en el mismo directorio que el código fuente.
2. Asegúrate de que las tablas necesarias (`productos`, `ventas`, `empleados`) están creadas. `db.py` incluye funciones para crear estas tablas automáticamente si no existen.
3. Para cambiar la ubicación de la base de datos, modifica la variable de conexión dentro de `db.py`:

   ```python
   connection = sqlite3.connect("ruta/nueva/kiosco.db")
   ```

## Pruebas de Funcionalidades CRUD

Para realizar pruebas de cada funcionalidad CRUD en los módulos, sigue estas instrucciones:

### 1. **Productos**

   - **Crear**: Completa los campos de producto y presiona el botón "Agregar Producto".
   - **Leer**: Todos los productos existentes se muestran en la tabla principal al abrir la interfaz de productos.
   - **Actualizar**: Selecciona un producto en la tabla, edita los campos y presiona "Modificar Producto".
   - **Eliminar**: Selecciona un producto en la tabla y presiona "Eliminar Producto".

### 2. **Ventas**

   - **Crear**: Selecciona un producto, ingresa la cantidad y el descuento, y presiona "Agregar Producto" para añadirlo a la venta.
   - **Leer**: Usa "Registro de Ventas" para ver todas las ventas registradas.
   - **Actualizar**: Modifica la cantidad o descuento de un producto agregado y presiona "Modificar Producto".
   - **Eliminar**: Presiona "Eliminar Producto" para quitar un producto de la tabla o "Borrar Registro" para eliminar todas las ventas de la tabla temporal.

### 3. **Empleados**

   - **Crear**: Completa los campos de nombre, apellido y correo y presiona "Agregar Empleado".
   - **Leer**: Los empleados registrados se muestran en la tabla principal.
   - **Actualizar**: Selecciona un empleado, edita los datos y presiona "Modificar Empleado".
   - **Eliminar**: Selecciona un empleado y presiona "Eliminar Empleado".

## Funcionalidades Extra

### Verificación de Stock en Ventas

Cada vez que se selecciona un producto para agregar a una venta, la aplicación verifica el stock disponible en la base de datos. Si la cantidad solicitada excede el stock, aparece un mensaje de error y el producto no se añade a la venta.

### Evitar Productos Duplicados en Ventas

En la interfaz de ventas, se evita que el mismo producto se agregue dos veces en la misma venta. Si un producto ya está en la tabla, la aplicación muestra un mensaje de error.
