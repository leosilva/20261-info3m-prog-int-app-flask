from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class Postform(FlaskForm):
    body = TextAreaField('Postagem', validators=[DataRequired(message="A postagem é obrigatória")])
    submit = SubmitField('Enviar')