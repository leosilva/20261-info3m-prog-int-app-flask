from app import app
from flask import render_template, redirect, flash, request

from app.forms.login_form import LoginForm
from app.forms.usuario_form import UsuarioForm
from app.forms.post_form import Postform
from app.services.AuthenticationService import AuthenticationService
from app.services.UsuarioService import UsuarioService
from app.services.PostService import PostService


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/endereco')
def endereco():
    return render_template('endereco.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        if AuthenticationService.login(formulario):
            flash("Login efetuado com sucesso!")
            return redirect("/index2")
        else:
            flash("Erro nas credenciais.")
            return redirect("/login")
    return render_template('login.html', 
                           title='Login', 
                           form=formulario)
    

@app.route('/inserir', methods=['GET', 'POST'])
def inserir_usuario():
    formulario = UsuarioForm()
    if formulario.validate_on_submit():
        if UsuarioService.salvar(formulario):
            flash("Usuario cadastrado com sucesso!", category="success")
            return redirect("/")
        else:
            flash("Usuário não cadastrado.", category="warning")
            return redirect("/inserir")
    return render_template('usuario/cadastro_usuario.html', 
                            title='Cadastro de Usuário', 
                            form=formulario)
    

@app.route('/buscar_usuario', methods=['GET', 'POST'])
def buscar_usuario():
    if request.method == 'GET':
        return render_template('usuario/buscar_usuario.html')
    elif request.method == 'POST':
        email_a_buscar = request.form.get("email")
        if email_a_buscar:
            usuario = UsuarioService.buscar_por_email(email_a_buscar)
            print(usuario.username)
            print(usuario.email)
            UsuarioService.atualizar(usuario)
        return render_template("index.html")


@app.route('/listar_usuario')
def listar_usuario():
    usuarios = UsuarioService.listar()
    return render_template('usuario/listar_usuario.html', title='Listagem de Usuário', usuarios = usuarios)
                
    
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    usuario = UsuarioService.buscar_por_id(id)

    form = UsuarioForm(obj=usuario)
    if form.validate_on_submit():
        sucesso = UsuarioService.atualizar(usuario, form)
        if sucesso:
            flash("Usuário atualizado com sucesso!", category='success')
            return render_template('index.html')
        else:
            flash("Usuário não atualizado. Tente novamente mais tarde.", category='warning')
            return render_template("usuario/cadastro_usuario.html", form=form, editar=True)

    return render_template("usuario/cadastro_usuario.html", form=form, editar=True)    


@app.route('/remover/<int:id>', methods=['GET'])
def remover(id):
    usuario = UsuarioService.buscar_por_id(id)
    if usuario:
        removeu = UsuarioService.remover(usuario)
        if removeu:
            flash("Usuário removido com sucesso!", category='success')
        else:
            flash("Usuário não removido. Tente novamente mais tarde.", category='warning')
    else:
        flash("Usuário não encontrado. Tente novamente mais tarde.", category='warning')
    return redirect("/listar_usuario")


@app.route('/nova_postagem', methods=['GET', 'POST'])
def nova_postagem():
    formulario = Postform()
    if formulario.validate_on_submit():
        usuario = UsuarioService.buscar_por_id(1)
        if PostService.salvar(formulario, usuario):
            flash("Postagem realizada com sucesso!", category="success")
            return redirect("/")
        else:
            flash("Postagem nã orealizada.", category="warning")
            return redirect("/nova_postagem")
    return render_template('post/postagem.html', 
                            title='Nova Postagem', 
                            form=formulario)