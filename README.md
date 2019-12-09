# flask-project
Flask project for a class subject. Deployed the server and the database in free Heroku. The main purpose for the project was to create a free library that anyone could use to downloads books. 

The project is uploaded **without** the database URI, the SECRET KEY, the GMAIL account and the Telegram Bot.
URL: https://desarrollo-libreria.herokuapp.com/


![INDEX](/imgs/img1.png)

### Used packages
* Flask
  * Babel
  * Blueprint
  * Flask-babel
  * Flask-Mail 
  * pyTelegramBotApi
  * SQLAlchemy (ORM)
  * Gunicorn
* Jinja2
* Bootstrap


### SCREENSHOTS
![CONTACT](/imgs/img2.png)
![REGISTER](/imgs/img3.png)
![MY BOOKS](/imgs/img4.png)

### How to run
* First of all, install the requirements: ```pip3 install -r requirements.txt```
* You need to change the code in flaskr/__init__.py and you need to add the SECRET_KEY, the GMAIL account, the bot and the most important, the **URI** for the database. For the database part, the project uses SQLAlchemy so is simple to change between SQL databases and the you can use ```flask init-db```to create the database structure.
* Finally you can run for "production" environment (Use the command in the base of the project): ```flask run``` 

If you have any problem, you may contact me.

### Phonegap
For this part I used a reduced part of the project (Index) to create an APK for Android. I used a small part of the project because the project uses Jinja2 that is incompatible with Phonegap. 
 * APK
 * Client: The part that was uploaded to Phonegap to create the apk.
 * Server: Which is a reduced part (Only the index) of the main project an instead using Jinja2 uses a JS to return the books.

### Resources
* https://flask-sqlalchemy.palletsprojects.com/
* https://getbootstrap.com/docs/
* https://docs.sqlalchemy.org/en/13/core/dml.html

### Projects used as examples
* https://github.com/pallets/flask-sqlalchemy
