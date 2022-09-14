import os
import tempfile
import pytest
import sys
from flask import json
from werkzeug.security import generate_password_hash
from tests import test_credentials
sys.path.append('../')
from kanban_website import create_app, db, DBmodel


t_user = test_credentials.Test_User()


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': f'sqlite://'})

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            user = DBmodel.User(email=t_user.username, first_name=t_user.name, password=generate_password_hash(
               t_user.password, method='sha256'))
            db.session.add(user)
            db.session.commit()
            
            

        yield client

    os.close(db_fd)
    os.unlink(db_path)
