from .base import db
from flask import jsonify
from .user import User


class Like(db.Model):
    __tablename__ = 'likes'
    user_id = db.Column(db.String, db.ForeignKey("users.id"), primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"), primary_key=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def is_like(user_id, comment_id):
        is_liked=Like.query.filter_by(comment_id=comment_id).filter_by(user_id=user_id).one_or_none()
        if is_liked is None:
            return False
        else:
            return True
    
    def get_user(self):
        return User.query.filter_by(id=self.user_id).one().format()

    def format(self):
        return {
            'user': self.get_user()
        }