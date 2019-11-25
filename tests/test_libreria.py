import pytest

from flaskr import db
from flaskr.auth.models import Usuario
from flaskr.libreria.models import Libro
from io import BytesIO

def test_index(client, auth):
    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/")
    assert b"Libreria FDR" in response.data


@pytest.mark.parametrize("path", ("/create", "/1/delete"))
def test_login_required(client, path):
    print(path)
    response = client.get(path)
    assert response.headers["Location"] == "http://localhost/auth/login"


def test_exists_required(client, auth):
    auth.login()
    assert client.get("/9999/delete").status_code == 404


#def test_create(client, auth, app):
#    auth.login()
#    assert client.get("/create").status_code == 200
#    response = client.post("/create", content_type='multipart/form-data', 
#            data={"name": "title", 
#                "autor": "test", 
#                "image":(BytesIO(b'my file contents'), 'test_file1.jpg'), 
#                "PDF":(BytesIO(b'my fileasda contents'), 'test_file.pdf'), 
#                "EPUB":(BytesIO(b'my file contents'), 'test_file.epub'), 
#                "categoriaId":1,
#                "usuarioId":1})
#    print(response.data)
#    assert b'title' in (client.get("/").data) 

#def test_delete(client, auth, app):
#    auth.login()
#    response = client.post("/create", data={"id":20, "name": "title", "autor": "test", "image":"IMAGECODE", "PDF":"PDFCODE", "EPUB": "EPUBCODE", "categoriaId": "1"})
#    response = client.get("/") 
#    assert b'title' in response.data 
#    print(response.data )
#    print( response.headers["Location"])
#    assert response.headers["Location"] == "http://localhost/"
#    response = client.get("/20/delete")
#    print(response)
#    assert b'borrado' in (response.data) 
