import sqlite3
from db import db
from models.sport import SportModel

class GameModel(db.Model):

    __tablename__ = 'games'
    __bind_key__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    schedule = db.Column(db.String)
    sport_id = db.Column(db.Integer, db.ForeignKey('sports.id'))
    sport_name = db.Column(db.String)
    sport = db.relationship('SportModel')

    def __init__(self, name, sport_name, schedule=None):
        self.name = name
        self.schedule = schedule
        self.sport_id = SportModel.check_by_name(sport_name).id
        self.sport_name = sport_name

    def get_json(self):
        return {'name': self.name, 'schedule': self.schedule,
                'sport': self.sport_name}

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def check_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
