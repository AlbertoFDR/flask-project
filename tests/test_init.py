from flaskr import create_app

def test_config():
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing

def test_db_url_environ(monkeypatch):
    app = create_app()
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "postgres://mpdtsnsxkjdlrr:695db0227af0a0e70674816e7f7b5c351e8b59aa44874c5ee11bd8078613b503@ec2-50-19-95-77.compute-1.amazonaws.com:5432/d285uv22g2uv47"

def test_init_db_command(monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True
    
    app = create_app()
    runner = app.test_cli_runner()
    monkeypatch.setattr("flaskr.init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    assert "Initialized" in result.output
    assert Recorder.called
