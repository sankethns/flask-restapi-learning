'''
Starts the REST API Server.
Create an Olympic database
Hosted on DigitalOcean
'''

import os
from flask import Flask
from flask_restful import Api
from security import authenticate, identity
from flask_jwt import JWT
from resources.user import UserRegister
from resources.game import Game, Games
from resources.sport import Sport, Sports

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'qwer1234!@#$'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {
    'data' : os.environ.get('DATABASE_URL', 'sqlite3:///data.db'),
}
jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(UserRegister, '/register')
api.add_resource(Game, '/game/<string:name>')
api.add_resource(Games, '/games')
api.add_resource(Sport, '/sport/<string:name>')
api.add_resource(Sports, '/sports')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
