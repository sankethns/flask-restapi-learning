from flask_restful import Resource, request, reqparse
from flask_jwt import jwt_required
import sqlite3

from models.sport import SportModel


class Sport(Resource):

    def get(self, name):
        sport = SportModel.check_by_name(name)
        if sport:
            return sport.get_json(), 200
        return {"message" : "Game %s not found" % (name)}

    @jwt_required()
    def post(self, name):

        if SportModel.check_by_name(name):
            return {"message" : "Sport {} already exists" . format(name)}, 400

        sport = SportModel(name)
        sport.add_to_db()

        return sport.get_json(), 201

    @jwt_required()
    def delete(self, name):
        sport = SportModel.check_by_name(name)
        if sport:
            sport.delete_from_db()
            return {"message" : "sport removed"}, 200
        return {"message" : "sport not found"}, 404


class Sports(Resource):
    def get(self):
        sports = [sport.get_json() for sport in SportModel.query.all()]
        return {'sports' : sports}, 200
