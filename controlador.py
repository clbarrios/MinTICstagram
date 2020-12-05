from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hola_mundo():
    return render_template("activacion.html")