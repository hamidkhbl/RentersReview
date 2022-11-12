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
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
        
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
        return response.json()
    
    def import_users():
        users = User.get_all_from_auth0()
        existing_user = User.get_all()
        existing_ids = []
        added = []
        not_added = []
        for u in existing_user:
            existing_ids.append(u.id)
            
        for u in users:
            user = User(
                id = u.get('user_id').split('|')[1],
                email = u.get('email'),
                name = u.get('name'),
                nickname = u.get('nickname'),
                picture = u.get('picture'),
                updated_at = u.get('updated_at'),
            )
            if user.id not in existing_ids:
                user.insert()
                added.append(user)
            else:
                not_added.append(user)
        return [added, not_added]
                
    def format(self):
        return {
            'id': self.id,
            'email': self.email
        }