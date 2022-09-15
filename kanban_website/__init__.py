import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah'
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    if test_config:
        app.config.update(test_config)

    db.init_app(app)


    from .functionality import views
    from .authentication import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .DBmodel import User, Task

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app, db_nm=DB_NAME):
    if not path.exists('website/' + db_nm):
        db.create_all(app=app)
        print('Database is successfully created.')
