from .base import db
from flask import jsonify
from config import get_config
import requests


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String)
    name = db.Column(db.String)
    nickname = db.Column(db.String)
    picture = db.Column(db.String)
    updated_at = db.Column(db.String)
    
    def get_all():
        return User.query.all()

    def get_all_formatted():
        return [ u.format() for u in User.query.all()]
    
    def get_all_from_auth0():

        url = "https://dev-6gnrncvpus8amyed.us.auth0.com/api/v2/users"
        headers = {
        'Authorization': get_config('auth0_token')
        }

        response = requests.request("GET", url, headers=headers)

        print(response.text)
        
        return response.json()
        
    def format(self):
        return jsonify({
            'id': self.id,
            'email': self.email
        })