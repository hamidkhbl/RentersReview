from .base import db 
from flask import jsonify

class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    description = db.Column(db.String)
    latitude = db.Column(db.String)
    longitude = db.Column(db.String)
    
    def get_all():
        return Place.query.all()
    
    def get_all_formatted():
        return [p.format() for p in Place.get_all()]
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def get_by_id(place_id):
        return Place.query.filter_by(id=place_id).one_or_none()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def delete_bulk(ids):
        deleted = []
        not_deleted = []
        for id in ids:
            try:
                place = Place.get_by_id(id)
                db.session.delete(place)
                db.session.commit()
                deleted.append(id)
            except Exception as e:
                not_deleted.append(id)
                print(e)
        return [deleted, not_deleted]
    
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'description': self.description,
            'latitude': self.latitude,
            'longtude': self.longitude
        }