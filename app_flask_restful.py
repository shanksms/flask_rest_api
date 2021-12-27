from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)
items = []

class Item(Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item
        return {'name': None}, 404


    def get(self):
        return {'items': items}


    def post(self):
        request_data = request.get_json()
        item = {'name': request_data['name'], 'price': request_data['price']}
        items.append(item)
        return item, 201


api.add_resource(Item, '/items/<string:name>', '/items')

app.run(port=5000, debug=True)