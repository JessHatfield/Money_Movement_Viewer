import datetime
import os
import unittest
from decimal import Decimal

from flask_login import FlaskLoginClient

from app import create_app, db
from app.models import User, Person, MoneyMovement


def generate_dummy_data():
    person_1 = Person(first_name="Clément", last_name="Pergaud")
    person_2 = Person(first_name="Jeffery", last_name="Bezos")
    person_3 = Person(first_name="X Æ A-12", last_name="Musk")
    person_4 = Person(first_name="Emma", last_name="Smith")

    money_movement_1 = MoneyMovement.create(sender=person_2, receiver=person_3, money_amount=Decimal(0.0010),
                                            currency_code="GBP")

    money_movement_2 = MoneyMovement.create(sender=person_2, receiver=person_1, money_amount=1000.15,
                                            currency_code="GBP")

    money_movement_3 = MoneyMovement.create(sender=person_1, receiver=person_4, money_amount=1000, currency_code="GBP")

    money_movement_4 = MoneyMovement.create(sender=person_4, receiver=person_1, money_amount=1000, currency_code="EUR")

    # harcode money movements to allow integration tests to repeat!

    money_movement_1.modified_at_datetime_utc = datetime.datetime.strptime("2022-06-03 17:17:05", "%Y-%m-%d %H:%M:%S")
    money_movement_2.modified_at_datetime_utc = datetime.datetime.strptime("2022-06-03 17:17:05", "%Y-%m-%d %H:%M:%S")
    money_movement_3.modified_at_datetime_utc = datetime.datetime.strptime("2022-06-03 17:17:05", "%Y-%m-%d %H:%M:%S")
    money_movement_4.modified_at_datetime_utc = datetime.datetime.strptime("2022-06-03 17:17:05", "%Y-%m-%d %H:%M:%S")

    db.session.add_all([money_movement_1, money_movement_2, money_movement_3, money_movement_4])
    db.session.commit()


class TestConfig():
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://money_movement_viewer_admin:password@localhost:3306/money_movement_viewer_test?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_DOMAIN = "http://127.0.0.1:5000"
    SECRET_KEY = "You-Will-Never-Guess-This"
    WTF_CSRF_ENABLED = False


class TestAuthentication(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.app = self.app.test_client()

        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_user_can_login_and_access_protected_route(self):
        new_user = User.create(email="joshuahatfield.jh@gmail.com", name="Josh", password="password")

        db.session.add(new_user)
        db.session.commit()
        generate_dummy_data()

        money_movements_table_page = self.app.post('/login?next=%2F',
                                                   data={"username": "joshuahatfield.jh@gmail.com",
                                                         "password": "password",
                                                         },
                                                   follow_redirects=True)

        self.assertEqual(money_movements_table_page.status_code, 200)
        self.assertIn("Welcome Josh", money_movements_table_page.text)
        self.assertIn("Logout", money_movements_table_page.text)

    def test_user_can_logout(self):
        new_user = User.create(email="joshuahatfield.jh@gmail.com", name="Josh", password="password")

        db.session.add(new_user)
        db.session.commit()
        generate_dummy_data()

        money_movements_table_page = self.app.post('/login?next=%2F',
                                                   data={"username": "joshuahatfield.jh@gmail.com",
                                                         "password": "password",
                                                         },
                                                   follow_redirects=True)

        self.assertEqual(money_movements_table_page.status_code, 200)

        # logout and then try accessing a protected page
        self.app.get('/logout')

        view_after_logging_out = self.app.get('/')

        self.assertNotIn(view_after_logging_out.text, 'Welcome Josh')
        self.assertNotIn(view_after_logging_out.text, 'Logout')
        self.assertEqual(view_after_logging_out.status_code, 302)

    def test_unauthenticated_requests_are_redirected(self):
        new_user = User.create(email="joshuahatfield.jh@gmail.com", name="Josh", password="password")

        db.session.add(new_user)
        db.session.commit()
        generate_dummy_data()

        response = self.app.get('/')
        self.assertIn('You should be redirected automatically to the target URL: <a href="/login?next=%2F">',
                      response.text)

        # View single money movement page
        response = self.app.get('/view_money_movement/1')
        self.assertIn(
            'You should be redirected automatically to the target URL: <a href="/login?next=%2Fview_money_movement%2F1">/login?next=%2Fview_money_movement%2F1</a>',
            response.text)

        # Edit user note on single money movement page
        response = self.app.post('/view_money_movement/1', data={"user_note": ""})
        self.assertIn(
            '<p>You should be redirected automatically to the target URL: <a href="/login?next=%2Fview_money_movement%2F1">/login?next=%2Fview_money_movement%2F1</a>.',
            response.text)


class TestViewAllMoneyMovements(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.app = self.app.test_client()

        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_money_movements_viewable_when_logged_in(self):
        new_user = User.create(email="joshuahatfield.jh@gmail.com", name="Josh", password="password")

        db.session.add(new_user)
        db.session.commit()

        generate_dummy_data()

        money_movements_table_page = self.app.post('/login?next=%2F',
                                                   data={"username": "joshuahatfield.jh@gmail.com",
                                                         "password": "password",
                                                         },
                                                   follow_redirects=True)

        self.assertEqual(money_movements_table_page.status_code, 200)
        # I'm not a fan of testing against exact HTML code in an integration test. We are testing implementation, but really we just want to test behaviours
        # In these tests we only really care that a row exists containing the movement data. We don't care about css/exact html tags used
        # Testing against implementation details can make tests more brittle, easier to break and reduce the ease at which changes can be made
        # Given more time BS4 or selenium could prehaps be used here and we could search by Roles or classes (like forms/buttons or table_rows). Similar to the React Testing Library
        # The assertions below are hard to read and a little brittle but still serve their purpose of confirming outputs meet expectations.

        # Check each of the table rows contains expected money movement data
        self.assertIn(
            """<tr id=2>\n                <td>2022-06-03 17:17:05</td>\n                <td>1000.1500 GBP</td>\n                <td>Jeffery Bezos</td>\n                <td><a href="/view_money_movement/2">Details</a></td>\n            </tr>\n""",
            money_movements_table_page.text)
        self.assertIn(
            """<tr id=1>\n                <td>2022-06-03 17:17:05</td>\n                <td>0.0010 GBP</td>\n                <td>Jeffery Bezos</td>\n                <td><a href="/view_money_movement/1">Details</a></td>\n            </tr>\n""",
            money_movements_table_page.text)
        self.assertIn(
            """<tr id=3>\n                <td>2022-06-03 17:17:05</td>\n                <td>1000.0000 GBP</td>\n                <td>Clément Pergaud</td>\n                <td><a href="/view_money_movement/3">Details</a></td>\n            </tr>\n""",
            money_movements_table_page.text)
        self.assertIn(
            """<tr id=4>\n                <td>2022-06-03 17:17:05</td>\n                <td>1000.0000 EUR</td>\n                <td>Emma Smith</td>\n                <td><a href="/view_money_movement/4">Details</a></td>\n            </tr>\n""",
            money_movements_table_page.text)


if __name__ == '__main__':
    unittest.main()
