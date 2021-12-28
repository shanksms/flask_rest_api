from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import request
import sqlite3
from creating_models_and_resources.models.item import ItemModel


class Item(Resource):
    @jwt_required()
    def get(self, name):

        item = ItemModel.get_item_by_name(name)
        if not item:
            return {'message': 'item not found'}, 404
        return item.json(), 200

    def post(self, name):
        if ItemModel.get_item_by_name(name):
            return {'message': f'an item with name {name} already exists'}, 400

        request_data = request.get_json()
        price = float(request_data['price'])
        item = ItemModel(name=name, price=price)
        if item.insert():
           return {'name': name, 'price': price}, 201
        else:
            return {'message': 'error occurred while creating record'}, 500

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
        price = float(data['price'])
        item = ItemModel.get_item_by_name(name)
        updated_item = ItemModel(name=name, price=price)
        if item:
            updated_item.update()
        else:
            updated_item.insert()
        return updated_item.json()


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
