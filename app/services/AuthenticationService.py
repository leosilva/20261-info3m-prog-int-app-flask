from app import db
from app.models.usuario import Usuario
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash


class AuthenticationService():
    def login(form):
        username = form.username.data.strip()
        user = Usuario.query.filter_by(username=username).first()
        
        if user and user.password_hash:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user, remember=form.remember_me.data)
                return True
        return False
    
    def logout():
        return logout_user()

    def login_suap(dados):
        username = str(dados.get('matricula') or dados.get('username') or dados.get('email'))
        email = dados.get('email') or f'{username}@suap.local'
        user = Usuario.query.filter(
            (Usuario.username == username) | (Usuario.email == email)
        ).first()

        if not user:
            user = Usuario(username=username, email=email)
            db.session.add(user)
            db.session.commit()

        login_user(user)
        return user
