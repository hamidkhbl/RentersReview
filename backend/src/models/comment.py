from .base import db
from flask import jsonify
from .like import Like


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    creation_date = db.Column(db.String)
    user_id = db.Column(db.String)
    place_id = db.Column(db.Integer, db.ForeignKey("places.id"))
    likes = db.relationship("Like", backref="comment")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def get_all():
        return Comment.query.all()
    
    def get_place_comments(place_id):
        return Comment.query.filter_by(place_id=place_id).all()
    
    def get_all_formatted():
        return [c.format() for c in Comment.get_all()]
    
    def get_place_comments_formatted(place_id):
        return [c.format() for c in Comment.get_place_comments(place_id)]

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'creation_date': self.creation_date,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'likes_count': len(self.likes),
        }

    def format_with_likes(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'creation_date': self.creation_date,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'likes_count': len(self.likes),
            'likes': [l.format() for l in self.likes]
        }
