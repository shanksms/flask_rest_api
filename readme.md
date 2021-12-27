# Flask Rest concepts

## resources
[O'Reilly course] (https://learning.oreilly.com/videos/rest-apis-with/9781788621526/9781788621526-video3_4/)
[Deploy Flask to prod] (https://vsupalov.com/flask-web-server-in-production/)

## Rest Principles

### Thinking end points as resources
Lets say there is a chair resource on a server.
|HTTP Method|Resource|
|----|-----|
|GET|/items/chair|
|POST|/items/chair|
|PUT|/items/chair|
|DELETE|/items/chair|

<br>
as you can see for all the http verbs, same url is sufficient.

### Test-First API design
in this we start with designing the API end points. If possible use a tool like Postman to save the end points.

## Rest Principles - ends
 

### json always used " while python dictionaries can use ' also

## Flask restfull
### This is a sample Flask restful code.
it lets you encapsulate a Resource in a class
```python
from flask import Flask
from flask_restful import Resource, Api
app = Flask(__name__)
api = Api(app)
class Student(Resource):
    def get(self, name):
        return {'student': name}
api.add_resource(Student, '/student/<string:name>')
app.run(port=5000)
```

## Flask restful - ends

### how to return response and status code from Flask
```python
from flask import Response
def rest_end_point_method():
    return Response("{'a':'b'}", status=201, mimetype='application/json')
```