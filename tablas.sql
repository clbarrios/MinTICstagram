CREATE TABLE Usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_usuario TEXT UNIQUE,
    correo TEXT UNIQUE,
    contraseña TEXT,
    activado BOOLEAN
);

CREATE TABLE Imagenes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_imagen TEXT,
    ruta TEXT,
    privada BOOLEAN
);

CREATE TABLE MeGusta (
    id_usuario INTEGER REFERENCES Usuarios (id),
    id_imagen INTEGER REFERENCES Imagenes (id),
    PRIMARY KEY (id_usuario, id_imagen)
);

CREATE TABLE Etiquetas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_etiqueta TEXT UNIQUE
);

CREATE TABLE Imagenes_Etiquetas (
    id_imagen INTEGER REFERENCES Imagenes (id),
    id_etiqueta INTEGER REFERENCES Etiquetas (id),
    PRIMARY KEY (id_imagen, id_etiqueta)
);

