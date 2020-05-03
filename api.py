# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import reqparse, Resource, Api
from service import loginGithub


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()


class RecentActivity(Resource):
    def get(self):
        return {
            'help': 'send email, password and 2fa_token with the post method.'
        }

    def post(self):
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('2fa_token', type=str)
        args = parser.parse_args()
        return loginGithub(args['email'], args['password'], args['2fa_token'])


api.add_resource(RecentActivity, '/recent_activity')

if __name__ == '__main__':
    app.run(debug=True, port=4000)
