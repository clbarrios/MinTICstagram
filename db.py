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


# Para insertar un usuario nuevo, se inserta como inactivo, i.e. activo = 0
def insertar_usuario(nombre, correo, contraseña):
    query = f"INSERT INTO Usuarios (nombre_usuario, correo, contraseña, activado) VALUES ('{nombre}', '{correo}', '{contraseña}', 0);"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        con.close()
    except Error as e:
        print(e)


# Para autenticar un usuario
def autenticar_usuario(nombre, contraseña):
    query = f"SELECT id FROM Usuarios WHERE nombre_usuario='{nombre}' AND contraseña='{contraseña}';"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        res = cursor.fetchone()
        con.close()
        return False if res is None else True
    except Error as e:
        print(e)

def activar_usuario(nombre):
    query = f"UPDATE Usuarios SET activado=1 WHERE nombre_usuario='{nombre}';"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        con.close()
    except Error as e:
        print(e)

# para validar si un correo o un nombre de usuario está registrado
# devuelve una lista de mensajes
def validar_nuevo_usuario(nombre, correo):
    query = f"SELECT nombre_usuario, correo FROM Usuarios WHERE nombre_usuario='{nombre}' OR correo='{correo}';"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        usuarios = cursor.fetchall()
        con.close()
        msgs = []
        for usuario in usuarios:
            if usuario[0] == nombre: 
                msgs.append("El nombre ya se encuentra registrado")
            if usuario[1] == correo:
                msgs.append("El correo ya se encuentra registrado")
        if len(msgs) == 0:
            msgs.append("OK")
        return msgs        
    except Error as e:
        print(e)


# Para obtener el id de un usuario
def get_id_usuario(nombre):
    query = f"SELECT id FROM Usuario WHERE nombre='{nombre}';"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        res = cursor.fetchone()
        con.close()
        return res[0]
        
    except Error as e:
        print(e)


def get_imagenes(usrId, privada):
    query = f"SELECT id, nombre_imagen, ruta FROM Imagenes WHERE id_usuario={usrId} AND privada={1 if privada else 0};"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        imagenes = cursor.fetchall()
        con.close()
        # convertir el resultado a una lista de diccionarios
        keys = ['id', 'nombre', 'ruta']
        imagenes = [{k:v for k,v in zip(keys,img)} for img in imagenes]
        for img in imagenes: 
            img['etiquetas'] = get_etiquetas(img['id'])
            
        return imagenes
    except Error as e:
        print(e)


def get_guardadas(usrId):
    query = f"SELECT I.id, I.nombre_imagen, I.ruta FROM Imagenes AS I INNER JOIN MeGusta AS MG ON MG.id_imagen = I.id WHERE MG.id_usuario={usrId};"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        imagenes = cursor.fetchall()
        con.close()
        # convertir el resultado a una lista de diccionarios
        keys = ['id', 'nombre', 'ruta']
        imagenes = [{k:v for k,v in zip(keys,img)} for img in imagenes]
        for img in imagenes: 
            img['etiquetas'] = get_etiquetas(img['id'])

        return imagenes
    except Error as e:
        print(e)


def get_etiquetas(imgId):
    query = f"SELECT E.nombre_etiqueta FROM Etiquetas AS E INNER JOIN Imagenes_Etiquetas IE ON IE.id_etiqueta=E.id WHERE IE.id_imagen={imgId};"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        etiquetas = cursor.fetchall()
        con.close()
        return [e[0] for e in etiquetas]
    except Error as e:
        print(e)


# Para insertar una etiqueta nueva
def insertar_etiqueta(nombre_etiqueta):
    query = f"INSERT OR IGNORE INTO Etiquetas (nombre_etiqueta) VALUES ('{nombre_etiqueta}');"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        con.close()
    except Error as e:
        print(e)


# Para obtener el id de una etiqueta
def get_id_etiqueta(nombre_etiqueta):
    query = f"SELECT id FROM Etiquetas WHERE nombre_etiqueta='{nombre_etiqueta}';"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        res = cursor.fetchone()
        con.close()
        return res if res is None else res[0]
        
    except Error as e:
        print(e)


