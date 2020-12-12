from flask import Flask, render_template, request, redirect, flash, url_for
from flask import Flask, request, redirect, render_template
import yagmail as yagmail
import utils
from credenciales import app_mail, app_password
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods=("GET", "POST"))
def ingreso():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        clave = request.form.get("clave")

        if utils.isUsernameValid2(usuario) and utils.isPasswordValid2(clave):
            return redirect(url_for('principal'))
        else:
            flash("Error en los datos. Vuelve a intentar.")
    return render_template("ingreso.html")

@app.route('/registro', methods=('GET','POST'))
def registro():
    if request.method== 'POST':
        username=request.form.get("nombre")
        password=request.form.get("password")
        email=request.form.get("correo")
        
        if not utils.isUsernameValid(username):
            flash("El usuario que escogiste no es un usuario válido. Vuelve a intentar.")
            return render_template('registro.html')
        
        if not utils.isPasswordValid(password):
            flash("La contraseña que escogiste no es un contraseña válida. Vuelve a intentar.")
            return render_template('registro.html')

        if not utils.isEmailValid(email):
            flash("El correo que escribiste no es un correo válido. Vuelve a intentar.")
            return render_template('registro.html')
        
        yag = yagmail.SMTP(app_mail, app_password)
        yag.send(to=email,subject="Activa tu cuenta",contents="Bienvenido, usa el link para activar tu cuenta")
        return redirect('/activacion')
    
    return render_template("registro.html")

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

galeria1 = ['img/imagen1.jpg', 'img/imagen2.png', 'img/imagen3.jpg', 'img/imagen4.jpg', 'img/imagen5.jpg', 'img/imagen6.jpg', 'img/imagen7.jpg', 'img/imagen8.jpg', 'img/imagen9.jpg', 'img/imagen10.jpg', 'img/imagen11.jpg', 'img/imagen12.jpg', 'img/imagen13.jpg','img/imagen14.jpg', 'img/imagen15.jpg', 'img/imagen15.jpg' ]
galeria2 = ['img/imagen2.png', 'img/imagen3.jpg', 'img/imagen4.jpg', 'img/imagen5.jpg', 'img/imagen6.jpg', 'img/imagen7.jpg', 'img/imagen7.jpg', 'img/imagen9.jpg', 'img/imagen10.jpg', 'img/imagen11.jpg', 'img/imagen12.jpg', 'img/imagen13.jpg', 'img/imagen14.jpg','img/imagen15.jpg', 'img/imagen1.jpg', 'img/imagen2.png' ]
galeria3 = ['img/imagen3.jpg', 'img/imagen4.jpg', 'img/imagen5.jpg', 'img/imagen6.jpg', 'img/imagen7.jpg', 'img/imagen8.jpg', 'img/imagen9.jpg', 'img/imagen10.jpg', 'img/imagen11.jpg', 'img/imagen12.jpg', 'img/imagen13.jpg', 'img/imagen14.jpg', 'img/imagen15.jpg','img/imagen1.jpg', 'img/imagen2.png', 'img/imagen3.jpg' ]

@app.route("/principal/")
def principal():
    return render_template("principal.html", galeria1=galeria1, galeria2=galeria2, galeria3=galeria3)

# Activar el modo debug
if __name__=="__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)
