from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
items = []


class Item(Resource):
    def get(self, name):
        filtered_items = [item for item in items if item['name'] == name]
        if len(filtered_items) == 0:
            return {'message': 'item not found'}, 404
        else:
            return filtered_items[0], 200

    def get(self):
        return {'items': items}, 200

    def post(self):
        request_data = request.get_json()
        existing_items = [item for item in items if item['name'] == request_data['name']]
        if len(existing_items) != 0:
            return {'message': 'item already exists'}, 400
        item = {'name': request_data['name'], 'price': request_data['price']}
        items.append(item)
        return item, 201


api.add_resource(Item, '/items/<string:name>', '/items')

app.run(port=5000, debug=True)
