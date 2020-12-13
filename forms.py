from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class FormRegistro(FlaskForm):
    nombre = StringField('Nombre de Usuario', validators= [DataRequired(message="Se requiere un nombre de usuario")])
    correo = StringField('Correo', validators= [DataRequired(message="Se requiere un Correo")])
    contraseña = PasswordField('Contraseña', validators= [DataRequired(message="Se requiere una contraseña")])
    conf_contraseña = PasswordField('Confirmar Contraseña', validators= [DataRequired(message="Confirme la contraseña")])
    registrar = SubmitField('¡Únete!')