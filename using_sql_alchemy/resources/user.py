import sqlite3
from flask_restful import Resource, reqparse
from using_sql_alchemy.models.user import UserModel

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
        if UserModel.get_user_by_name(data['username']):
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
    print(UserModel.get_user_by_id(1))