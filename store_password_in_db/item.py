from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import request

items = []

class Item(Resource):
    @jwt_required()
    def get(self, name):
        filtered_items = [item for item in items if item['name'] == name]
        if len(filtered_items) == 0:
            return {'message': 'item not found'}, 404
        else:
            return filtered_items[0], 200

    def post(self, name):
        request_data = request.get_json()
        existing_items = [item for item in items if name == item['name']]
        if len(existing_items) != 0:
            return {'message': 'item already exists'}, 400
        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = [item for item in items if item['name'] != name]
        return {'message': 'item deleted'}

    def put(self, name):
        request_parser = reqparse.RequestParser()
        request_parser.add_argument(
            'price',
            type=float,
            required=True,
            help='This field can not be left blank'
        )
        #data = request.get_json()
        data = request_parser.parse_args()
        filtered_items = [item for item in items if item['name'] == name]
        if len(filtered_items) == 0:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item = filtered_items[0]
            item.update(data)
        return item

class ItemList(Resource):

    def get(self):
        return {'items': items}, 200