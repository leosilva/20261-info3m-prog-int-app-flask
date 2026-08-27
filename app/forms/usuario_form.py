from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, EqualTo, ValidationError


class UsuarioForm(FlaskForm):
    nome_completo = StringField('Nome Completo', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirmação de Senha', 
                                      validators=[DataRequired(), EqualTo('senha')])
    submit = SubmitField('Entrar')
    
    def validate_nome_completo(self, field):
        if field.data.lower() == 'admin':
            raise ValidationError('O nome "admin" está reservado. Escolha outro.')