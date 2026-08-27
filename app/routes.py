from app import app
from flask import render_template, redirect, flash

from app.forms.login_form import LoginForm
from app.forms.usuario_form import UsuarioForm
from app.services.AuthenticationService import AuthenticationService
from app.services.UsuarioService import UsuarioService


@app.route('/')
def home():
    usuario = {
        "nome": "Leo",
        "produtos": ["Banana", "Abacaxi", "Melancia"]
    }
    esta_logado = True
    return render_template("index.html", pessoa = usuario,
                           usuario_logado = esta_logado)


@app.route('/sobre')
def sobre():
    return "Página sobre"

@app.route('/endereco')
def endereco():
    return "<h1>Meu endereço</h1>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        if AuthenticationService.login(formulario):
            flash("Login efetuado com sucesso!")
            return redirect("/")
        else:
            flash("Erro nas credenciais.")
            return redirect("/login")
    return render_template('login.html', 
                           title='Login', 
                           form=formulario)
    

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_usuario():
    formulario = UsuarioForm()
    if formulario.validate_on_submit():
        if UsuarioService.salvar(formulario):
            flash("Usuario cadastrado com sucesso!")
            return redirect("/")
        else:
            flash("Usuário não cadastrado.")
            return redirect("/cadastrar")
    return render_template('cadastro_usuario.html', 
                            title='Cadastro de Usuário', 
                            form=formulario)