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
        suap_id = str(dados.get('matricula') or dados.get('username') or dados.get('email') or '').strip()
        if not suap_id:
            return None

        username = str(dados.get('nome_usual') or dados.get('nome') or '').strip()
        email = dados.get('email') or f'{username}@suap.local'
        user = Usuario.query.filter_by(suap_id=suap_id).first()

        if not user:
            user = Usuario.query.filter((Usuario.username == username) | (Usuario.email == email)).first()

        if user and user.suap_id and user.suap_id != suap_id:
            return None

        if not user:
            user = Usuario(username=username, email=email, suap_id=suap_id)
            db.session.add(user)
        else:
            user.suap_id = suap_id

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return None

        login_user(user)
        return user
