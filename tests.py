#!/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import Employee, Company, Record
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class BaseModelCase(unittest.TestCase):
    # set up database
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    # destroy database
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class EmployeeModelCase(BaseModelCase):
    
    # password hashing
    def test_password_hash(self):
        # create employee
        e = Employee(email='thomas@example.com', first_name='thomas',
                     last_name='mcdonnell')
        # set password
        e.set_password('test')

        # check password hashing
        self.assertTrue(e.check_password('test'))
        self.assertFalse(e.check_password('fest'))

    # Check Employee Memberships
    def test_company_membership(self):
        # create companies
        c1 = Company(company_name='test', email='test@example.com')
        c2 = Company(company_name='test2', email='test2@example.com')

        # create employees with memberships
        e1 = Employee(email='thomas@example.com', first_name='thomas',
                     last_name='mcdonnell', is_admin=True, member_of=c1)
        e2 = Employee(email='tom@example.com', first_name='tom',
                     last_name='jones', member_of=c2)

        # commit to database 
        db.session.add(c1)
        db.session.add(c2)
        db.session.add(e1)
        db.session.add(e2)
        db.session.commit()


        # test memberships
        self.assertEqual(c1.employees.count(), 1)
        self.assertEqual(c2.employees.count(), 1)

        # test memberships
        self.assertEqual(c1.employees.all(), [e1])
        self.assertNotEqual(c1.employees.all(), [e2])
        self.assertEqual(c2.employees.all(), [e2])
        self.assertNotEqual(c2.employees.all(), [e1])


if __name__ == '__main__':
    unittest.main(verbosity=2)
