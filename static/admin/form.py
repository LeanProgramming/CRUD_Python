from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class Formulario(FlaskForm):
    #campos del formulario
    apellido = StringField('Apellido', validators = [DataRequired()])
    nombre = StringField('Nombre', validators = [DataRequired()])
    locacion = SelectField(u'Locación', choices=[], coerce = int)
    submit = SubmitField('Confirmar')