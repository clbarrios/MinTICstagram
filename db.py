import sqlite3
from sqlite3 import Error
from flask import current_app, g


def conectar():
    try:
        if 'db' not in g:
            g.db = sqlite3.connect('MinTICstagram.db')
        return g.db
    except Error as e:
        print(e)
        

def desconectar():
    try:
        db = g.pop('db', None)
        if db is not None:
            db.close()
    except Error as e:
        print(e)


def insertar_usuario(nombre, correo, contraseña):
    '''
    Inserta un nuevo usuario a la base de datos, por defecto con la cuenta sin
    activar
    '''
    query = """INSERT INTO Usuarios (nombre_usuario, correo, contraseña, activado)
               VALUES ('?', '?', '?', 0);"""
    values = (nombre, correo, contraseña)
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        con.close()
    except Error as e:
        print(e)


def autenticar_usuario(nombre, contraseña):
    '''
    retorna None si el las credenciales no coinciden con la base de datos,
    y un diccionario con las llaves id, nombre_usuario, correo y contraseña si
    las credenciales coinciden
    '''
    query = """SELECT id, nombre_usuario 
               FROM Usuarios 
               WHERE nombre_usuario='?' AND contraseña='?';"""
    values = (nombre, contraseña)
    keys = ['id', 'nombre_usuario']
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query, values)
        res = cursor.fetchone()
        con.close()
        return None if res is None else {k:v for k,v in zip(keys, res)}
    except Error as e:
        print(e)


def activar_usuario(nombre):
    '''
    Activar la cuenta de un usuario
    '''
    query = "UPDATE Usuarios SET activado=1 WHERE nombre_usuario='?';"
    values = (nombre,)
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query, values)
        con.commit()
        con.close()
    except Error as e:
        print(e)


def validar_nuevo_usuario(nombre, correo):
    '''
    Retorna una lista de mensajes indicando si el nombre de usuario o el
    '''
    query = """SELECT nombre_usuario, correo 
               FROM Usuarios 
               WHERE nombre_usuario='?' OR correo='?';"""
    values = (nombre, correo)
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query, values)
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

def get_id_usuario(nombre):
    '''
    obtener el id de un usuario por su nombre de usuario
    '''
    query = "SELECT id FROM Usuario WHERE nombre='?';"
    values = (nombre,)
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query, values)
        res = cursor.fetchone()
        con.close()
        return res[0]
        
    except Error as e:
        print(e)


def get_imagenes(usrId, privada):
    '''
    Consultar lista de imagenes para el usario de id usrId, privada es un
    booleano que indica si se desea consultar las imagenes privadas o publicas.
    Se retorna una lista de diccionarios con las llaves: id, nombre, ruta y
    etiquetas, siendo esta última una lista
    '''
    query = """SELECT id, nombre_imagen, ruta 
               FROM Imagenes 
               WHERE id_usuario=? AND privada=?;"""
    values = (usrId, 1 if privada else 0)
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query, values)
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
    '''
    Consultar lista de imagenes guardadas para el usario de id usrId.
    Sólo retorna imagenes de otros usuarios a las que se les dio 'me gusta'.
    Se retorna una lista de diccionarios con las llaves: id, nombre, ruta y
    etiquetas, siendo esta última una lista
    '''
    query = """SELECT I.id, I.nombre_imagen, I.ruta 
               FROM Imagenes AS I 
               INNER JOIN MeGusta AS MG ON MG.id_imagen = I.id 
               WHERE MG.id_usuario=?;"""
    values = (usrId,)
    
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query, values)
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
    '''
    Retorna una lista con las etiquetas asociadas a la imagen identificada con
    el id imgId
    '''
    query = """SELECT E.nombre_etiqueta 
               FROM Etiquetas AS E 
               INNER JOIN Imagenes_Etiquetas IE ON IE.id_etiqueta=E.id 
               WHERE IE.id_imagen=?;"""
    values = (imgId,)
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query, values)
        etiquetas = cursor.fetchall()
        con.close()
        return [e[0] for e in etiquetas]
    except Error as e:
        print(e)


def insertar_etiqueta(nombre_etiqueta):
    '''
    Inserta una etiqueta en la base de datos, si la etiqueta ya se encuentra en
    la base de datos se ignora la inserción 
    '''
    query = """INSERT OR IGNORE 
               INTO Etiquetas (nombre_etiqueta) 
               VALUES ('?');"""
    values = (nombre_etiqueta,)
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query, values)
        con.commit()
        con.close()
    except Error as e:
        print(e)


