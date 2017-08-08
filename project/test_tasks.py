# test_tasks.py
import os
import unittest

from views import app, db
from models import User
from _config import basedir

TEST_DB = 'test.db'


class TasksTests(unittest.TestCase):
    # ##########################
    # Setup and Teardown Methods
    # ##########################
    def setUp(self):
        # Set configuation for test case
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        # Have an app client for test cases
        self.app = app.test_client()
        # Create db schemea
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # ##############
    # Helper Methods
    # ##############
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

    def create_user(self, name, email, password):
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
    
    def create_admin_user(self):
        admin_user = User(name='superman', email='superman@gmail.com', password="lahore", role='admin')
        db.session.add(admin_user)
        db.session.commit()

    def create_task(self):
        return self.app.post(
                    'add/',
                    data=dict(
                        name='Go to the bank',
                        due_date='10/08/2017',
                        priority=10,
                        posted_date='08/08/2017',
                        status=1),
                    follow_redirects=True)

    # ########################
    # Tasks Related Test Cases
    # ########################
    def test_logged_in_users_can_access_tasks_page(self):
        self.register('abuzar', 'abuzar@gmail.com', 'lahore', 'lahore')
        self.login('abuzar', 'lahore')
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertIn(b'Add a new task:', response.data)

    def test_not_logged_in_users_cannot_access_tasks_page(self):
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_users_can_add_tasks(self):
        self.create_user('abuzar', 'abuzar@gmail.com', 'lahore')
        self.login('abuzar', 'lahore')
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.assertIn(b'New entry was successfully posted. Thanks.', response.data)

    def test_users_cannot_add_tasks_when_error(self):
        self.create_user('abuzar', 'abuzar@gmail.com', 'lahore')
        self.login('abuzar', 'lahore')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.post('add/',
                            data=dict(
                                name='Go to the bank',
                                due_date='',
                                priority=10,
                                posted_date='08/08/2017',
                                status=1),
                            follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)

    def test_users_can_complete_tasks(self):
        self.create_user('abuzar', 'abuzar@gmail.com', 'lahore')
        self.login('abuzar', 'lahore')
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        print(response)
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertIn(b'The task is complete. Nice.', response.data)

    def test_users_can_delete_tasks(self):
        self.create_user('abuzar', 'abuzar@gmail.com', 'lahore')
        self.login('abuzar', 'lahore')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        response = self.app.get('delete/1/', follow_redirects=True)
        self.assertIn(b'The task was deleted.', response.data)

    def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
        self.create_user('abuzar', 'abuzar@gmail.com', 'lahore')
        self.login('abuzar', 'lahore')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()

        self.create_user('abuzar1', 'abuzar1@gmail.com', 'lahore')
        self.login('abuzar1', 'lahore')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertNotIn(b'The task is complete. Nice.', response.data)
        self.assertIn(b'You can only update tasks that belong to you.', response.data)

    def test_users_cannot_delete_tasks_that_are_not_created_by_them(self):
        self.create_user('abuzar', 'abuzar@gmail.com', 'lahore')
        self.login('abuzar', 'lahore')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()

        self.create_user('abuzar1', 'abuzar1@gmail.com', 'lahore')
        self.login('abuzar1', 'lahore')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('delete/1/', follow_redirects=True)
        self.assertNotIn(b'The task was deleted. Why not add a new one?', response.data)
        self.assertIn(b'You can only delete tasks that belong to you.', response.data)

    def test_admin_users_can_complete_tasks_not_created_by_them(self):
        self.create_user('abuzar', 'abuzar@gmail.com', 'lahore')
        self.login('abuzar', 'lahore')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()

        self.create_admin_user()
        self.login('superman', 'lahore')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertIn(b'The task is complete. Nice.', response.data)
        self.assertNotIn(b'You can only update tasks that belong to you.', response.data)

    def test_admin_users_can_delete_tasks_that_are_not_created_by_them(self):
        self.create_user('abuzar', 'abuzar@gmail.com', 'lahore')
        self.login('abuzar', 'lahore')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()

        self.create_admin_user()
        self.login('superman', 'lahore')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('delete/1/', follow_redirects=True)
        self.assertIn(b'The task was deleted. Why not add a new one?', response.data)
        self.assertNotIn(b'You can only delete tasks that belong to you.', response.data)


if __name__ == '__main__':
    unittest.main()