from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def ingreso():
    return render_template("ingreso.html")

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/activacion")
def activacion():
    return render_template("activacion.html")

@app.route("/activacionExitosa")
def activacionExitosa():
    return render_template("activacionExitosa.html")

@app.route("/reestablecerContra")
def reestablecerContra():
    return render_template("reestablecerContra.html")

@app.route("/nuevaContra")
def nuevaContra():
    return render_template("nuevaContra.html")

@app.route("/reestablecimientoExitoso")
def reestablecimientoExitoso():
    return render_template("reestablecimientoExitoso.html")

galeria = ['img/imagen1.jpg', 'img/imagen2.png', 'img/imagen3.jpg', 'img/imagen4.jpg', 'img/imagen5.jpg', 'img/imagen6.jpg', 'img/imagen7.jpg', 'img/imagen8.jpg', 'img/imagen9.jpg', 'img/imagen10.jpg', 'img/imagen11.jpg', 'img/imagen12.jpg', 'img/imagen13.jpg','img/imagen14.jpg', 'img/imagen15.jpg', 'img/imagen15.jpg' ]

@app.route("/principal/")
def principal():
    return render_template("principal.html", galeria=galeria)

# Activar el modo debug
if __name__=="__main__":
    app.run(debug=True)
