import unittest
import urllib
from flask import url_for
from flask_login import current_user
from flask import request
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


class ViewTestCase(BaseTestCase):
    def test_login_page_loads(self):
        with self.client:
            response = self.client.get('/auth/login')
            self.assertIn(b'Remember Me', response.data)

    def test_correct_view_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Personal Portfolio Nazar', response.data)

    def test_real_server_is_up_and_running(self):
        response = urllib.request.urlopen(self.baseURL)
        self.assertEqual(response.code, 200)


if __name__ == '__main__':
    unittest.main()
