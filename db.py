import sqlite3
from sqlite3 import Error
from flask import current_app, g

def conectar():
    try:
        if 'db' not in g:
            g.db = sqlite3.connect('BaseDeDatos')
            return g.db
    except Error:
        print(Error)

def desconectar():
    try:
        db = g.pop('db', None)
        if db is not None:
            db.close()
