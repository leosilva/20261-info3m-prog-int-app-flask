from app.models.usuario import Usuario
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash


class AuthenticationService():
    def login(form):
        username = form.username.data.strip()
        user = Usuario.query.filter_by(username=username).first()
        
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user, remember=form.remember_me.data)
                return True    
        return False
    
    def logout():
        return logout_user()