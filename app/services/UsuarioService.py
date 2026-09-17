from app import db
from app.models import Usuario
import sqlalchemy as sa

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
        
        
    def buscar_por_email(email):
        query = sa.select(Usuario).where(Usuario.email == email)
        usuario = db.session.scalar(query)
        if usuario:
            return usuario
        return None

    def listar():
        query = sa.select(Usuario).order_by(Usuario.username)
        return db.session.scalars(query).all()
    
    def atualizar(usuario):
        try:
            usuario.email = "outro_email@email.com"
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(e)
            return False
