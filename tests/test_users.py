# test_users.py

import os
import unittest

from views import app, db
from _config import basedir
from models import User

# Define constants to be used in test cases
TEST_DB = 'test.db'

TEST_USERNAME1 = 'testuser1'
TEST_EMAIL1 = 'testuser1@gmail.com'
TEST_PASSWORD1 = 'testpassword1'

TEST_USERNAME2 = 'testuser2'
TEST_EMAIL2 = 'testuser2@gmail.com'
TEST_PASSWORD1 = 'testpassword2'

# Defin

class UsersTests(unittest.TestCase):
    # ####################
    # Setup and tear down
    # ####################
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client() # local data
        # create DB from scratch
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #################
    # Helper Methods
    #################
    def login(self, name, password):
        return self.app.post('/', 
                      data=dict(name=name, password=password), 
                      follow_redirects=True)
    def register(self, name, email, password, confirm):
        return self.app.post("register/",
                            data=dict(name=name, email=email, password=password, confirm=confirm),
                            follow_redirects=True)
    def logout(self):
        return self.app.get('logout/', follow_redirects=True)

    def register_and_login(self, name, email, password, confirm):
        self.register(name, email, password, confirm)
        return self.login(name, password)

    
    # ##################
    # User's Test Cases
    # ##################
    def test_user_setup(self):
        new_user = User("abuzar", "abuzar@gmail.com", "lahore")
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == 'abuzar'

    def test_login_form_is_present(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please sign in to access your task list', response.data)

    def test_users_can_login(self):
        response = self.register_and_login(TEST_USERNAME1, TEST_EMAIL1, 
                                            TEST_PASSWORD1, TEST_PASSWORD1)
        self.assertIn(b'Welcome', response.data)

    def test_users_cannot_login_unless_registered(self):
        response = self.login(TEST_USERNAME1, TEST_PASSWORD1)
        self.assertIn(b'Invalid username or password', response.data)

    def test_registration_form_is_present(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please register to access the task list', response.data)

    def test_invalid_form_data(self):
        self.register(TEST_USERNAME1, TEST_EMAIL1, TEST_PASSWORD1, TEST_PASSWORD1)
        response = self.login('alert("alert box!")', 'foo')
        self.assertIn(b'Invalid username or password', response.data)

    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please register to access the task list.', response.data)

    def test_user_registration(self):
        #self.app.get('register/', follow_redirects=True)
        response = self.register('abuzar', 'abuzar@gmail.com', 'lahore', 'lahore')
        self.assertIn(b'Thanks for registration. Please login.', response.data)

    def test_user_registration_error(self):
        #self.app.get('register/', follow_redirects=True)
        self.register('abuzar', 'abuzar@gmail.com', 'lahore', 'lahore')
        #self.app.get('register/', follow_redirects=True)
        response = self.register('abuzar', 'abuzar@gmail.com', 'lahore', 'lahore')
        self.assertIn(b'That username and/or email already exist.', response.data)

    def test_logged_in_users_can_logout(self):
        self.register_and_login(TEST_USERNAME1, TEST_EMAIL1, TEST_PASSWORD1, TEST_PASSWORD1)
        response = self.logout()
        self.assertIn(b'Goodbye!', response.data)

    def test_not_logged_in_users_cannot_logout(self):
        response = self.logout()
        self.assertNotIn(b'Goodbye!', response.data)

    def test_default_user_role(self):
        db.session.add(User(TEST_USERNAME1, TEST_EMAIL1, TEST_PASSWORD1))
        db.session.commit()

        users = db.session.query(User).all()
        print(users)
        for user in users:
            self.assertEqual(user.role, 'user')

if __name__ == '__main__':
    unittest.main()
