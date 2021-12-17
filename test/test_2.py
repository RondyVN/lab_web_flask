import unittest
import urllib
from flask import url_for
from flask_login import current_user
from flask import request, current_app
from flask_testing import TestCase

from app import db, create_app
from app.auth.models import User

class BaseTestCase(TestCase):
    def create_app(self):
        self.baseURL = "http://localhost:5000/"
        return create_app('test')

    def setUp(self):
        db.create_all()
        db.session.add(User("test", "test@gmail.com", "password"))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()