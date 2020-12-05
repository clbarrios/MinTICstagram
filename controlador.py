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

@app.route("/reestablecimientoExitoso")
def reestablecimientoExitoso():
    return render_template("reestablecimientoExitoso.html")

@app.route("/principal")
def principal():
    return render_template("principal.html")

@app.route("/actualizarImagen")
def actualizarImagen():
    return render_template("actualizarImagen.html")

@app.route("/nuevaImagen")
def nuevaImagen():
    return render_template("nuevaImagen.html")

# Activar el modo debug
if __name__=="__main__":
    app.run(debug=True)
