import unittest
from decimal import Decimal

from app import create_app, db
from app.models import Person, MoneyMovement


class TestConfig():
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://money_movement_viewer_admin:password@localhost:3306/money_movement_viewer_test?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_DOMAIN = "http://127.0.0.1:5000"


class MoneyMovementTests(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app = self.app.test_client()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_money_movement_via_create_method(self):
        sender = Person(first_name="jeff", last_name="bezo")
        receiver = Person(first_name="Clément", last_name="Pergaud")

        new_movement = MoneyMovement.create(sender=sender, receiver=receiver, currency_code="GBP", money_amount=10)

        db.session.add(new_movement)
        db.session.commit()

        # check movement exists in DB + Has Correct Values Stored
        movement_in_db = MoneyMovement.query.first()

        self.assertEqual(movement_in_db.id, 1)
        self.assertEqual(movement_in_db.iso_4217_currency_code, 'GBP')
        self.assertEqual(movement_in_db.money_amount, 10.000)
        self.assertEqual(movement_in_db.origin_id, 1)
        self.assertEqual(movement_in_db.receiver_id, 2)
        self.assertEqual(movement_in_db.sender.first_name, "jeff")
        self.assertEqual(movement_in_db.receiver.first_name, "Clément")

    def test_fractional_money_amounts_preserved(self):
        # Making some assumptions about number of decimal places required?
        # Visa card fee is 0.2% of a value
        # The Smallest transaction a user would be likely to make in the UK is 1 pence
        # 0.2% of 1 pence is 0.002 pounds

        sender = Person(first_name="jeff", last_name="bezo")
        receiver = Person(first_name="Clément", last_name="Pergaud")

        # can we store and then retrieve this fractional value
        new_movement = MoneyMovement.create(sender=sender, receiver=receiver, currency_code="GBP", money_amount=0.002)

        db.session.add(new_movement)
        db.session.commit()

        movement_in_db = MoneyMovement.query.first()
        self.assertEqual(movement_in_db.money_amount, Decimal("0.002"))
        self.assertEqual(movement_in_db.iso_4217_currency_code, "GBP")




if __name__ == '__main__':
    unittest.main()
