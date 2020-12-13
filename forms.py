from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class FormRegistro(FlaskForm):
    usuario = StringField('Usuario', validators= [DataRequired(message="No dejar vacío")])
    correo = StringField('Correo', validators= [DataRequired(message="No dejar vacío")])
    contraseña = PasswordField('Contraseña', validators= [DataRequired(message="No dejar vacío")])
    conf_contraseña = PasswordField('Conf_Contraseña', validators= [DataRequired(message="No dejar vacío")])
    registrar = SubmitField('Registrar')