#para guardar una imagen 
def insertar_guardadas(id_usuario,id_imagen):
    query = f"INSERT INTO MeGusta (id_usuario, id_imagen) VALUES({id_usuario},{id_imagen});"
    try:
        con = conectar()
        cursorObj= con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close()
    except Error as e:
        print(e)


#para eliminar una imagen de las que guardo
def eliminar_guardadas(id_usuario, id_imagen):
    query = f"DELETE FROM MeGusta WHERE id_usuario={id_usuario} AND id_imagen={id_imagen};"
    try:
        con = conectar()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close
    except Error:
        print(Error)

#agregar una imagen 
def insertar_imagen_etiqueta(id_imagen, id_etiqueta):
    query = f"INSERT INTO Imagenes_Etiquetas (id_imagen, id_etiqueta) VALUES ({id_imagen}, {id_etiqueta});"
    try:
        con = conectar()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close
    except Error as e:
        print(e)

def eliminar_imagen_etiqueta(id_imagen, id_etiqueta):
    query = f"DELETE Imagenes_Etiquetas WHERE id_imagen={id_etiqueta} AND id_etiqueta={id_etiqueta});"
    try:
        con = conectar()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close
        
    except Error as e:
        print(e)

def insertar_imagen(nombre_imagen, id_usuario, ruta, privada, etiquetas):
    query = f"INSERT INTO Imagenes (nombre_imagen, id_usuario, ruta, privada) VALUES('{nombre_imagen}', {id_usuario} '{ruta}',{1 if privada else 0});"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)            
        con.commit()
        con.close()
        
        for etiqueta in etiquetas:
            insertar_etiqueta(etiqueta)
            insertar_imagen_etiqueta(get_id_imagen(ruta), get_id_etiqueta(etiqueta))

    except Error as e:
        print(e)

def get_id_imagen(ruta):
    query = f"SELECT id FROM Imagenes WHERE ruta='{ruta}';"
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        res = cursor.fetchone()
        con.close()
        return res if res is None else res[0]
        
    except Error as e:
        print(e)


def actualizar_imagen(id_, nombre_imagen, ruta, privada, etiquetas):
    query = f"UPDATE Imagenes SET nombre_imagen='{nombre_imagen}', ruta='{ruta}', privada={1 if privada else 0} WHERE id ={id_};"
    try:
        con = conectar()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close()
        # obtener lista de etiquetas antes de la actualizacion
        etiquetas_old = get_etiquetas(id_)
        # recorrer la lista de etiquetas más corta entre la nueva y la anterior
        etiquetas_aux = etiquetas_old if len(etiquetas_old) < len(etiquetas) else etiquetas
        for e in etiquetas_aux:
            # si un elemento está en ambas listas, eliminarlo de ambas
            if (e in etiquetas_old) and (e in etiquetas):
                etiquetas_old.remove(e)
                etiquetas.remove(e)
        # los elementos que queden en etiquetas hay que agregarlos/asociarlos a la imagen
        for e in etiquetas:
            insertar_etiqueta(e)
            insertar_imagen_etiqueta(id_, get_id_etiqueta(e))
        # para los elementos que queden en etiquetas_old hay que eliminar su relación con la imagen
        for e in etiquetas_old:
            eliminar_imagen_etiqueta(id_, get_id_etiqueta(e))

    except Error as e:
        print(e)

def eliminar_imagen(id_):
    # 1. Eliminar referencias a la imagen en la tabla MeGusta
    # 2. Eliminar referencias a la imagen en la tabla Imagenes_etiquetas
    # 3. Eliminar registro en tabla Imagenes
    queries =  [
        f"DELETE FROM MeGusta WHERE id_imagen={id_};",
        f"DELETE FROM Imagenes_Etiquetas WHERE id_imagen={id_};",
        f"DELETE FROM Imagenes WHERE id={id_};"
    ]
    try:
        con = conectar()
        cursorObj = con.cursor()
        for query in queries: 
            cursorObj.execute(query)
        con.commit()
        con.close()
    except Error as e:
        print(e)
