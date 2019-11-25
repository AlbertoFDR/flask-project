import click
import os
import telebot
import sys
from flask import Flask, render_template, request, flash, url_for, redirect, send_from_directory
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_recaptcha import ReCaptcha
from flask_babel import Babel
from flask import session

bot = telebot.TeleBot("BOT_ID")
db = SQLAlchemy()
mail = Mail()
recaptcha = ReCaptcha()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'SECRET_KEY'    
   
    #GMAIL configuration
    app.config.update(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME = 'USERNAME@gmail.com',
        MAIL_PASSWORD = 'PASS'
    )
    
    #ReCaptcha configuration
    app.config.update({'RECAPTCHA_ENABLED': True,
        'RECAPTCHA_SITE_KEY': 'SITE_KEY',
        'RECAPTCHA_SECRET_KEY':'SECRET_KEY'}
    )

    #DATABASE CONFIGURATION
    app.config.from_mapping(
        # default secret that should be overridden in environ or config
        #SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI="URI",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    
    #Babel config
    #app.config['BABEL_DEFAULT_LOCALE'] = 'eus'
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        """
            Flask-Babel
            Return the prefer lang by the user or the best match
        """
        try:
            lang = session['lang']
        except KeyError:
            lang = None 
        if lang is not None:
                return lang
        return request.accept_languages.best_match(['es','en','eu_ES'])

    @app.route('/language/<language>')
    def set_language(language=None):
        """
            A way to save user prefer language
        """
        session['lang'] = language
        return redirect(url_for('index'))

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
   
    # initialize Flask-SQLAlchemy and the init-db command
    db.init_app(app)
    app.cli.add_command(init_db_command)

    #Initialize Recaptcha
    recaptcha.init_app(app)

    # apply the blueprints to the app
    from flaskr import auth, libreria

    app.register_blueprint(auth.bp)
    app.register_blueprint(libreria.bp)

    # make "index" point at "/", which is handled by "blog.index"
    app.add_url_rule("/", endpoint="index")

    # Contact page with the 2 forms (Telegram, Email)
    @app.route('/telegram', methods=('GET','POST'))
    def telegram():
       if request.method == 'POST':
            form_name = request.form['form-name']
            if form_name=="Enviar correo":
                mail = Mail(app)
                msg = mail.send_message(
                    sender='SENDER@gmail.com',
                    recipients=['RECIPIENT@gmail.com'],
                    body=request.form['mensaje'],
                    subject=request.form['asunto']
                )
            if form_name=="Enviar telegram":
                nombre = request.form['nombre']
                texto = request.form['texto']
                chatid ='CHAT_ID'
                bot.send_message(chatid, nombre + ": " + texto)

            flash('Mensaje enviado existosamente', "success")
            return render_template('telegram.html') 
       return render_template('telegram.html')
    
    return app

#Inits the database with the models
def init_db():
    db.drop_all()
    db.create_all()


#If we do "flask init-db" it creates the database
@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


