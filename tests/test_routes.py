import os
import unittest

from app import create_app, db


class TestConfig():
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://money_movement_viewer_admin:password@localhost:3306/money_movement_viewer_test?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_DOMAIN = "http://127.0.0.1:5000"


class TestRouteRenders(unittest.TestCase):

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


    def test_200_response(self):

        response = self.app.get("/")
        assert b'Hello World!' in response.data


if __name__ == '__main__':
    unittest.main()
