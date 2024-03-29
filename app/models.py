from __future__ import annotations

import datetime

from decimal import Decimal

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, login


class MoneyMovement(db.Model):
    """
    A MoneyMovement represents a movement of a money amount between two persons
    """

    id = db.Column('id', db.Integer(), primary_key=True)
    modified_at_datetime_utc = db.Column(db.DateTime, nullable=False)
    iso_4217_currency_code = db.Column(db.String(3))  # currency codes are 3 bytes long https://www.xe.com/iso4217.php

    # money amount should be in the denomination specified in iso_4217_currency_code. E.g. The money amount for GBP would be Pounds. The money amount for EUR would be Euros.
    # This seems to be convention used in money transfer?
    money_amount = db.Column(
        db.DECIMAL(10,
                   4))  # Decimal stores exact numeric value as opposed to float which just approximates. 4 decimal points required to preserve fractional values on transactions like card fees

    origin_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    user_note = db.Column(db.Text, nullable=True)

    @classmethod
    def create(cls, currency_code: str, money_amount: Decimal, sender: Person, receiver: Person,
               user_note: str = "") -> MoneyMovement:
        """


        :param currency_code: An iso_4127 currency code - https://www.xe.com/iso4217.php
        :param money_amount: A decimal amount of a currency. Currency denomination specified by currency_code
        :param sender: An instance of the Person class "sending" the money amount
        :param receiver: An instance of the Person call "receiving" the money amount
        :param user_note: A user_note with no fixed length containing agent notes on the money movement
        :return: An instance of the MoneyMovement Class representing the money movement between two persons
        """

        money_movement = MoneyMovement(iso_4217_currency_code=currency_code, money_amount=money_amount,
                                       modified_at_datetime_utc=datetime.datetime.utcnow(),
                                       user_note=user_note)  # Store as UTC to allow for conversion to multiple timezones within view

        sender.money_movements_sent.append(money_movement)
        receiver.money_movements_received.append(money_movement)

        return money_movement


class Person(db.Model):
    """
    A person represents a single unique human being
    """

    # For simplicity’s sake we will assume a person = a single human being
    # In a production app a person might also be a group of humans (a bank/company/charity?) or a bank account?
    # We could have just used string fields within the Money Movement class to store person.
    # A person seemed to be a separate entity within the domain. Seems neater to give its own class as a result
    # If we end up wanting to trace movements across more than two people perhaps a graphDB might be useful?
    id = db.Column('id', db.Integer(), primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)

    money_movements_sent = db.relationship('MoneyMovement', foreign_keys='MoneyMovement.origin_id',
                                           backref='sender', lazy='dynamic')
    money_movements_received = db.relationship('MoneyMovement', foreign_keys='MoneyMovement.receiver_id',
                                               backref='receiver', lazy='dynamic')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.Text, nullable=False)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        valid = check_password_hash(self.password_hash, password)

        if not valid:
            current_app.logger.info(f"Password For {self} Does Not Match Stored Hash")
            current_app.logger.debug({"message": f"Password Does Not Match Stored Hash", "user": f"{self}"})

        return valid

    @classmethod
    def create(cls, email: str, name: str, password: str) -> User:
        user = User(email=email, name=name)
        user.set_password(password)
        return user


@login.user_loader
def load_user(id):
    user = User.query.get(int(id))
    current_app.logger.info(f"{user} Retrieved By Flask_Login User Loader")
    current_app.logger.debug(
        {"message": f"User Retrieved By Flask_Login User Loader", "id_given": id, "user": f"{user}"})
    return user
