from flask_restful import Resource, request, reqparse
from flask_jwt import jwt_required
import sqlite3

from models.game import GameModel


class Game(Resource):

    def get(self, name):
        game = GameModel.check_by_name(name)
        if game:
            return game.get_json(), 200
        return {"message" : "Game %s not found" % (name)}

    @jwt_required()
    def post(self, name):

        if GameModel.check_by_name(name):
            return {"message" : "Game {} already exists" . format(name)}, 400

        # Parsing the inputs
        parser = reqparse.RequestParser()
        parser.add_argument('schedule', type=str)
        parser.add_argument('sport_name', type=str, required=True,
                            help='Sport is required')

        data = parser.parse_args()

        game = GameModel(name, **data)
        game.add_to_db()

        return game.get_json(), 201

    @jwt_required()
    def delete(self, name):
        game = GameModel.check_by_name(name)
        if game:
            game.remove_from_db()
            return {"message" : "game removed"}, 200
        return {"message" : "game not found"}, 404

    @jwt_required()
    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('schedule', type=str)
        parser.add_argument('sport_name', type=str, required=True)
        data = parser.parse_args()
        game = GameModel(name, **data)

        game.add_to_db()

        return game.get_json(), 201


class Games(Resource):
    @jwt_required()
    def get(self):
        games = [game.get_json() for game in GameModel.query.all()]
        return {'games' : games}, 200
