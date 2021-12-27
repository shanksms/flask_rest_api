from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

# this creates /auth end point
jwt = JWT(app, authenticate, identity)

items = []

'''
you will have to first call /auth end point, pass user name and password. 
Then you will get jwt token. 
'''


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
        existing_items = [item for item in items if name == request_data['name']]
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
        data = request.get_json()
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


api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
