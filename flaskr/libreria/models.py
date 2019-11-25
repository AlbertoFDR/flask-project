from flaskr import db
from flaskr.auth.models import Usuario
from flask import url_for

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

class Libro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    autor = db.Column(db.String(30), nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)
    PDF = db.Column(db.LargeBinary, nullable=False)
    EPUB = db.Column(db.LargeBinary, nullable=False)
    categoriaId = db.Column(db.ForeignKey('categoria.id'), nullable=False)
    usuarioId = db.Column(db.ForeignKey('usuario.id'), nullable=False)
    created = db.Column(
        db.DateTime, nullable=False, server_default=db.func.current_timestamp()
        ) 
    descargas = db.Column(db.Integer, default=0)

     # User object backed by author_id
    # lazy="joined" means the user is returned with the post in one query
    # autor = db.relationship(Usuario, lazy="joined", backref="posts")

    @property
    def delete_url(self):
        return url_for("libreria.delete", id=self.id)

    @property
    def download_url(self):
        return url_for("libreria.download", id=self.id)

    @property
    def download_pdf(self):
        return url_for("libreria.downloadpdf", id=self.id)

    @property
    def download_epub(self):
        return url_for("libreria.downloadepub", id=self.id)

