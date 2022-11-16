import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from api import app
from models.comment import Comment
from models.place import Place
from models.like import Like
from models.base import setup_db
import unittest
from unittest import TestCase
import json
from flask_sqlalchemy import SQLAlchemy
import requests
from test_data import get_user_token



class PlaceTestCase(TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        try:
            self.database_name = "rentersReview_test"
            self.database_path = "postgresql://{}/{}".format(
                'localhost:5432', self.database_name)
            setup_db(self.app, self.database_path)

            with self.app.app_context():
                self.db = SQLAlchemy()
                self.db.init_app(self.app)
                # create all tables
                self.db.create_all()
        except:
            print("Database already exists.")

    def tearDown(self):
        """Executed after reach test"""
        pass


    # Test like authorization
    def test_like_no_auth(self):
        headers = {}
        comment_id = str(Comment.query.first().id)
        pyload = {
            'comment_id': comment_id
        }
        res = self.client().post('/like', json=pyload, headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Test like no permit
    def test_like_no_permit(self):
        token = get_user_token('non-member')
        headers = {
            'Authorization': 'Bearer '+token
        }
        comment_id = str(Comment.query.first().id)
        pyload = {
            'comment_id': comment_id
        }
        res = self.client().post('/like', json=pyload, headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
    
    # test like
    def test_like(self):
        token = get_user_token('member')
        headers = {
            'Authorization': 'Bearer '+token
        }
        comment_id = str(Comment.query.first().id)
        pyload = {
            'comment_id': comment_id
        }
        res = self.client().post('/like', json=pyload, headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_unlike(self):
        token = get_user_token('member')
        headers = {
            'Authorization': 'Bearer '+token
        }
        comment_id = str(Like.query.first().comment_id)
        pyload = {
            'comment_id': comment_id
        }
        res = self.client().post('/like', json=pyload, headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


if __name__ == "__main__":
    unittest.main()
