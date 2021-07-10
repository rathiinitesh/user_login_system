from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from user_login_system.config import Config


app = Flask(__name__)
app.config.from_object(Config)


db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail(app)


from user_login_system.user.routes import users
from user_login_system.main.routes import main
from user_login_system.errors.handlers import errors

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(errors)