def get_id_etiqueta(nombre_etiqueta):
    '''
    Obtener el id de una etiqueta dado su nombre. Si no se encuentra en la base
    de datos retorna None
    '''
    query = "SELECT id FROM Etiquetas WHERE nombre_etiqueta='?';"
    values = (nombre_etiqueta,)
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query, values)
        res = cursor.fetchone()
        con.close()
        return res if res is None else res[0]
        
    except Error as e:
        print(e)


def insertar_guardadas(id_usuario,id_imagen):
    '''
    Guarda en la base de datos que un usuario le dio 'me gusta' a una imagen
    de otro usuario
    '''
    query = "INSERT INTO MeGusta (id_usuario, id_imagen) VALUES(?,?);"
    values = (id_usuario, id_imagen)
    try:
        con = conectar()
        cursorObj= con.cursor()
        cursorObj.execute(query, values)
        con.commit()
        con.close()
    except Error as e:
        print(e)


def eliminar_guardadas(id_usuario, id_imagen):
    '''
    Registra en la base de datos que a un usuario ya no le gusta una imagen
    de otro usuario
    '''
    query = "DELETE FROM MeGusta WHERE id_usuario=? AND id_imagen=?;"
    values = (id_usuario, id_imagen)
    try:
        con = conectar()
        cursorObj = con.cursor()
        cursorObj.execute(query, values)
        con.commit()
        con.close
    except Error:
        print(Error)


def insertar_imagen_etiqueta(id_imagen, id_etiqueta):
    '''
    Asocia una imagen a una etiqueta en la base de datos
    '''
    query = """INSERT INTO Imagenes_Etiquetas (id_imagen, id_etiqueta) 
               VALUES (?, ?);"""
    values = (id_imagen, id_etiqueta)
    try:
        con = conectar()
        cursorObj = con.cursor()
        cursorObj.execute(query, values)
        con.commit()
        con.close
    except Error as e:
        print(e)


def eliminar_imagen_etiqueta(id_imagen, id_etiqueta):
    '''
    Elimina la asociación entre una imagen y una etiqueta
    '''
    query = "DELETE Imagenes_Etiquetas WHERE id_imagen=? AND id_etiqueta=?);"
    values = (id_imagen, id_etiqueta)
    try:
        con = conectar()
        cursorObj = con.cursor()
        cursorObj.execute(query, values)
        con.commit()
        con.close
        
    except Error as e:
        print(e)


def insertar_imagen(nombre_imagen, id_usuario, ruta, privada, etiquetas):
    '''
    Inserta una imagen en la base de datos
    '''
    query = """INSERT INTO Imagenes (nombre_imagen, id_usuario, ruta, privada)
               VALUES('?', ?, '?', ?);"""
    values = (nombre_imagen, id_usuario, ruta, 1 if privada else 0)
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query, values)            
        con.commit()
        con.close()

    except Error as e:
        print(e)


def get_id_imagen(ruta):
    '''
    Retorna el id de una imagen dada su ruta
    '''
    query = "SELECT id FROM Imagenes WHERE ruta='?';"
    values = (ruta,)
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute(query, values)
        res = cursor.fetchone()
        con.close()
        return res if res is None else res[0]
        
    except Error as e:
        print(e)


def actualizar_imagen(id_, nombre_imagen, ruta, privada, etiquetas):
    '''
    Actualiza los datos de una imagen en la base de datos
    '''
    query = """UPDATE Imagenes 
               SET nombre_imagen='?', ruta='?', privada=?
               WHERE id=?;"""
    values = (nombre_imagen, ruta, 1 if privada else 0, id_)
    try:
        con = conectar()
        cursorObj = con.cursor()
        cursorObj.execute(query, values)
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
    '''
    Elimina los datos de una imagen de la base de datos, incluyendo sus
    asociaciones a etiquetas y a usuarios que le dieron 'me gusta'
    '''
    # 1. Eliminar referencias a la imagen en la tabla MeGusta
    # 2. Eliminar referencias a la imagen en la tabla Imagenes_etiquetas
    # 3. Eliminar registro en tabla Imagenes
    queries =  [
        "DELETE FROM MeGusta WHERE id_imagen=?;",
        "DELETE FROM Imagenes_Etiquetas WHERE id_imagen=?;",
        "DELETE FROM Imagenes WHERE id=?;"
    ]
    values = (id_,)
    try:
        con = conectar()
        cursorObj = con.cursor()
        for query in queries: 
            cursorObj.execute(query, values)
        con.commit()
        con.close()
    except Error as e:
        print(e)
