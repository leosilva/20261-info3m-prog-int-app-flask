from app import db
from app.models import Usuario
import sqlalchemy as sa
from werkzeug.security import generate_password_hash

class UsuarioService():
    def salvar(form):
        try:
            usuario = Usuario()
            form.populate_obj(usuario)
            usuario.password_hash = generate_password_hash(form.password.data)
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

    
    def buscar_por_id(id):
        usuario = Usuario.query.get(id)
        return usuario


    def listar():
        query = sa.select(Usuario)
        return db.session.scalars(query).all()
    
    def atualizar(usuario, form):
        try:
            form.populate_obj(usuario)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(e)
            return False
        
    def remover(usuario):
        try:
            db.session.delete(usuario)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(e)
            return False
        
        
    def checar_unicidade(campo, tipo):
        if tipo == 'username':
            if Usuario.query.filter_by(username=campo).first():
                return False
        if tipo == 'email':
            if Usuario.query.filter_by(email=campo).first():
                return False
        return True