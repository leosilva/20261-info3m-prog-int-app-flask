from app import app
from flask import render_template, redirect, flash, request, url_for, session
from secrets import token_urlsafe
from urllib.parse import urljoin

from app.forms.login_form import LoginForm
from app.forms.usuario_form import UsuarioForm
from app.forms.post_form import Postform
from app.services.AuthenticationService import AuthenticationService
from app.services.UsuarioService import UsuarioService
from app.services.PostService import PostService
from app.services.SuapAuthenticationService import SuapAuthenticationService
from flask_login import login_required


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/endereco')
def endereco():
    return render_template('endereco.html')


@app.route('/logout', methods=['GET'])
def logout():
    success = AuthenticationService.logout()
    session.clear()
    if not success:
        flash("Erro ao realizar logout.", "error")
    return redirect(url_for("home"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        if AuthenticationService.login(formulario):
            flash("Login efetuado com sucesso!", category="success")
            next_page = request.args.get('next')
            if not next_page:
                return redirect(url_for('home'))
            return redirect(next_page)
        else:
            flash("Usuário ou senha inválidos.", category="error")
    return render_template('login.html', 
                           title='Login', 
                           form=formulario)


@app.route('/login-suap')
def login_suap():
    state = token_urlsafe(32)
    redirect_uri = request.host_url.rstrip('/') + url_for('suap_callback')
    session['suap_oauth_state'] = state
    return redirect(SuapAuthenticationService.authorization_url(state, redirect_uri))


@app.route('/suap/callback')
def suap_callback():
    state = session.pop('suap_oauth_state', None)
    if request.args.get('error') or not state or state != request.args.get('state', ''):
        flash('Falha na autenticação do SUAP.', 'error')
        return redirect(url_for('login'))

    code = request.args.get('code')
    if not code:
        flash('Código de autorização do SUAP não recebido.', 'error')
        return redirect(url_for('login'))

    redirect_uri = request.host_url.rstrip('/') + url_for('suap_callback')
    tokens = SuapAuthenticationService.exchange_code(code, redirect_uri)
    if not tokens or not tokens.get('access_token'):
        flash('Não foi possível obter o token do SUAP.', 'error')
        return redirect(url_for('login'))

    dados = SuapAuthenticationService.meus_dados(tokens['access_token'])
    if dados is None:
        flash('Não foi possível consultar os dados do SUAP.', 'error')
        return redirect(url_for('login'))

    usuario = AuthenticationService.login_suap(dados)
    if usuario is None:
        flash('Não foi possível vincular esta conta SUAP a um usuário local.', 'error')
        return redirect(url_for('login'))

    foto = dados.get('url_foto_75x100') or dados.get('url_foto') or dados.get('foto')
    foto_url = urljoin(app.config['SUAP_URL'] + '/', foto) if foto else None
    return render_template('suap_eu.html', title='Perfil SUAP', dados=dados, foto_url=foto_url)
    

@app.route('/inserir', methods=['GET', 'POST'])
@login_required
def inserir_usuario():
    formulario = UsuarioForm()
    if formulario.validate_on_submit():
        if UsuarioService.salvar(formulario):
            flash("Usuario cadastrado com sucesso!", category="success")
            return redirect(url_for('login'))
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
@login_required
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
