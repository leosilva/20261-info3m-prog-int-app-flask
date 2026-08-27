from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, EqualTo


class UsuarioForm(FlaskForm):
    nome_completo = StringField('Nome Completo', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirmação de Senha', 
                                      validators=[DataRequired(), EqualTo('senha')])
    submit = SubmitField('Entrar')