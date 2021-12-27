import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def get_user_by_name(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = '''
        select * from user where username=?
        '''
        result = cursor.execute(query, (username, ))
        row = result.fetchone()
        return cls(*row) if row else None


    @classmethod
    def get_user_by_id(cls, id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = '''
               select * from user where id=?
               '''
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        return cls(*row)


    def __str__(self):
        return f'username: {self.username}'


class UserRegister(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument(
        'username',
        type=str,
        required=True,
        help='This field can not be left blank'
    )
    request_parser.add_argument(
        'password',
        type=str,
        required=True,
        help='This field can not be left blank'
    )

    def post(self):
        data = UserRegister.request_parser.parse_args()
        if User.get_user_by_name(data['username']):
            return {'message': 'user already exists'}, 400
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            insert_query = '''
                   insert into user
                   (username, password)
                   values
                   (?, ?)
                   '''
            cursor.execute(insert_query, (data['username'], data['password']))
            connection.commit()
        finally:
            connection.close()
        return {'message': 'successfully created the user'}


if __name__ == '__main__':
    print(User.get_user_by_id(1))