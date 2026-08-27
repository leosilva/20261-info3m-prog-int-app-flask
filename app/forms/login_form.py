from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(message="Por favor, preencha o seu nome")])
    password = PasswordField('Senha', validators=[DataRequired(message="Por favor, preencha a senha")])
    remember_me = BooleanField('Permanecer Conectado')
    submit = SubmitField('Entrar')