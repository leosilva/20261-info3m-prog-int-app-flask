from app import app
from flask import render_template

from app.forms.login_form import LoginForm


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
        print(formulario.username.data)
        print(formulario.password.data)
        return render_template("index.html")
    return render_template('login.html', 
                           title='Login', 
                           form=formulario)