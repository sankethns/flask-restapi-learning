from db import db

class SportModel(db.Model):

    __tablename__ = 'sports'
    __bind_key__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    games = db.relationship('GameModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def get_json(self):
        return {'name': self.name,
                'id': self.id,
                'games': [game.get_json() for game in self.games.all()]}

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def check_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def check_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()
