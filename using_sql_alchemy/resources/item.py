from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import request
import sqlite3
from using_sql_alchemy.models.item import ItemModel


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
        try:
            item.save_to_db()
        except:
            return {'message': 'exception occurred'}, 500
        return {'message': 'item created'}, 201

    def delete(self, name):
        item = ItemModel.get_item_by_name(name)
        if item:
            item.delete_from_db()

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
        if item is None:
            item = ItemModel(name=name, price=price)
        else:
            item.price = price
        item.save_to_db()
        return item.json()


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
