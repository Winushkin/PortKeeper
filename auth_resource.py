from flask import jsonify
from flask_restful import Resource, reqparse
from database import DataBase


class AuthResource(Resource):
    def __init__(self):
        self.db = DataBase('database/base.sqlite3')


    def check_student_auth(self):
        args = parser.parse_args()
        login = args['login']
        password = args['password']
        user = self.db.get_student(login, password)
        if user:
            return jsonify({"user": user})
        else:
            return jsonify({"error": "Invalid credentials"})

    def check_teachers_auth(self):
        args = parser.parse_args()
        login = args['login']
        password = args['password']
        user = self.db.get_student(login, password)
        if user:
            return jsonify({"user": user})
        else:
            return jsonify({"error": "Invalid credentials"})



    def get(self):
        args = parser.parse_args()
        login = args['login']
        password = args['password']
        user = self.db.get_student(login, password)
        if user:
            return jsonify({"user": user})
        else:
            return jsonify({"error": "Invalid credentials"})

parser = reqparse.RequestParser()
parser.add_argument('login', type=str, required=True)
parser.add_argument('password', type=str, required=True)


