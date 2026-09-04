from app import db
from app.models import Usuario

class UsuarioService():
    def salvar(form):
        try:
            usuario = Usuario()
            usuario.username = form.nome_completo.data
            usuario.email = form.email.data
            usuario.password_hash = form.senha.data
            db.session.add(usuario)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(e)
            return False