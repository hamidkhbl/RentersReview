from .base import db
from flask import jsonify
from .user import User


class Like(db.Model):
    __tablename__ = 'likes'
    user_id = db.Column(db.String)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"), primary_key=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def like(self):
        is_liked=Like.query.filter_by(comment_id=self.comment_id).filter_by(user_id=self.user_id).one_or_none()
        if is_liked is None:
            self.insert()
            return "added"
        else:
            is_liked.delete()
            return "removed"
    
    def get_user(self):
        return User.query.filter_by(id=self.user_id).one().format()

    def format(self):
        return {
            'user': self.get_user()
        }