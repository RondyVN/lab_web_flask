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


class FlaskTestCase(BaseTestCase):
    # Ensure that Flask was set up correctly
    def test_index(self):
        response = self.client.get('/auth/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that main page requires user login
    def test_main_route_requires_login(self):
        response = self.client.get('/auth/account', follow_redirects=True)
        self.assertIn(b'Remember Me', response.data)


class UserViewsTests(BaseTestCase):

    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        response = self.client.get('/auth/login')
        self.assertIn(b'Remember Me', response.data)

    # Ensure login behaves correctly with correct credentials
    def test_correct_register_and_login(self):
        with self.client:
            response = self.client.post(url_for('auth.signup'),
                data=dict(email="sdaawdgg@gmail.com",
                          username="testhuan",
                          password1="Password",
                          password2="Password"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)

            response = self.client.post(
                '/auth/login',
                data=dict(email="test_lab12@gmail.com", password="Password"),
                follow_redirects=True
            )
            self.assertTrue(current_user.is_active)
            self.assert_200(response)

    def test_incorrect_login(self):
        response = self.client.post(
            '/auth/login',
            data=dict(email="test_lab12@gmail.com", password="Password"),
            follow_redirects=True
        )


if __name__ == '__main__':
    unittest.main()