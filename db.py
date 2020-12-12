import sqlite3
from sqlite3 import Error
from flask import current_app, g

def conectar():
    try:
        if 'db' not in g:
            g.db = sqlite3.connect('MinTICstagram.db')
            return g.db
    except Error:
        print(Error)

def desconectar():
    try:
        db = g.pop('db', None)
        if db is not None:
            db.close()

# Para insertar un usuario nuevo
def insertar_usuario(nombre, correo, contraseña):
    query = f"INSERT INTO Usuarios (nombre, correo, contraseña) VALUES ('{nombre}', '{correo}', '{contraseña}');"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)

# Para autenticar un usuario
def consultar_usuario(nombre, contraseña):
    query = f"SELECT * FROM Usuarios WHERE nombre='{nombre}' contraseña='{contraseña}';"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        usuario = cursor.fetchall()
        con.close()
        return True if (len(usuario) > 0) else False
    except Error:
        print(Error)

# para validar si un correo o un nombre de usuario está registrado
def validar_nuevo_usuario(nombre, correo):
    query = f"SELECT * FROM Usuarios WHERE nombre='{nombre}' OR correo='{correo}';"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        usuarios = cursor.fetchall()
        con.close()
        return True if (len(usuarios) > 0) else False
        
    except Error:
        print(Error)

# Para obtener el id de un usuario
def get_id_Usuario(nombre):
    query = f"SELECT id FROM Usuario WHERE nombre='{nombre}';"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        res = cursor.fetchone()
        con.close()
        return res[0]
        
    except Error:
        print(Error)
