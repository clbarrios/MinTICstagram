from flask import Flask, render_template, request, redirect, flash, url_for
from flask import Flask, request, redirect, render_template
import yagmail as yagmail
import utils
from credenciales import app_mail, app_password
from forms import FormRegistro
from forms import FormInicio
import os
from werkzeug import secure_filename
from db import *


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = "./static/img"



galeria1 = ['img/imagen1.jpg', 'img/imagen2.png', 'img/imagen3.jpg', 'img/imagen4.jpg', 'img/imagen5.jpg', 'img/imagen6.jpg', 'img/imagen7.jpg', 'img/imagen8.jpg', 'img/imagen9.jpg', 'img/imagen10.jpg', 'img/imagen11.jpg', 'img/imagen12.jpg', 'img/imagen13.jpg','img/imagen14.jpg', 'img/imagen15.jpg', 'img/imagen15.jpg' ]
galeria2 = ['img/imagen2.png', 'img/imagen3.jpg', 'img/imagen4.jpg', 'img/imagen5.jpg', 'img/imagen6.jpg', 'img/imagen7.jpg', 'img/imagen7.jpg', 'img/imagen9.jpg', 'img/imagen10.jpg', 'img/imagen11.jpg', 'img/imagen12.jpg', 'img/imagen13.jpg', 'img/imagen14.jpg','img/imagen15.jpg', 'img/imagen1.jpg', 'img/imagen2.png' ]
galeria3 = ['img/imagen3.jpg', 'img/imagen4.jpg', 'img/imagen5.jpg', 'img/imagen6.jpg', 'img/imagen7.jpg', 'img/imagen8.jpg', 'img/imagen9.jpg', 'img/imagen10.jpg', 'img/imagen11.jpg', 'img/imagen12.jpg', 'img/imagen13.jpg', 'img/imagen14.jpg', 'img/imagen15.jpg','img/imagen1.jpg', 'img/imagen2.png', 'img/imagen3.jpg' ]



@app.route("/upload", methods=('GET', 'POST'))
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
        listaImg=get_todas_imagenes(1)
        
        for i in listaImg:
            if i['ruta'] == ruta:
                flash("Ya subiste esta imagen")
                return redirect('/principal')
            

        insertar_imagen(nom_imagen, 1, ruta, privada, etiquetas)

        flash("Se ha agregado su imagen con exito")
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], "1" + filename))
        return 'ok'

@app.route("/delete", methods=('GET', 'POST'))
def delete(rutaImg):
    idImg = get_id_imagen(rutaImg)
    eliminar_imagen(idImg)


@app.route("/", methods=("GET", "POST"))
def ingreso():
    '''if request.method == "POST":
        usuario = request.form.get("usuario")
        clave = request.form.get("clave")

        if utils.isUsernameValid2(usuario) and utils.isPasswordValid2(clave):
            return redirect(url_for('principal'))
        else:
            flash("Error en los datos. Vuelve a intentar.")
    return render_template("ingreso.html")'''
    form= FormInicio()
    if form.validate_on_submit():
        usuario=form.usuario.data
        clave=form.contraseña.data
        if utils.isUsernameValid2(usuario) and utils.isPasswordValid2(clave):
            return redirect(url_for('principal'))
        else:
            flash("Error en los datos. Vuelve a intentar.")
            return render_template('ingreso.html', form= form)
    return render_template('ingreso.html', form= form)   
  

@app.route('/registro', methods=('GET','POST'))
def registro():
    form = FormRegistro()
    titulo = 'MinTICstagram | Registro'
    if form.validate_on_submit():
        
        username = form.nombre.data
        email = form.correo.data
        password = form.contraseña.data
        conf_password = form.conf_contraseña.data
        
        if not utils.isUsernameValid(username):
            flash("El usuario que escogiste no es un usuario válido. Vuelve a intentar.")
            return render_template('registro.html', title=titulo, form=form)
        
        if not utils.isPasswordValid(password):
            flash("La contraseña que escogiste no es un contraseña válida. Vuelve a intentar.")
            return render_template('registro.html', title=titulo, form=form)

        if not utils.isEmailValid(email):
            flash("El correo que escribiste no es un correo válido. Vuelve a intentar.")
            return render_template('registro.html', title=titulo, form=form)
        
        if password != conf_password:
            flash("Las contraseñas no coinciden")
            return render_template('registro.html', title=titulo, form=form)

        
        yag = yagmail.SMTP(app_mail, app_password)
        yag.send(to=email,subject="Activa tu cuenta",contents="Hola, Bienvenido a MinTinstagram, has click en el siguiente link para activar tu cuenta </br><br> <a href='http://127.0.0.1:5000/activacionExitosa' >ACTIVA TU CUENTA </a>")
        nom = request.form.get('nombre')
        cor = request.form.get('correo')
        con = request.form.get('contraseña')
        insertar_usuario(nom, cor, con)
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
def principal():
    img_privadas = get_imagenes(1, 1)
    img_publicas = get_imagenes(1, 0)
    img_guardadas = get_guardadas(1)
    
    return render_template("principal.html",  galeria1=img_privadas, galeria2=img_publicas, galeria3=img_guardadas)

# Activar el modo debug
if __name__=="__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)
