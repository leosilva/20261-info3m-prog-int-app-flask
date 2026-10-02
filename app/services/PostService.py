from app import db
from app.models import Post
import sqlalchemy as sa

class PostService():
    def salvar(form, usuario):
        try:
            post = Post()
            form.populate_obj(post)
            post.author = usuario
            db.session.add(post)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(e)
            return False