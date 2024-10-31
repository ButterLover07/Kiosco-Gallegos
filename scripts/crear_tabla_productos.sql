CREATE TABLE productos (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    stock INTEGER NOT NULL,
    precio REAL NOT NULL,
    fecha_agregado TEXT DEFAULT CURRENT_TIMESTAMP
);
