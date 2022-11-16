import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from api import app
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
    def test_get_places(self):
        res = self.client().get('/places')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test post a place without authorization
    def test_post_places_no_auth(self):
        headers = {}
        place = Place(title="Test")
        res = self.client().post('/places', json=place.format(), headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Test post a place without permit
    def test_post_places_no_permit(self):
        token = get_user_token('non-member')
        headers = {
            'Authorization': 'Bearer '+token
        }
        
        place = Place(title="Test")
        res = self.client().post('/places', json=place.format(), headers=headers)
        data = json.loads(res.text)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # Test post a place
    def test_post_places_success(self):
        token = get_user_token('member')
        headers = {
            'Authorization': 'Bearer '+token
        }
        place = Place(title="Test")
        res = self.client().post('/places', json=place.format(), headers=headers)
        data = json.loads(res.text)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    # Test delete a place with member user
    def test_delete_places_no_permit(self):
        old_place = Place.query.first()
        token = get_user_token('member')
        headers = {
            'Authorization': 'Bearer '+token
        }
        place = Place(title="Test")
        res = self.client().delete('/places/'+str(old_place.id), headers=headers)
        data = json.loads(res.text)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        
    # Test delete a place with admin user
    def test_delete_places(self): 
        old_place = Place.query.first()
        old_place_id = str(old_place.id)
        token = get_user_token('admin')
        headers = {
            'Authorization': 'Bearer '+token
        }
        place = Place(title="Test")
        res = self.client().delete('/places/'+ old_place_id, headers=headers)
        data = json.loads(res.text)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test patch a place with member user
    def test_patch_places_no_permit(self):
        old_place = Place.query.first()
        old_place.address = "Patched"
        token = get_user_token('member')
        headers = {
            'Authorization': 'Bearer '+token
        }
        place = Place(title="Test")
        res = self.client().patch('/places/'+str(old_place.id), json=old_place.format(), headers=headers)
        data = json.loads(res.text)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # Test patch a place with admin user
    def test_patch_places(self):
        old_place = Place.query.first()
        old_place.address = "Patched"
        token = get_user_token('admin')
        headers = {
            'Authorization': 'Bearer '+token
        }
        place = Place(title="Test")
        res = self.client().patch('/places/'+str(old_place.id), json=old_place.format(), headers=headers)
        data = json.loads(res.text)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


if __name__ == "__main__":
    unittest.main()
