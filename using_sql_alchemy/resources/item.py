from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import request
import sqlite3
from using_sql_alchemy.models.item import ItemModel


class Item(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field can not be left blank'
    )
    request_parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help='This field can not be left blank'
    )

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
        item = ItemModel(name=name, price=price, store_id=request_data['store_id'])
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

        # data = request.get_json()
        data = Item.request_parser.parse_args()
        price = float(data['price'])
        item = ItemModel.get_item_by_name(name)
        if item is None:
            item = ItemModel(name=name, price=price, store_id=data['store_id'])
        else:
            item.price = price
        item.save_to_db()
        return item.json()


class ItemList(Resource):

    def get(self):
        return {'items': [item_model.json() for item_model in ItemModel.query.all()]}, 200
