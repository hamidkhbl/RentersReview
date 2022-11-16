import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from api import app
from models.comment import Comment
from models.place import Place
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

    # Test get places
    def test_get_place_comments(self):
        place_id = str(Place.query.first().id)
        res = self.client().get('/places/'+place_id+'/comments')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test post a comment without authorization
    def test_post_places_no_auth(self):
        headers = {}
        place_id = Place.query.first().id
        comment = Comment(title="Test", place_id=place_id)
        res = self.client().post('/comments', json=comment.format(), headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_post_comment_no_permit(self):
        token = get_user_token('non-member')
        headers = {
            'Authorization': 'Bearer '+token
        }
        place_id = Place.query.first().id
        comment = Comment(title="Test", place_id=place_id)
        res = self.client().post('/comments', json=comment.format(), headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        
    def test_post_comment(self):
        token = get_user_token('member')
        headers = {
            'Authorization': 'Bearer '+token
        }
        place_id = Place.query.first().id
        comment = Comment(title="Test", place_id=place_id)
        res = self.client().post('/comments', json=comment.format(), headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        






    # Test post a comment without authorization
    def test_delete_places_no_auth(self):
        headers = {}
        comment_id = str(Comment.query.first().id)
        res = self.client().delete('/comment/'+comment_id, headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_comment_no_permit(self):
        token = get_user_token('member')
        headers = {
            'Authorization': 'Bearer '+token
        }
        comment_id = str(Comment.query.first().id)
        res = self.client().delete('/comment/'+comment_id, headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        
    def test_delete_comment(self):
        token = get_user_token('admin')
        headers = {
            'Authorization': 'Bearer '+token
        }
        comment_id = str(Comment.query.first().id)
        res = self.client().delete('/comment/'+comment_id, headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


if __name__ == "__main__":
    unittest.main()
