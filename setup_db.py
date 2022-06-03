from decimal import Decimal

from app import create_app, db
from app.models import Person, MoneyMovement, User

app = create_app()
app_context = app.app_context()
app_context.push()

app.logger.info("Creating Tables Within Database")
db.drop_all()
db.create_all()

app.logger.info("Creating Mock MoneyMovement Objects")
person_1 = Person(first_name="Clément", last_name="Pergaud")
person_2 = Person(first_name="Jeffery", last_name="Bezos")
person_3 = Person(first_name="X Æ A-12", last_name="Musk")
person_4 = Person(first_name="Emma", last_name="Smith")

money_movement_1 = MoneyMovement.create(sender=person_2, receiver=person_3, money_amount=Decimal(0.0010),
                                        currency_code="GBP")
money_movement_2 = MoneyMovement.create(sender=person_2, receiver=person_1, money_amount=1000.15, currency_code="GBP")

money_movement_3 = MoneyMovement.create(sender=person_1, receiver=person_4, money_amount=1000, currency_code="GBP")

money_movement_4 = MoneyMovement.create(sender=person_4, receiver=person_1, money_amount=1000, currency_code="EUR")

db.session.add_all([money_movement_1, money_movement_2, money_movement_3, money_movement_4])
db.session.commit()

app.logger.info(f"MoneyMovement Objects Have Been Inserted Into Database At {app.config['SQLALCHEMY_DATABASE_URI']}")

app.logger.info("Creating User Account")

new_user = User.create(email="joshuahatfield.jh@gmail.com",name="Josh",password="password")


db.session.add(new_user)
db.session.commit()

app.logger.info(f"User Object Has Been Inserted Into Database At {app.config['SQLALCHEMY_DATABASE_URI']}")

exit()
