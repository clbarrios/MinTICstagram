from flask import Flask, render_template, request, redirect, flash, url_for, current_app, g, send_file, session
import yagmail as yagmail
import utils
from credenciales import app_mail, app_password
from forms import FormRegistro
from forms import FormInicio
import os
from functools import wraps
from werkzeug import secure_filename
from db import *
from werkzeug.security import generate_password_hash, check_password_hash
import secrets


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = "./static/img"



galeria1 = ['img/imagen1.jpg', 'img/imagen2.png', 'img/imagen3.jpg', 'img/imagen4.jpg', 'img/imagen5.jpg', 'img/imagen6.jpg', 'img/imagen7.jpg', 'img/imagen8.jpg', 'img/imagen9.jpg', 'img/imagen10.jpg', 'img/imagen11.jpg', 'img/imagen12.jpg', 'img/imagen13.jpg','img/imagen14.jpg', 'img/imagen15.jpg', 'img/imagen15.jpg' ]
galeria2 = ['img/imagen2.png', 'img/imagen3.jpg', 'img/imagen4.jpg', 'img/imagen5.jpg', 'img/imagen6.jpg', 'img/imagen7.jpg', 'img/imagen7.jpg', 'img/imagen9.jpg', 'img/imagen10.jpg', 'img/imagen11.jpg', 'img/imagen12.jpg', 'img/imagen13.jpg', 'img/imagen14.jpg','img/imagen15.jpg', 'img/imagen1.jpg', 'img/imagen2.png' ]
galeria3 = ['img/imagen3.jpg', 'img/imagen4.jpg', 'img/imagen5.jpg', 'img/imagen6.jpg', 'img/imagen7.jpg', 'img/imagen8.jpg', 'img/imagen9.jpg', 'img/imagen10.jpg', 'img/imagen11.jpg', 'img/imagen12.jpg', 'img/imagen13.jpg', 'img/imagen14.jpg', 'img/imagen15.jpg','img/imagen1.jpg', 'img/imagen2.png', 'img/imagen3.jpg' ]

def login_required(view):
    @wraps(view)
    def wrapped_view(*arg, **kwargs):
        if g.user is None:
            return redirect(url_for( 'ingreso' ))
        return view(*arg, **kwargs)
    return wrapped_view

@app.route("/upload", methods=('GET', 'POST'))
@login_required
def upload():
    if request.method == 'GET':
        return redirect('/principal')
    else:
        f = request.files['archivo']
        filename = secure_filename(f.filename)
        if(not filename):
            flash("no hay ningun archivo cargado")
            return redirect('/principal')
        
        nom_imagen =  request.form.get("nombre")
        ruta = "img/1" + str(filename)
        etiquetas =  request.form.get("etiquetas").split()
        if(request.form.get("privadas")):
            privada=1
        else:
            privada=0
        
        # Verifiacion de rutas duplicadas
        if validar_ruta(ruta):
            insertar_imagen(nom_imagen, 1, ruta, privada, etiquetas)
        else:
            flash("Ya subiste esta imagen")
            return redirect('/principal')

        flash("Se ha agregado su imagen con exito")
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], "1" + filename))
        return 'ok'


@app.route("/delete/<int:id>", methods=('GET', 'POST'))
@login_required
def delete(id):
    eliminar_imagen(id)
    return redirect('/principal')

@app.route("/deleteGusta/<int:id_imagen>", methods=('GET', 'POST'))
@login_required
def deleteGusta(id_imagen):
    eliminar_guardadas(1, id_imagen)
    return redirect('/principal')




@app.route('/', methods=("GET", "POST"))
def ingreso():
    form= FormInicio()
    if g.user:
        return redirect(url_for( 'principal' ))
    if request.method == "POST":
        usuario = request.form.get('usuario')
        clave = request.form.get('contraseña')
        db = conectar()
              
        user = get_usuario(usuario)

        if user is None:
                error = 'Usuario o contraseña inválidos'
        else:
            if check_password_hash(user['contraseña'], clave):
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('principal'))
        #flash( error )
        
        #if utils.isUsernameValid2(usuario) and utils.isPasswordValid2(clave):
        #    return redirect(url_for('principal'))
        #else:
        #    flash("Error en los datos. Vuelve a intentar.")
        #    return render_template('ingreso.html', form= form)
    
    return render_template('ingreso.html', form= form)   
  

@app.route('/registro', methods=('GET','POST'))
def registro():
    form = FormRegistro()
    titulo = 'MinTICstagram | Registro'
    if request.method == "POST":

        nom = request.form.get('nombre')
        cor = request.form.get('correo')
        con = request.form.get('contraseña')
        cfcon = request.form.get('conf_contraseña')

        if validar_nuevo_usuario(nom,cor)[0] != "OK":
            flash(validar_nuevo_usuario(nom,cor)[0])
            return render_template('registro.html', title=titulo, form=form)
        
        if not utils.isUsernameValid(nom):
            flash("El usuario que escogiste no es un usuario válido. Vuelve a intentar.")
            return render_template('registro.html', title=titulo, form=form)
        
        if not utils.isPasswordValid(con):
            flash("La contraseña que escogiste no es un contraseña válida. Vuelve a intentar.")
            return render_template('registro.html', title=titulo, form=form)

        if not utils.isEmailValid(cor):
            flash("El correo que escribiste no es un correo válido. Vuelve a intentar.")
            return render_template('registro.html', title=titulo, form=form)
        
        if con != cfcon:
            flash("Las contraseñas no coinciden")
            return render_template('registro.html', title=titulo, form=form)
        
        hash_password = generate_password_hash(con)
        print(nom, cor, hash_password)
        insertar_usuario(nom, cor, hash_password)

        yag = yagmail.SMTP(app_mail, app_password)
        yag.send(to=cor,subject="Activa tu cuenta",contents="Hola, Bienvenido a MinTinstagram, has click en el siguiente link para activar tu cuenta </br><br> <a href='http://127.0.0.1:5000/activacionExitosa' >ACTIVA TU CUENTA </a>")
        
        return redirect('/activacion')
    
    return render_template('registro.html', title=titulo, form=form)

@app.route("/activacion")
def activacion():
    return render_template("activacion.html")

@app.route("/activacionExitosa")
def activacionExitosa():
    return render_template("activacionExitosa.html")

@app.route("/reestablecerContra", methods=('GET','POST'))
def reestablecerContra():
    if request.method== 'POST':
        correo=request.form.get("correoRes")

        if not utils.isEmailValid(correo):
            flash("Escribe un correo valido")
            return render_template("reestablecerContra.html")
        yag = yagmail.SMTP(app_mail, app_password)
        yag.send(to=correo,subject="Reestablece tu contraseña",contents="Hola, Usa el link para cambiar tu contraseña.")
        flash("Se envio un correo para que cambies tu contraseña")
    return render_template("reestablecerContra.html")
    
    


@app.route("/nuevaContra")
def nuevaContra():
    return render_template("nuevaContra.html")

@app.route("/reestablecimientoExitoso")
def reestablecimientoExitoso():
    return render_template("reestablecimientoExitoso.html")


@app.route("/principal/")
@login_required
def principal():
    img_privadas = get_imagenes(1, 1)
    img_publicas = get_imagenes(1, 0)
    img_guardadas = get_guardadas(1)
    
    return render_template("principal.html",  galeria1=img_privadas, galeria2=img_publicas, galeria3=img_guardadas)

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_usuario_byID(user_id)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('ingreso'))


# Activar el modo debug
if __name__=="__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)
