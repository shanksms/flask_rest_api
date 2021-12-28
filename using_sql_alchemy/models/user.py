import sqlite3
from using_sql_alchemy.db import db


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))


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
