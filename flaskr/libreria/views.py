from flask import url_for, send_file, Blueprint, flash, redirect, render_template, request, g
from werkzeug.exceptions import abort

from flaskr import db
from flaskr.auth.views import login_required
from flaskr.libreria.models import Libro, Categoria
from flaskr.auth.models import Usuario

from base64 import b64encode
from io import BytesIO

bp = Blueprint("libreria", __name__)

#Index where appears a list of books
@bp.route("/")
def index():
    """Show all the books, most recent first."""
    libros = Libro.query.order_by(Libro.created.desc()).all()
    for libro in libros:
        #Encode the image to send by the network
        libro.image = b64encode(libro.image).decode('ascii')
    return render_template("libreria/index.html", libros=libros)

#Search a book
@bp.route('/explorar', methods=('GET','POST'))
def explorar():
   if request.method == 'POST':
        busqueda = request.form['busqueda'].lower()
        libroReturn = []
        libros = Libro.query.order_by(Libro.created.desc()).all()
        for libro in libros:
            #Encode the image to send by the network
            if busqueda in libro.name.lower() or busqueda in libro.autor.lower():
                libro.image = b64encode(libro.image).decode('ascii')
                libroReturn.append(libro)
        return render_template('explorar.html',libros=libroReturn) 
   return render_template('explorar.html')


def get_libro(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    libro = Libro.query.get_or_404(id, f"Post id {id} doesn't exist.")

    if check_author and libro.usuarioId != g.user.id:
        abort(403)

    return libro

@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new libro/book for the current user."""
    if request.method == "POST":
        titulo = request.form["titulo"] #title
        autorform = request.form["autor"] #Author
        pdf = request.files['pdf'] 
        imagen = request.files['portada'] #Coverpage
        epub = request.files["epub"] 
        categoria = request.form["categoria"] 
        #Search categoria id
        categoriaid = Categoria.query.filter_by(name=categoria).first().id
        error = None
        if not titulo:
            error = "Titulo is required."
        if error is not None:
            flash(error)
        else:
            db.session.add(Libro(name=titulo, autor=autorform, image=imagen.read(), EPUB=epub.read(), PDF=pdf.read(), categoriaId=categoriaid, usuarioId=g.user.id))
            db.session.commit()
            flash("Libro creado", "success")
            libros = Libro.query.order_by(Libro.created.desc()).all()
            return redirect(url_for("libreria.index", libros=libros ))

    return render_template("libreria/create.html", categorias=Categoria.query.all())


@bp.route("/<int:id>/download")
def download(id):
    """Download a book page"""
    libro = get_libro(id, check_author=False)
    libro.image = b64encode(libro.image).decode('ascii')
    return render_template("libreria/download.html", libro=libro)

#Download pdf button
@bp.route("/<int:id>/download/pdf")
def downloadpdf(id):
    libro = get_libro(id, check_author=False)
    libro.descargas = libro.descargas + 1
    db.session.commit()
    return send_file(BytesIO(libro.PDF), attachment_filename=libro.name + ".pdf", as_attachment=True)

#Download EPUB button
@bp.route("/<int:id>/download/epub")
def downloadepub(id):
    libro = get_libro(id, check_author=False) 
    return send_file(BytesIO(libro.EPUB), attachment_filename=libro.name + ".epub", as_attachment=True)

#See my (User's) books
@bp.route("/mybooks")
@login_required
def mybooks():
    libros = Libro.query.filter_by(usuarioId=g.user.id).order_by(Libro.created.desc()).all()
    return render_template("libreria/mybooks.html", libros=libros)

#Delete one of our books
@bp.route("/<int:id>/delete")
@login_required
def delete(id):
    """Delete a book.

    Ensures that the book exists and that the logged in user is the
    author of the post.
    """
    libro = get_libro(id) #This also checks that is the author
    db.session.delete(libro)
    db.session.commit()
    return redirect(url_for("libreria.index"))
