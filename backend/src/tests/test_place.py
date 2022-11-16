import os
import unittest
from unittest import TestCase
import json
from flask_sqlalchemy import SQLAlchemy
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from models.base import setup_db
from models.place import Place
from api import app

class PlaceTestCase(TestCase):
    
    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.database_name = "rentersReview_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass
    
    def test_get_post(self):
        res = self.client().get('/places')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

if __name__ == "__main__":
    unittest.main()


