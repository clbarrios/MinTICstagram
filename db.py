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
    except:
        pass


# Para insertar un usuario nuevo
def insertar_usuario(nombre, correo, contraseña):
    query = f"INSERT INTO Usuarios (nombre_usuario, correo, contraseña) VALUES ('{nombre}', '{correo}', '{contraseña}');"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)


# Para autenticar un usuario
def autenticar_usuario(nombre, contraseña):
    query = f"SELECT id FROM Usuarios WHERE nombre_usuario='{nombre}' contraseña='{contraseña}';"
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
# devuelve una lista de mensajes
def validar_nuevo_usuario(nombre, correo):
    query = f"SELECT nombre_usuario, correo FROM Usuarios WHERE nombre='{nombre}' OR correo='{correo}';"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        usuarios = cursor.fetchall()
        con.close()
        msgs = []
        for msg in msgs:
            if usuarios[0] == nombre: 
                msgs.append("El nombre ya se encuentra registrado")
            if usuarios[1] == correo:
                msgs.append("El correo ya se encuentra registrado")
        if len(msgs) == 0:
            msgs.append("OK")
        return msgs        
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


def get_imagenes(usrId, privada):
    query = f"SELECT id, nombre, ruta FROM Imagenes WHERE id_usuario={usrId} AND privada={1 if privada else 0};"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        imagenes = cursor.fetchall()
        con.close()
        for img in imagenes:
            imgId = img[0]
            etiquetas = get_etiquetas(imgId)
            img.append(etiquetas)
        return imagenes
    except Error:
        print(Error)


def get_guardadas(usrId):
    query = f"SELECT I.id, I.nombre, I.ruta FROM Imagenes AS I INNER JOIN MeGusta AS MG ON MG.id_imagen = I.id WHERE MG.id_usuario={usrId};"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        imagenes = cursor.fetchall()
        con.close()
        for img in imagenes:
            imgId = img[0]
            etiquetas = get_etiquetas(imgId)
            img.append(etiquetas)
        return imagenes
    except Error:
        print(Error)


def get_etiquetas(imgId):
    query = f"SELECT E.nombre FROM Etiquetas AS E INNER JOIN Imagenes_Etiquetas IE ON IE.id_etiqueta=E.id WHERE IE.id_imagen={imgId};"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        etiquetas = cursor.fetchall()
        con.close()
        return etiquetas
    except Error:
        print(Error)


# Para insertar una etiqueta nueva
def insertar_etiqueta(nombre_etiqueta):
    query = "INSERT INTO Etiquetas (nombre_etiqueta) VALUES ('"+ nombre_etiqueta +"');"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)


# Para obtener el id de una etiqueta
def get_id_Etiqueta(nombre_etiqueta):
    query = "SELECT id FROM Etiquetas WHERE nombre_etiqueta='"+ nombre_etiqueta +"';"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        res = cursor.fetchone()
        con.close()
        return res[0]
        
    except Error:
        print(Error)


#para guardar una imagen 
def insert_guardadas(id_usuario,id_imagen):
    query = f"INSERT INTO MeGusta (id_usuario, id_imagen) VALUES({id_usuario},{id_imagen});"
    try:
        con = conectar()
        cursorObj= con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)


#para eliminar una imagen de las que guardo
def eliminar_guardadas(id_usuario,id_imagen):
    query = f"DELETE FROM MeGusta WHERE id_usuario = {id_usuario} AND id_imagen = {id_imagen};"
    try:
        con = conectar()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close
    except Error:
        print(Error)

#agregar una imagen 
def sql_insert_imagen(nombre_imagen, ruta, privada):
    query = "insert into Imagenes (nombre_imagen, ruta, privada) values('" + nombre_imagen + "','" + ruta + "'," + privada + " )"
    try:
        con = conectar()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)

#editar imagenes 
def sql_update_imagen(id, nombre_imagen, ruta, privada):
    query = "update Imagenes set nombre_imagen = '" + nombre_imagen + "', ruta = '" + ruta + "', privada = '" + privada + "' where id = '" + id
    try:
        con = conectar()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)

#eliminar una imagen 
def sql_delete_imagen(id):
    query = "delete from Imagenes where id = " + id
    try:
        con = conectar()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)

def sql_select_imagen():
    query = "select * from Imagenes"
    try:
        con = conectar()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        imagenes = cursorObj.fetchall()
        con.close()
        return imagenes    
    except Error:
        print(Error)

