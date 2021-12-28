from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import request
import sqlite3


class Item(Resource):
    @jwt_required()
    def get(self, name):

        item = self.get_item_by_name(name)
        if item == 0:
            return {'message': 'item not found'}, 404
        return item, 200

    def get_item_by_name(self, name):
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            sql = '''
                              select name, price from item where name=?
                       '''
            result = cursor.execute(sql, (name,))
            row = result.fetchone()
        finally:
            connection.close()
        if row:
            return {'name': row[0], 'price': row[1]}
        else:
            return None

    def post(self, name):
        if self.get_item_by_name(name):
            return {'message': f'an item with name {name} already exists'}, 400

        request_data = request.get_json()
        price = float(request_data['price'])
        if self.insert(name, price):
           return {'name': name, 'price': price}, 201
        else:
            return {'message': 'error occurred while creating record'}, 500

    @classmethod
    def insert(cls, name, price):
        status = 1
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            insert_sql = '''
                   insert into item
                   (name, price)
                   values
                   (?, ?)
                   '''
            result = cursor.execute(insert_sql, (name, price))
            print(result)
            connection.commit()
        except Exception as exc:
            print('exception occurred', exc)
            status = 0
        finally:
            connection.close()
        return status

    @classmethod
    def update(cls, name, price):
        status = 1
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            update_sql = 'update item set price=? where name=?'
            result = cursor.execute(update_sql, (price, name))
            connection.commit()
            print(f'{result.rowcount} rows updated')
        except Exception as exc:
            print('exception occurred', exc)
            status = 0
        finally:
            connection.close()
        return status

    def delete(self, name):
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            delete_sql ='delete from item where name=?'
            result = cursor.execute(delete_sql, (name, ))
            print(result)
            connection.commit()
        finally:
            connection.close()

        return {'message': 'item deleted'}

    def put(self, name):
        request_parser = reqparse.RequestParser()
        request_parser.add_argument(
            'price',
            type=float,
            required=True,
            help='This field can not be left blank'
        )
        # data = request.get_json()
        data = request_parser.parse_args()
        item = self.get_item_by_name(name)
        if item:
            self.update(name, data['price'])
        else:
            self.insert(name, data['price'])
        return {'name': name, 'price': data['price']}


class ItemList(Resource):

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        sql = '''
        select name, price from item
        '''
        result = cursor.execute(sql)
        rows = result.fetchall()
        items = []
        for row in rows:
            items.append({'name': row[0], 'price': row[1]})
        connection.commit()
        connection.close()
        return {'items': items}, 200
